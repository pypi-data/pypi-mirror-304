import urllib.parse
from collections import namedtuple

import requests
requests.packages.urllib3.disable_warnings()

ConnectionConfig = namedtuple("ConnectionConfig", ["host", "port", "username", "password", "database", "protocol"])


def _from_dict(config: dict):
    try:
        conn = config['connection']
        host = conn['host']
        port = conn.get('port', 8123)
        username = conn.get('username', '')
        password = conn.get('password', '')
        database = conn.get('database', '')
        protocol = conn.get('protocol', 'http')

    except KeyError as e:
        raise Exception(f"connection config missing key {e}")
    return ConnectionConfig(host, port, username, password, database, protocol)


def _quote(s: str) -> str:
    if s.endswith('`'):
        return s
    else:
        return f"`{s}`"


class Database:
    """facade clickhouse's HTTP interface
    """

    @staticmethod
    def from_config(config: dict) -> 'Database':
        cc = _from_dict(config)
        return Database(cc)

    def __init__(self, conn_conf: ConnectionConfig):
        self.conn_conf = conn_conf
        self.baseurl = f"{conn_conf.protocol}://{conn_conf.username}:{conn_conf.password}@{conn_conf.host}:{conn_conf.port}/{conn_conf.database}"
        self._test_conn()

    def _query_url(self, query: str):
        return f"{self.baseurl}?query={urllib.parse.quote(query)}"

    def load_csv(self, csv_path, into_table):
        cmd = f"INSERT INTO {_quote(into_table)} FORMAT CSV"
        with open(csv_path, 'rb') as payload:
            r = requests.post(self._query_url(cmd), data=payload, verify=False)
        if not r.ok:
            raise Exception(r.text)

    def query(self, sql: str):
        """
        not performing type mapping
        """
        r = requests.get(self._query_url(sql), stream=True, verify=False)
        if not r.ok:
            raise Exception(r.text)

        for line in r.iter_lines(decode_unicode=True):
            yield line.split('\t')

    def command(self, sql: str):
        r = requests.post(self._query_url(sql), verify=False)
        if not r.ok:
            raise Exception(r.text)
        return r.text

    def _test_conn(self):
        sql = "select 10"
        url = self._query_url(sql)
        r = requests.get(url, verify=False)
        if not r.ok:
            raise Exception(r.text)

# coding: utf-8
from contextlib import contextmanager

import ldap
import ldap.modlist

from django.conf import settings


class LDAPClient(object):

    @staticmethod
    @contextmanager
    def connect(host=None, port=None, basedn=None, user=None, password=None):
        host = host or settings.LDAP["host"]
        port = port or settings.LDAP["port"]
        basedn = basedn or settings.LDAP["basedn"]
        user = user or settings.LDAP["user"]
        password = password or settings.LDAP["password"]
        ldap_client = LDAPClient(host, port, basedn, user, password)
        try:
            yield ldap_client
        finally:
            ldap_client.close()

    def __init__(self, host, port, basedn, user, password):
        self.basedn = basedn
        self.ldap_conn = ldap.initialize("ldap://%s:%s" % (host, port), trace_level=1)
        self.ldap_conn.simple_bind_s(user, password)

    def close(self):
        self.ldap_conn.unbind_s()

    def ola(self):
        pass

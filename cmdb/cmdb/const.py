#!/usr/bin/env python
# coding: utf-8 
# @Time   : const.py
# @Author : Derek
# @File   : 2018/4/8 16:04

from __future__ import unicode_literals


class Const(object):
    """ _attr_list: 写dict的方式，name，value必写的值
    name: 属性名，
    value： 数据库值，
    _attr_dict: name为key，值为dict，保存value等
    """
    def __getattr__(self, attr):
        if getattr(self, '_attr_list', None):
            for item in self._attr_list:
                if item['name'] == attr:
                    return item['value']
        if getattr(self, '_attr_dict', None):
            val = self._attr_dict.get(attr, None)
            if val:
                v = val.get('value', None)
                if v:
                    return v

        return super(Const, self).__getattr__(attr)

    @classmethod
    def get_choices(cls):
        if getattr(cls, '_attr_list', None):
            for item in cls._attr_list:
                setattr(cls, item['name'], item['value'])
        if getattr(cls, '_attr_dict', None):
            for name, item in cls._attr_dict.items():
                setattr(cls, name, item['value'])

        r = []
        for k, v in cls.__dict__.items():
            if not k.startswith('_') and isinstance(v, (int, str)):
                # r.append((v, k))
                r.append((v, cls.get_display(v)))
        return r

    @classmethod
    def get_display(cls):
        raise NotImplementedError


class Status(Const):
    deleted = 0
    normal = 1

    @classmethod
    def get_display(cls, e):
        if e == cls.normal:
            return '正常'
        elif e == cls.deleted:
            return '已删除'
        return '未知'



class HostStatus(Const):
    approving = 0
    using = 1
    destroyed = 2

    @classmethod
    def get_display(cls, e):
        if e == cls.approving:
            return '审批中'
        elif e == cls.using:
            return '使用中'
        elif e == cls.destroyed:
            return '已销毁'
        return '未知'


class UserAction(Const):
    other = 0
    create = 1
    update = 2
    delete = 3

    @classmethod
    def get_display(cls, e):
        if e == cls.create:
            return '创建'
        elif e == cls.update:
            return '更新'
        elif e == cls.delete:
            return '删除'
        elif e == cls.other:
            return '其他'
        return '未知'


class ApprovalStatus(Const):
    approving = 0
    access = 1
    deny = 2

    @classmethod
    def get_display(cls, e):
        if e == cls.approving:
            return '待审核'
        elif e == cls.access:
            return '审核通过'
        elif e == cls.deny:
            return '审核未通过'
        return '未知'


class ImageVisibility(Const):
    private = 0
    public = 1

    @classmethod
    def get_display(cls, e):
        if e == cls.private:
            return '私有'
        elif e == cls.public:
            return '共有'
        return '未知'

    @classmethod
    def get_id_from_openstack(cls, status):
        if status == 'private':
            return cls.private
        elif status == 'public':
            return cls.public
        else:
            raise


class ImageType(Const):
    none = 0
    snapshot = 1
    backup = 2
    image = 3

    @classmethod
    def get_display(cls, e):
        if e == cls.snapshot:
            return '快照'
        elif e == cls.image:
            return '镜像'
        elif e == cls.backup:
            return '备份'
        return '未知'

    @classmethod
    def get_id_from_openstack(cls, status):
        if status == 'snapshot':
            return cls.snapshot
        elif status == 'image':
            return cls.image
        elif status == 'backup':
            return cls.backup
        else:
            raise


class TagIndex(Const):
    env = 'env'
    service = 'service'

    @classmethod
    def get_display(cls, e):
        if e == cls.env:
            return '环境'
        elif e == cls.service:
            return '服务'
        return '未知!'


class ImageStatus(Const):
    active = 0
    saving = 1
    deleted = 2
    error = 3
    unknown = 3

    @classmethod
    def get_display(cls, e):
        if e == cls.active:
            return '运行中'
        elif e == cls.saving:
            return '保存中'
        elif e == cls.deleted:
            return '删除'
        elif e == cls.error:
            return '出错'
        elif e == cls.unknown:
            return '未知'
        return '未知!'

    @classmethod
    def get_id_from_openstack(cls, status):
        if status == 'active':
            return cls.active
        elif status == 'saving':
            return cls.saving
        elif status == 'deleted':
            return cls.deleted
        elif status == 'error':
            return cls.error
        elif status == 'unknown':
            return cls.unknown
        else:
            raise


class NetworkStatus(Const):
    active = 0
    down = 1
    build = 2
    error = 3
    deleted = 9

    @classmethod
    def get_display(cls, e):
        if e == cls.active:
            return '运行中'
        elif e == cls.down:
            return 'DOWN'
        elif e == cls.build:
            return '构建'
        elif e == cls.error:
            return '出错'
        elif e == cls.deleted:
            return '删除'
        return '未知!'

    @classmethod
    def get_id_from_openstack(cls, status):
        if status == 'ACTIVE':
            return cls.active
        elif status == 'DOWN':
            return cls.saving
        elif status == 'BUILD':
            return cls.deleted
        elif status == 'ERROR':
            return cls.error
        else:
            raise


class RuleDirection(Const):
    egress = 'egress'
    ingress = 'ingress'

    @classmethod
    def get_display(cls, e):
        if e == cls.egress:
            return '出口'
        elif e == cls.ingress:
            return '入口'
        return '未知!'


class Protocol(Const):
    _attr_list = [
        {'name': 'tcp', 'value': 'tcp', 'display_name': '定制TCP规则', },
        {'name': 'udp', 'value': 'udp', 'display_name': '定制UDP规则', },
        {'name': 'icmp', 'value': 'icmp', 'display_name': '定制ICMP规则', },
        {'name': 'custom', 'value': 'custom', 'display_name': '其他协议', },
        {'name': 'all_tcp', 'value': 'all_tcp', 'display_name': '所有TCP协议', },
        {'name': 'all_udp', 'value': 'all_udp', 'display_name': '所有UDP协议', },
        {'name': 'all_icmp', 'value': 'all_icmp', 'display_name': '所有ICMP协议', },
        {'name': 'ssh', 'value': 'ssh', 'display_name': 'SSH', },
        {'name': 'dns', 'value': 'dns', 'display_name': 'DNS', },
        {'name': 'http', 'value': 'http', 'display_name': 'HTTP', },
        {'name': 'https', 'value': 'https', 'display_name': 'HTTPS', },
        {'name': 'ms_sql', 'value': 'ms_sql', 'display_name': 'MS SQL', },
        {'name': 'mysql', 'value': 'mysql', 'display_name': 'MySQL', },
        {'name': 'imap', 'value': 'imap', 'display_name': 'imap', },
        {'name': 'imaps', 'value': 'imaps', 'display_name': 'imaps', },
        {'name': 'pop3', 'value': 'pop3', 'display_name': 'pop3', },
        {'name': 'pop3s', 'value': 'pop3s', 'display_name': 'pop3s', },
        {'name': 'smtp', 'value': 'smtp', 'display_name': 'SMTP', },
        {'name': 'smtps', 'value': 'smtps', 'display_name': 'SMTPS', },
        {'name': 'rdp', 'value': 'rdp', 'display_name': 'rdp', },
        {'name': 'ldap', 'value': 'ldap', 'display_name': 'ldap', },
    ]

    @classmethod
    def get_display(cls, e):
        for item in cls._attr_list:
            if item['value'] == e:
                return item['display_name']
        return '未知!'


class EtherType(Const):
    IPv4 = 'IPv4'
    IPv6 = 'IPv6'

    @classmethod
    def get_display(cls, e):
        if e == cls.IPv4:
            return 'IPv4'
        elif e == cls.IPv6:
            return 'IPv6'
        return '未知!'

slave_num = 1

# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, GroupManager, Group


class User(AbstractUser):
    ROLES = (
        ('developer_supremo', u'总监'),
        ('developer_manager', u'经理'),
        ('developer', u'研发'),
    )
    # leader = models.ForeignKey('Group.leader', null=True, blank=True, on_delete=models.CASCADE, related_name='fans')
    # leader = models.CharField(max_length=32, blank=True, null=True)
    role = models.CharField(max_length=32, default='developer', choices=ROLES)
    remark = models.CharField(max_length=128, default='', blank=True)

    class Meta:
        verbose_name_plural = u'用户'

    def __unicode__(self):
        return self.username


# class NewGroup(models.Model):
#     """
#     Groups are a generic way of categorizing users to apply permissions, or
#     some other label, to those users. A user can belong to any number of
#     groups.
#
#     A user in a group automatically has all the permissions granted to that
#     group. For example, if the group 'Site editors' has the permission
#     can_edit_home_page, any user in that group will have that permission.
#
#     Beyond permissions, groups are a convenient way to categorize users to
#     apply some label, or extended functionality, to them. For example, you
#     could create a group 'Special users', and you could write code that would
#     do special things to those users -- such as giving them access to a
#     members-only portion of your site, or sending them members-only email
#     messages.
#     """
#     # name = models.CharField(_('name'), max_length=80, unique=True)
#     leader = models.ForeignKey('User', null=True, blank=True, on_delete=models.CASCADE, db_column='leader')
#     name = models.CharField(max_length=80, unique=True)
#     permissions = models.ManyToManyField(
#         Permission,
#         verbose_name=_('permissions'),
#         blank=True,
#     )
#
#     class Meta:
#         verbose_name_plural = u'用户组'
#
#     def __unicode__(self):
#         return self.name

class NewGroup(Group):
    leader = models.ForeignKey('User', null=True, blank=True, on_delete=models.CASCADE, related_name="fans")

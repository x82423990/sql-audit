from rest_framework import serializers
from account.models import User, NewGroup
from django.contrib.auth.models import Group, Permission
# from django.contrib.auth.models import Permission
from collections import OrderedDict


class UserINFO(serializers.HyperlinkedModelSerializer):
    # ModelSerializer
    '''
    平台用户信息列表serializers
    '''

    class Meta:
        model = User
        fields = ('id', 'username', 'group', 'department', 'email', 'auth_group', 'real_name')
        # fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # days_cccc = serializers.SerializerMethodField()
    #
    # # 方法写法：get_ + 字段
    # def days_cccc(self, obj):
    #     # obj指这个model的对象
    #     print(obj.username)
    #     return obj.username

    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        # 这里框架默认是接受OrderDict参数的方法
        # print("password", instance)
        # print(type(instance))
        ret = super(UserSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            groupobj = instance.groups.first()
            groups = [{'id': groupobj.id, 'name': groupobj.name}] if groupobj else []
            perm_list = instance.user_permissions.all()
            perms = [{'id': perm.id, 'name': perm.name} for perm in perm_list]
            ret['groups'] = groups
            ret['perms'] = perms
            if groupobj:
                new_group = NewGroup.objects.get(pk=groupobj.id)
                ret['leader'] = {'id': new_group.leader.id, 'username': new_group.leader.username}
        return ret

    # 重写create 方法，因为有密码(set password)
    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    # def update_sysaccount(self, validated_data):
    #     default_account = {
    #         'is_active': 0,
    #         'is_staff': 0,
    #         'is_superuser': 0
    #     }
    #     sys_account = validated_data.pop('sysaccount', [])
    #     for account in sys_account:
    #         if account in default_account:
    #             default_account[account] = 1
    #     validated_data.update(default_account)
    #     return validated_data

    # 重写update 方法，
    def update(self, instance, validated_data):
        print("我重写update方法")
        validated_data.pop('password')
        try:
            newpassword = validated_data.pop('newpassword')
        except KeyError:
            newpassword = None
        if newpassword:
            instance.set_password(newpassword)
        # validated_data = self.update_sysaccount(validated_data)
        return super(UserSerializer, self).update(instance, validated_data)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewGroup
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(DepartmentSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            leader = instance.leader.username if instance.leader else ""
            qs_perms = instance.permissions.all()
            perms = [{'id': perm.id, 'name': perm.name} for perm in qs_perms]
            qs_members = instance.user_set.all()
            members = [{'id': user.id, 'name': user.username, 'role': user.role} for user in qs_members]
            # leader =
            ret['leader_name'] = leader
            ret['perms'] = perms
            ret['members'] = members
        return ret


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(GroupSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            qs_perms = instance.permissions.all()
            perms = [{'id': perm.id, 'name': perm.name} for perm in qs_perms]
            qs_members = instance.user_set.all()
            members = [{'id': user.id, 'name': user.username, 'role': user.role} for user in qs_members]
            ret['perms'] = perms
            ret['members'] = members
        return ret


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PersonalCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

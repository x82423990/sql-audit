# -*- coding:utf-8 -*-
from rest_framework import serializers
from ulits.dbcrypt import prpcrypt
from ulits.basemixins import AppellationMixins
from .models import *
from account.models import User
# import datetime
from datetime import datetime, timedelta, timezone


class InceptionSerializer(serializers.ModelSerializer):
    admin = 'Admin'

    class Meta:
        model = Inceptsql
        fields = '__all__'

    def get_step_user_group(self, user_instance):
        print("用户", user_instance)
        group_name = user_instance.groups.first().name if user_instance and not user_instance.is_superuser else self.admin
        return group_name

    def get_step(self, instance):
        data = []
        # 获取工单步骤
        steps = instance.workorder.step_set.order_by('id')
        for step in steps:
            username = step.user.username if step.user else self.admin
            updatetime = step.updatetime if step.status != 0 else ''
            # group = self.get_step_user_group(step.user)
            data.append(
                {
                    'id': step.id,
                    'updatetime': updatetime,
                    'username': username,
                    # 'group': group,
                    'status': step.status
                }
            )
        data.insert(0, {'id': 0, 'updatetime': instance.createtime, 'username': '系统审核', 'status': 1})
        return data

    # 返回样式
    def to_representation(self, instance):
        ret = super(InceptionSerializer, self).to_representation(instance)
        ret['db_name'] = instance.db.name
        ret['steps'] = self.get_step(instance)
        ret['work_order_status'] = instance.workorder.status
        # ret['commiter_email'] = instance.users.email
        print("instance.users.email", instance.users)
        utc = instance.createtime.astimezone(timezone(timedelta(hours=8)))

        # UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        # utcTime = datetime.datetime.strptime(utc, UTC_FORMAT)
        # localtime = utcTime + timedelta(hours=8)
        ret['createtime'] = utc
        return ret


class DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dbconf
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.get('password')
        pc = prpcrypt()
        validated_data['password'] = pc.encrypt(password)
        return super(DbSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password != instance.password:
            pc = prpcrypt()
            validated_data['password'] = pc.encrypt(password)
        return super(DbSerializer, self).update(instance, validated_data)


class ForbiddenWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForbiddenWords
        fields = '__all__'


class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = '__all__'


class PersonalSerializer(AppellationMixins, serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def get_leader(self, env, instance):
        leader_obj = instance.leader if env == self.env_prd else instance
        leader = {'id': leader_obj.id, 'username': leader_obj.username} if leader_obj else {}
        return leader

    def get_db_list(self, env, instance):
        db_queryset = instance.dbconf_set.all() if env == self.env_prd else Dbconf.objects.filter(env=env)
        db_list = [{'id': db.id, 'name': db.name} for db in db_queryset] if db_queryset else []
        return db_list

    def get_commiter(self, instance):
        return {'id': instance.id, 'username': instance.username, 'mail': instance.email}

    def to_representation(self, instance):
        env = self.context['request'].GET.get('env')
        ret = super(PersonalSerializer, self).to_representation(instance)
        ret['leader'] = self.get_leader(env, instance)
        ret['db_list'] = self.get_db_list(env, instance)
        ret['commiter'] = self.get_commiter(instance)
        return ret


class AuthRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthRules
        fields = '__all__'


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(SuggestionSerializer, self).to_representation(instance)
        ret['username'] = instance.user.username if instance.user else ''
        return ret

class AppellationMixins(object):
    dev_spm = 'developer_supremo'
    dev_mng = 'developer_manager'
    dev = 'developer'
    admin = 'admin'
    env_test = 'test'
    env_prd = 'prd'

    action_desc_map = {
        'execute': '代执行',
        'reject': '代放弃',
        'rollback': '代回滚',
        'approve': '代审批通过',
        'disapprove': '代审批驳回',
    }

    reject_steps = {
        dev: 0,
        dev_mng: 1,
        dev_spm: 2
    }


class PromptMxins(object):
    connect_error = 'MySQL连接异常 '
    forbidden_words = '禁用关键字 '
    exception_sqls = 'SQL语法错误 '
    not_exists_group = '用户的组不存在 '
    executed = 'SQL已执行过'
    approve_warning = '此工单无需重复审批'
    reject_warning = '该工单当前的流转状态不在您这里，无法放弃'
    require_handleable = '该工单未审批通过，无法操作'
    require_different = '执行人和审批人相同，无法操作'
    require_same = '您不是该工单的审批人，无法审批'
    require_commiter = '你不是该工单的执行者'
    type_warning = '回滚类型错误(SELECT)'
    old_password_warning = '旧密码错误'
    new_rep_password_warning = '重复密码错误'

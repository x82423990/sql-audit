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
    require_commiter = 'You are not the submitter of the work order！'
    type_warning = '回滚类型错误(SELECT)'
    old_password_warning = '旧密码错误'
    new_rep_password_warning = '重复密码错误'
    not_group = '你不能提交工单，因为你没有领导Txx'
    forbidden_select = "暂不支持Select语句"
    not_sucessed_order = "该工单没有执行，不能回滚"
    row_is_non = "该条mysql语句无效，因为影响行数为0."
    inception_err = 'Inception2 链接失败'

auth_rules = [
    {
        'is_manual_review': True,
        'role': 'developer',
        'env': 'prd',
        'reject': True,
        'execute': False,
        'rollback': False,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': True,
        'role': 'developer_manager',
        'env': 'prd',
        'reject': True,
        'execute': False,
        'rollback': False,
        'approve': True,
        'disapprove': True
    },
    {
        'is_manual_review': True,
        'role': 'developer_supremo',
        'env': 'prd',
        'reject': True,
        'execute': False,
        'rollback': False,
        'approve': True,
        'disapprove': True
    },
    {
        'is_manual_review': True,
        'role': 'admin',
        'env': 'prd',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': True,
        'disapprove': True
    },

    {
        'is_manual_review': False,
        'role': 'developer',
        'env': 'prd',
        'reject': True,
        'execute': False,
        'rollback': False,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': False,
        'role': 'developer_manager',
        'env': 'prd',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': False,
        'role': 'developer_supremo',
        'env': 'prd',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': False,
        'role': 'admin',
        'env': 'prd',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },

    {
        'is_manual_review': True,
        'role': 'developer',
        'env': 'test',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': True,
        'role': 'developer_manager',
        'env': 'test',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': True,
        'role': 'developer_supremo',
        'env': 'test',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': True,
        'role': 'admin',
        'env': 'test',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },

    {
        'is_manual_review': False,
        'role': 'developer',
        'env': 'test',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': False,
        'role': 'developer_manager',
        'env': 'test',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': False,
        'role': 'developer_supremo',
        'env': 'test',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },
    {
        'is_manual_review': False,
        'role': 'admin',
        'env': 'test',
        'reject': True,
        'execute': True,
        'rollback': True,
        'approve': False,
        'disapprove': False
    },

]

step_rules = {
    'developer':
        {
            'commiter_true': [1],
            'commiter_false': [1]
        },
    'developer_manager':
        {
            'commiter_true': [1, 2],
            'commiter_false': [1, 2]
        },
    'developer_supremo':
        {
            'commiter_true': [1, 2],
            'commiter_false': [2, 3]
        },
    'admin':
        {
            'commiter_true': [1, 2],
            'commiter_false': [2, 3]
        }
}

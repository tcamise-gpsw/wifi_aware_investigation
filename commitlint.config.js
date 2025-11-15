module.exports = {
    extends: ['@commitlint/config-conventional'],
    rules: {
        'type-enum': [
            2,
            'always',
            ['feat', 'fix', 'docs', 'chore', 'refactor', 'test', 'ci', 'build'],
        ],
        'scope-enum': [
            2,
            'always',
            [
                'rpi',
                'android',
                'ios',
                'docs',
                'config',
                'deps',
                'ci',
            ],
        ],
        'scope-empty': [0, 'never'],
        'subject-empty': [2, 'never'],
        'subject-full-stop': [2, 'never', '.'],
        'header-max-length': [2, 'always', 100],
    },
};

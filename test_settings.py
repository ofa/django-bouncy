DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './example.db',
    }
}

INSTALLED_APPS = (
    'django_bouncy',
)

BOUNCY_TOPIC_ARN = ['arn:aws:sns:us-east-1:250214102493:Demo_App_Unsubscribes']

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-xunit',
    '--nologcapture',
    '--cover-package=django_bouncy',
]

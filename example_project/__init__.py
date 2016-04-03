# Based off microdjango by J. Cliff Dyer
# Get it at https://bitbucket.org/cliff/microdjango/

ROOT_URLCONF = 'example_project.urls'
SECRET_KEY = u'None'
DEBUG = True
STATIC_URL = '/static/'
SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './example.db',
    }
}

BOUNCY_TOPIC_ARN = ['arn:aws:sns:us-east-1:250214102493:Demo_App_Unsubscribes']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_bouncy'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-xunit',
    '--nologcapture',
    '--cover-package=django_bouncy',
]

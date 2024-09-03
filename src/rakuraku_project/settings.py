import os
from pathlib import Path

# プロジェクトのベースディレクトリを定義
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEYの設定
# 本番環境では、DJANGO_SECRET_KEY環境変数から取得し、設定されていない場合はエラーを出す
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("SECRET_KEY環境変数が設定されていません。")

# デバッグモードの設定
# DJANGO_DEBUG環境変数から取得し、デフォルトはFalse
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# 許可するホストの設定
# DJANGO_ALLOWED_HOSTS環境変数から取得し、カンマ区切りで複数ホストを指定可能
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# アプリケーション定義
INSTALLED_APPS = [
    'rakuraku_apps.apps.RakurakuAppsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ミドルウェア定義
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL設定
ROOT_URLCONF = 'rakuraku_project.urls'

# テンプレート設定
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'rakuraku_apps' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGIアプリケーション設定
WSGI_APPLICATION = 'rakuraku_project.wsgi.application'

# データベース設定
# MySQLの接続情報を環境変数から取得
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'katsurao_db'),
        'USER': os.getenv('MYSQL_USER', 'user'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'password'),
        'HOST': os.getenv('MYSQL_HOST', 'localhost'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
    }
}

# パスワードバリデータ
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 言語とタイムゾーンの設定
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 静的ファイルのURLとディレクトリ設定
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# デフォルトのプライマリキー設定
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# カスタムユーザーモデルの設定
AUTH_USER_MODEL = "rakuraku_apps.User"

# ログイン・ログアウトのリダイレクトURL設定
LOGIN_REDIRECT_URL = "rakuraku_apps:home"
LOGOUT_REDIRECT_URL = "rakuraku_apps:login"

# LINE Notifyのアクセストークン設定
LINE_NOTIFY_ACCESS_TOKEN = os.getenv('LINE_NOTIFY_ACCESS_TOKEN', '')

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta
SECRET_KEY = os.getenv('SECRET_KEY', 'chave_de_teste_local')

# Debug
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # True local, False no Render via .env

# Hosts
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
else:
    ALLOWED_HOSTS = ['dojo-on.onrender.com']

CSRF_TRUSTED_ORIGINS = [
    'https://dojo-on.onrender.com',
]

# Apps e Middleware (sem mudanças)
INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'core','pag1','pag2','pag3','pag4','pag5','pag6','pag7',
    'home','ukemis','quiz','historia','palavras','regras','payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'payments.middleware.PaymentMiddleware',
]

ROOT_URLCONF = 'meu_projeto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]},
    },
]

WSGI_APPLICATION = 'meu_projeto.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuração para encontrar arquivos estáticos em desenvolvimento
# Esta configuração diz ao Django onde procurar por arquivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Configuração do WhiteNoise para servir arquivos estáticos
# Em desenvolvimento, o Django serve os arquivos estáticos automaticamente
# Em produção, o WhiteNoise é responsável por servir esses arquivos
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # Em desenvolvimento, usar o storage padrão do Django
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'

# Configuração para desenvolvimento
DEVELOPMENT_MODE = True  # Mude para False em produção

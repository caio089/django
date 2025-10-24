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
ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver,www.dojoon.com.br,dojoon.com.br,dojo-on.onrender.com,dojoon.onrender.com').split(',')]

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://www.dojoon.com.br',
    'https://dojoon.com.br',
    'http://www.dojoon.com.br',
    'http://dojoon.com.br',
    'https://dojoon.onrender.com',
    'https://dojo-on.onrender.com',
    'https://*.onrender.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Configurações adicionais para domínios customizados
USE_TZ = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CSRF Settings
CSRF_COOKIE_SECURE = not DEBUG  # True em produção, False em desenvolvimento
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False
CSRF_COOKIE_AGE = 3600  # 1 hora
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'  # View padrão para falhas CSRF
CSRF_COOKIE_DOMAIN = None  # Permitir em localhost

# Apps e Middleware (sem mudanças)
INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'core','pag1','pag2','pag3','pag4','pag5','pag6','pag7',
    'home','ukemis','quiz','historia','palavras','regras','payments','dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'meu_projeto.supabase_middleware.SupabaseConnectionMiddleware',  # Middleware para conexões Supabase
    'meu_projeto.middleware.WWWRedirectMiddleware',  # Redirecionamento www
    'meu_projeto.supabase_pro_middleware.SupabaseProMiddleware',  # Middleware otimizado para Supabase Pro
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'dashboard.middleware.DashboardPerformanceMiddleware',  # Otimização do dashboard
    'payments.middleware_payment_sync.PaymentSyncMiddleware',  # Sincronização automática de pagamento
    'payments.middleware.PremiumAccessMiddleware',
    'payments.security.SecurityMiddleware',
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

# Database - Configuração para Supabase PostgreSQL
import dj_database_url

# Configuração do Supabase - SEMPRE usar PostgreSQL
if os.getenv('DATABASE_URL'):
    # Usar DATABASE_URL do Supabase
    DATABASES = {
        'default': dj_database_url.parse(
            os.getenv('DATABASE_URL'),
            conn_max_age=0,  # Não reutilizar conexões
            conn_health_checks=False,  # Desabilitar verificações de saúde
        )
    }
    
    # Configurações específicas para Supabase
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
        'connect_timeout': 60,  # Aumentar timeout
        'application_name': 'django_app',
        'options': '-c default_transaction_isolation=read_committed'
    }
    
    # Configurações de pool de conexões para Supabase
    DATABASES['default']['CONN_MAX_AGE'] = 0
    DATABASES['default']['AUTOCOMMIT'] = True
    
elif os.getenv('DB_HOST'):
    # Configuração manual do Supabase
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'postgres'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
                'connect_timeout': 60,
                'application_name': 'django_app',
            },
            'CONN_MAX_AGE': 0,
            'AUTOCOMMIT': True,
        }
    }
else:
    # Fallback para SQLite apenas em desenvolvimento local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Cache otimizado para reduzir carga no Supabase
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    }
}

# Configurações para resolver problema do modo Session do Supabase
DISABLE_HEAVY_PROCESSES = True  # Desabilitar processos que consomem conexões
LIGHT_MODE = True  # Modo leve para evitar esgotamento do pool
SUPABASE_SESSION_MODE = True  # Supabase está em modo Session (limitado)
MAX_CONCURRENT_CONNECTIONS = 3  # Limite muito baixo para modo Session

# Configurações de sessão otimizadas
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Usar banco para evitar problemas CSRF
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True

# Configurações adicionais para reduzir uso de banco
DATABASE_ROUTERS = []  # Sem roteadores de banco
CONN_MAX_AGE = 0  # Fechar conexões imediatamente
DATABASES['default']['CONN_MAX_AGE'] = 0  # Forçar fechamento imediato

# Senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
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

# Configurações adicionais para produção
if not DEBUG:
    # Forçar HTTPS em produção
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'home'

# Configurações de segurança para produção
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Configurações específicas para domínios customizados
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# =====================================================
# CONFIGURAÇÕES DO MERCADO PAGO
# =====================================================

# Credenciais do Mercado Pago
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN', '')
MERCADOPAGO_PUBLIC_KEY = os.getenv('MERCADOPAGO_PUBLIC_KEY', '')
MERCADOPAGO_WEBHOOK_SECRET = os.getenv('MERCADOPAGO_WEBHOOK_SECRET', '')
MERCADOPAGO_WEBHOOK_URL = os.getenv('MERCADOPAGO_WEBHOOK_URL', '')

# Configurações de email para notificações
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@dojoon.com.br')

# Configurações de logging para debug
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'payments': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

from .celery import celery as celery_app

try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass

__all__ = ('celery_app',)
import sys, os

current_path = os.path.abspath('.')
sys.path.append(current_path)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = '/Users/ender/Documents/workspace/kimlerdensin/src/templates'
MEDIA_ROOT = '/Users/ender/Documents/workspace/kimlerdensin/static/'
MEDIA_URL = 'http://localhost:8000'

DATABASE_NAME = '/Users/ender/Documents/workspace/kimlerdensin/db/kimlerdensin.db'
DATABASE_ENGINE = 'sqlite3'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


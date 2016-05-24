import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_redis_sessions',
    'pyramid_tm',
    'SQLAlchemy',
    'sqlalchemy_utils',
    'psycopg2',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'marshmallow',
    'alembic',
    'pycrypto',
    'bcrypt',
    'requests'
]

setup(name='smartgymapi',
      version='0.0',
      description='smartgymapi',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='smartgymapi',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = smartgymapi:main
      [console_scripts]
      initialize_smartgymapi_db = smartgymapi.scripts.initializedb:main
      """,
      )

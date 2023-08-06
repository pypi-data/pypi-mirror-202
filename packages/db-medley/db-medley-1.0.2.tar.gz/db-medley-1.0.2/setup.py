import re
import ast
import os
import shutil

from setuptools import setup, find_packages


do_cythonize = os.getenv('CYTHONIZE', 'false').lower() == 'true'
ext_modules = []
cmdclass = {}
packages = find_packages(exclude=["tests"])

if do_cythonize:
    try:
        from Cython.Build import cythonize
        from Cython.Distutils import build_ext

        class MyBuildExt(build_ext):
            def run(self):
                build_ext.run(self)
                build_dir = os.path.realpath(self.build_lib)
                root_dir = os.path.dirname(os.path.realpath(__file__))
                target_dir = build_dir if not self.inplace else root_dir
                self.copy_file('db_medley/__init__.py', root_dir, target_dir)

            def copy_file(self, path, source_dir, destination_dir):
                if os.path.exists(os.path.join(source_dir, path)):
                    shutil.copyfile(os.path.join(source_dir, path),
                                    os.path.join(destination_dir, path))

        cmdclass['build_ext'] = MyBuildExt
        ext_modules = cythonize("db_medley/*.py")
        packages = []

    except ImportError:
        pass

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('db_medley/__init__.py', 'rb') as f:
    __version__ = str(
        ast.literal_eval(
            _version_re.search(f.read().decode('utf-8')).group(1)))

setup(name='db-medley',
      version=__version__,
      description="Database Helpers",
      long_description=open('README.md', 'r').read(),
      maintainer="Bravos Power Corp.",
      license="MIT",
      url="https://gitlab.com/bravos2/libs/db-medley",
      packages=packages,
      include_package_data=True,
      install_requires=[],
      ext_modules=ext_modules,
      extras_require={
          'sqlalchemy': ['SQLAlchemy', 'python-dateutil>=2.4.2'],
          'flask_sqlalchemy':
          ['SQLAlchemy', 'Flask-SQLAlchemy', 'python-dateutil>=2.4.2'],
          'redis': ['redis>=2.10.6'],
          'aws': ['boto3>=1.11', 'botocore>=1.14'],
          'elasticsearch': [
              'elasticsearch>=6.3',
              'requests-aws4auth>=0.9',
              'elasticsearch-dsl>=6.2',
          ],
          'arangodb': ['python-arango >=3.12.1'],
          'dev': ['honcho>=1.0'],
          'test': [
              'pytest', 'tox>=3,<4', 'coverage>=4.0a5',
              'psycopg2-binary>=2.7.5', 'mock>=1,<2', 'mysqlclient',
              'Flask>=1.0.2'
          ],
          'build': ['wheel', 'twine'],
      },
      cmdclass=cmdclass)

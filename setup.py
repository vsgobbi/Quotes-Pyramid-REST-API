from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

requires = ["pyramid", "waitress", "sqlalchemy", "transaction", "zope.sqlalchemy"]


setup(name="quotes",
      version="1.0",
      description="quotes restful api sample",
      install_requires=requires,
      author="vsgobbi",
      author_email="sgobbivitor@gmail.com",
      url="",
      packages=find_packages(),
      include_package_data=True,
      license="GPLv3",
      entry_points={
            'paste.app_factory': [
                  'main = quotes:main',
            ],
            'console_scripts': [
                  'initialize_wiki2_db=wiki2.scripts.initialize_db:main',
            ],
      },
      )


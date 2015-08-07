from setuptools import setup, find_packages

requires = [
    'clld>=1.5.0',
    'clldmpg>=1.0.0',
    'psycopg2',
    'fuzzywuzzy',
]

tests_require = [
    'WebTest >= 1.3.1', # py3 compat
    'mock',
]

setup(name='dogonlanguages',
      version='0.0',
      description='dogonlanguages',
      long_description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      test_suite="dogonlanguages",
      entry_points="""\
[paste.app_factory]
main = dogonlanguages:main
""",
      )

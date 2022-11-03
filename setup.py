from setuptools import setup, find_packages


setup(
    name='dogonlanguages',
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
    install_requires=[
        'clld>=9.2.2',
        'clldmpg>=4.2',
        'fuzzywuzzy',
        'pyglottolog',
        'sqlalchemy>=1.4.26',
        'waitress',
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox',
        ],
        'test': [
            'mock',
            'psycopg2',
            'pytest>=3.1',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="dogonlanguages",
    entry_points="""\
[paste.app_factory]
main = dogonlanguages:main
""")

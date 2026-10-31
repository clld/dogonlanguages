# Releasing the Dogon and Bangime Linguistics clld app

```shell
git clone https://github.com/clld/dogonlanguages
cd dogonlanguages
pip install -e .[test]
```

A PostgreSQL database named `dogonlanguages` must be available.

Make sure the tests pass (in clld/concepticon):
```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 dogonlanguages > dogonlanguages.sql.gz
```


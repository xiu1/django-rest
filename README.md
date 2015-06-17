# django-rest
Simple REST view for django

|Request method|SQL|
|---|---|
|GET|SELECT|
|POST|INSERT|
|PUT/PATCH|UPDATE| 
|DELETE|DELETE|

# HOW TO INSTALL

```
$ python setup.py develop
or
$ python setup.py install
```

# HOW TO USE

```
from django_rest.views import RestView

class TestRestView(RestView):
    model = <Your Moldel>
    allow_http_method = ['GET', 'POST', 'PUT', 'DELETE']
```

## GET

```
curl "http://localhost:8000/path/to/views?id=1&name=foo"
```

## POST

```
curl -X POST -d '{"name": "new_name"}' "http://localhost:8000/path/to/views"
```

## PUT or PATCH

```
curl -X PUT -d '{"name": "update_name"}' "http://localhost:8000/path/to/views?id=1"
```

## DELETE

```
curl -X DELETE -d "http://localhost:8000/path/to/views?id=1"
```

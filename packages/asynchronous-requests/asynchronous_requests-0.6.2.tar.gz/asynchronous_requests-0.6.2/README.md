# asynchronous_requests

Brings support for `async`/`await` syntax to Python's fabulous `requests` library.

<p>
<a href="https://travis-ci.org/encode/asynchronous_requests">
    <img src="https://travis-ci.org/encode/asynchronous_requests.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/encode/asynchronous_requests">
    <img src="https://codecov.io/gh/encode/asynchronous_requests/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/asynchronous_requests/">
    <img src="https://badge.fury.io/py/asynchronous_requests.svg?cache0" alt="Package version">
</a>
</p>

## Requirements

* Python 3.6+

## Installation

```shell
$ pip install asynchronous_requests
```

## Usage

Just use *the standard requests API*, but use `await` for making requests.

**Note**: Use `ipython` to try this from the console, since it supports `await`.

```python
import asynchronous_requests as requests


response = await requests.get('https://example.org')
print(response.status_code)
print(response.text)
```

Or use explicit sessions, with an async context manager.

```python
import asynchronous_requests as requests


async with requests.Session() as session:
    response = await session.get('https://example.org')
    print(response.status_code)
    print(response.text)
```

The `asynchronous_requests` package subclasses `requests`, so you're getting all the
standard behavior and API you'd expect.

## Streaming responses & requests

The `iter_content()` and `iter_lines()` methods are async iterators.

```python
response = await requests.get('https://example.org', stream=True)
async for chunk in response.iter_content():
    ...
```

The method signatures remain the same as the standard `requests` API:

* `iter_content(chunk_size=1, decode_unicode=False)`
* `iter_lines(chunk_size=512, decode_unicode=False, delimiter=None)`

The methods will yield text if `decode_unicode` is set and the response includes
an encoding. Otherwise the methods will yield bytes.

You can also stream request bodies. To do this you should use an asynchronous
generator that yields bytes.

```python
async def stream_body():
    ...

response = await requests.post('https://example.org', data=stream_body())
```

## Mock Requests

In some situations, such as when you're testing a web application, you may
not want to make actual outgoing network requests, but would prefer instead
to mock out the endpoints.

You can do this using the `ASGISession`, which allows you to plug into
any ASGI application, instead of making actual network requests.

```python
import asynchronous_requests

# Create a mock service, with Starlette, Responder, Quart, FastAPI, Bocadillo,
# or any other ASGI web framework.
mock_app = ...

if TESTING:
    # Issue requests to the mocked application.
    requests = asynchronous_requests.ASGISession(mock_app)
else:
    # Make live network requests.
    requests = asynchronous_requests.Session()
```

## Test Client

You can also use `ASGISession` as a test client for any ASGI application.

You'll probably want to install `pytest` and `pytest-asyncio`, or something
equivalent, to allow you to write `async` test cases.

```python
from asynchronous_requests import ASGISession
from myproject import app
import pytest

@pytest.mark.asyncio
async def test_homepage():
    client = ASGISession(app)
    response = await client.get("/")
    assert response.status_code == 200
```


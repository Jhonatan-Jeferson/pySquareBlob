# Introduction

This project is just a simple way to interact with Square Cloud Blob service

## About the project

This python package is just a simple way to interact with Square Cloud Blob while the official is not released.
You can use this package to upload objects, get objects, get account infos. All routes are already implemented in this code.
Only the post response still doesn't have a class/object to it but all the other methods returns one class/Object or a list of them.

## How to use

1. Install the package with `pip install pysquareblob`
2. Get your API key on [Square Cloud](https://squarecloud.app/pt-br/dashboard/settings)
3. Instantiate the client class passing your API key
4. You can find some methods examples in this Github [repository](https://github.com/Jhonatan-Jeferson/pySquareBlob/tree/main/examples).

## Extras

If you want to remove the logs or reduce the clean cache timer, you can pass some additional params to the class instance.
For cache timer, always pass the time in seconds.
For logs, always a boolean value.
Here's an example:

```python
from pysquareblob import Client

blob_client = Client('Your api key', clean_cache_timer=90.0, debug=False)
```

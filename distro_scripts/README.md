# The API

The bot expects each distro to have a class with a classmethod called search().

The search() method should be defined like this:

```python
def search(name, arch=None, repository=None)
```

It should return an array of hashes. Each hash should contain at least ([1]):

```python
{
    'name': pkg_name, # String
    'version': pkg_version, # String
    'repo': pkg_repo, # String
    'arch': pkg_arch, # String
    'licenses': pkg_licenses, # Array
}
```

[1] it can optionally contain more data, which will be added to the end of the
  result. But don't go crazy, because we want to be able to show several results.
  Brevity is a good thing here. And remember to use meaningful keys.
  All extra values must be Strings.
  Some extra things you might include are:
  * maintainer
  * last update timestamp
  * package size
# How to release this package

## Build

```bash
make build
```

## Publish

```bash
TWINE_USERNAME=__token__
TWINE_PASSWORD=pypi-<YOUTTOKEN>
make publish
```

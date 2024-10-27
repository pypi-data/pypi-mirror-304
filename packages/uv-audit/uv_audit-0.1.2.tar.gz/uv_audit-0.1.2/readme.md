# uv Audit Tool

uv tool for checking dependencies for vulnerabilities

[![PyPI](https://img.shields.io/pypi/v/uv-audit)](https://pypi.org/project/uv-audit/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uv-audit)](https://pypi.org/project/uv-audit/)

[![Downloads](https://static.pepy.tech/badge/uv-audit)](https://pepy.tech/project/uv-audit)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/uv-audit)](https://gitlab.com/rocshers/python/uv-audit)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/uv-audit)](https://gitlab.com/rocshers/python/uv-audit)

Powered by [safety](https://safetycli.com)

## Functionality

- Check **dependencies**

## Quick start

```bash
uvx uv-audit

# Or using uvxt
uv tool install uvxt
uvxt audit
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/uv-audit/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/uv-audit>

Before adding changes:

```bash
make install
```

After changes:

```bash
make format test
```

# sag_py_fastapi_health
[![Maintainability][codeclimate-image]][codeclimate-url]
[![Coverage Status][coveralls-image]][coveralls-url]
[![Known Vulnerabilities][snyk-image]][snyk-url]

Add health check endpoints to fastapi (similar to the ones dotnet core has)

## What it does
* Adds one or multiple health endpoint
* Configurable output format (json or prtg)
* Possibility to add checks (own and pre shipped)
* Pre-Shipped tests for http get requests including basic auth and directory existence/readability/writability

### Installation
pip install sag-py-fastapi-health

## How to use

### Sample usage with existing checks
```python
from sag_py_fastapi_health.checks.http import HttpCheck
from sag_py_fastapi_health.checks.storage import StorageExistsCheck, StorageReadableCheck
from sag_py_fastapi_health.formatter import DefaultResponseFormatter, PrtgResponseFormatter
from sag_py_fastapi_health.models import Probe
from sag_py_fastapi_health.router import HealthcheckRouter

from config import config

router = HealthcheckRouter(
    Probe(
        name="health",
        response_formatter=DefaultResponseFormatter(),
        checks=[
            StorageExistsCheck("/opt/app/data", name="my_dir_exists"),
            StorageReadableCheck("/opt/app/data", name="my_dir_is_readable"),
            HttpCheck("https://localhost/auth", name="auth_available", timeout=5),
        ],
    ),
    Probe(
        name="health-prtg",
        response_formatter=PrtgResponseFormatter(),
        checks=[
            StorageExistsCheck("/opt/app/data", name="my_dir_exists"),
            StorageReadableCheck("/opt/app/data", name="my_dir_is_readable"),
            HttpCheck("https://localhost/auth", name="auth_available", timeout=5),
        ],
    ),
)

```
### Write your own check
```python
from sag_py_fastapi_health.models import CheckResult

class TestCheck(Check):
    def __init__(self, name: str = "check") -> None:
        self._name: str = name

    async def __call__(self) -> CheckResult:
        is_healthy: bool = a_custom_check()
        description: str = "A description of the status or a error message"

        return CheckResult(
            name=self._name,
            status="Healthy" if is_healthy else "Unhealthy",
            description=description,
        )
```
The description contains something like "Directory ... was accessable" or "Service is running" if everything is ok.
If there was an error, you can add the error message/exception message there.

## How to publish
* Update the version in setup.py and commit your change
* Create a tag with the same version number
* Let github do the rest

[codeclimate-image]:https://api.codeclimate.com/v1/badges/518206f10db22dbeb984/maintainability
[codeclimate-url]:https://codeclimate.com/github/SamhammerAG/sag_py_fastapi_health/maintainability
[coveralls-image]:https://coveralls.io/repos/github/SamhammerAG/sag_py_fastapi_health/badge.svg?branch=master
[coveralls-url]:https://coveralls.io/github/SamhammerAG/sag_py_fastapi_health?branch=master
[snyk-image]:https://snyk.io/test/github/SamhammerAG/sag_py_fastapi_health/badge.svg
[snyk-url]:https://snyk.io/test/github/SamhammerAG/sag_py_fastapi_health

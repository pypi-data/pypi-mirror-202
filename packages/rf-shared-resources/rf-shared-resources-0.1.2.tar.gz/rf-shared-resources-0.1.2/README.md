# rf-shared-resources

[![CI](https://github.com/kangasta/rf-shared-resources/actions/workflows/ci.yml/badge.svg)](https://github.com/kangasta/rf-shared-resources/actions/workflows/ci.yml)
[![Release](https://github.com/kangasta/rf-shared-resources/actions/workflows/release.yml/badge.svg)](https://github.com/kangasta/rf-shared-resources/actions/workflows/release.yml)

Library for importing Robot Framework resource files from python libraries. See [examples/](./examples) directory for an example of Python library with embedded Robot Framework resources and usage of this library.

## Usage

There are three different ways to import resources with this library: inside the Python library that contains the resources, in Settings table with initialization parameters, or through a keyword.

### Inside a Python library

```python
from SharedResources import SharedResources

class EmbeddedResources(SharedResources):
    def __init__(self):
        super().__init__(
            'EmbeddedResources.resources',
            'a_keywords.resource',
            'b_keywords.robot')
```

### In settings table

```robot
*** Settings ***
Library  SharedResources  EmbeddedResources
...      a_keywords.resource b_keywords.robot
```

### Through a keyword

```robot
*** Settings ***
Library  SharedResources

*** Keywords ***
Load resources
    Import resource from package  EmbeddedResources.resources
    ...  a_keywords.resource  b_keywords.robot
```

## Testing

Check and automatically fix formatting with:

```bash
pycodestyle SharedResources
autopep8 -aaar --in-place SharedResources
```

Run static analysis with:

```bash
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance SharedResources
```

Run acceptance tests:

```bash
# Run acceptance tests
robot -L TRACE:INFO -d out/ acceptance_tests/

# Run acceptance tests with coverage analysis
coverage run \
    --branch \
    --source SharedResources/ \
    -m robot -L TRACE:INFO -d out/ acceptance_tests/
coverage report -m
```

Run acceptance tests in Docker container:

```bash
# Build image
docker build . -t atest

# Run acceptance tests
docker run --rm atest

# Run acceptance tests and get test output to ./out
docker run -v $(pwd)/out:/out --rm atest -d /out -L TRACE:INFO
```

Generate documentation with:

```bash
python3 -m robot.libdoc SharedResources docs/index.html
```

# devpipe

[![Tests](https://github.com/sebustam/devpipe/actions/workflows/tests.yaml/badge.svg)](https://github.com/sebustam/devpipe/actions/workflows/tests.yaml)

devpipe is a little Python package for caching pipeline results.

## Installation

Create and activate a virtual environment and then install devpipe:

```bash
pip install devpipe
```

## Basic usage

The following example shows a simple ETL pipeline.

```python
import devpipe as dp

@dp.step
def extract(source: str) -> int:
    return 1

@dp.step
def transform(data: int) -> int:
    return data + 1

@dp.step
def load(data: int) -> bool:
    print(data)
    return True

@dp.pipeline
def etl(source: str) -> None:
    extracted = extract(source=source)
    transformed = transform(data=extracted)
    response = load(data=transformed)
    return response
```

Results are cached by default based on the decorated function arguments. The
following code runs the pipeline twice, but only the first time the pipeline
is executed. The second time, the results are loaded from the cache.

```python
res1 = etl(source='source')
res2 = etl(source='source')

assert res1 == res2
```

You can set a name, force rerun or disable cache both at the step and pipeline
levels.

```python
import devpipe as dp

@dp.step(name='My Step', rerun=False, cache=True)
def step_function() -> None:
    return None

@dp.pipeline(name='My Pipeline', rerun=True, cache=True)
def pipeline_function() -> None:
    return step_function()
```

Check the [documentation](https://sebustam.github.io/devpipe/) for more
details.

## License

This project is licensed under the terms of the MIT license.

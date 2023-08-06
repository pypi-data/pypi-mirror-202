# Kogger

This is a very simple logger.

# Install

```shell script
pip install kogger
# or pip install git+https://github.com/zengbocheng/kogger.git
```

# Usage
There are two basic methods to use it.

## Create a Logger Object

```python
from kogger import Logger

logger = Logger('__main__')
# logger = Logger('__main__', stream='out.log')
# logger = Logger()

logger.info('Hello, world!')
logger.warning('Hello, world!')
logger.error('Hello, world!')
```

The output of is

```shell script
[2023-04-11 23:26:38] [__MAIN__] [INFO] Hello, world!
[2023-04-11 23:26:38] [__MAIN__] [WARNING] Hello, world!
[2023-04-11 23:26:38] [__MAIN__] [ERROR] Hello, world!
```

## Use the Default Logger of Package

```python
import kogger

# kogger.set_name('__main__')
# kogger.set_file('out.log')
kogger.info('Hello, world!')
```

# Warning

If you use the logger in multiple processes to output logs synchronously into the same file, the behaviors are undefined. You have better to find another package supporting multiple processes.
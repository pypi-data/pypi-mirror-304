[![PyPI version](https://badge.fury.io/py/yundownload.svg)](https://badge.fury.io/py/yundownload)

# Intro

[官方文档](https://2214372851.github.io/yundownload/)
> This project is a file downloader, supporting dynamic download according to the size of the file to choose the
> download mode, for the connection that supports breakpoint continuation will automatically break the connection, for
> the
> unsupported link will overwrite the previous content, the project includes retry mechanism, etc., currently supports:
> streaming download, large file fragment download.

# Install

`pip install yundownload`

# Document

[yundownload GitHub](https://github.com/2214372851/yundownload)

# Give an example

```python
from yundownload import YunDownloader, Limit

yun = YunDownloader(
    limit=Limit(
        max_concurrency=4,
        max_join=4
    ),  # concurrency
    timeout=1000,
    # You are advised to set a longer timeout period for large file fragments because large file fragments exert pressure on the peer server
    dynamic_concurrency=True,
)
# Files larger than this size are downloaded in fragments
yun.DISTINGUISH_SIZE = 100 * 1024 * 1024
# The size of each shard at download time
yun.CHUNK_SIZE = 100 * 1024 * 1024
# Heartbeat status detection time
yun.HEARTBEAT_SLEEP = 1
# Run task. error_retry: Number of retries when an error occurs
yun.download(
    url='https://dldir1.qq.com/qqfile/qq/PCQQ9.7.17/QQ9.7.17.29225.exe',
    save_path='QQ9.7.17.29225.exe',
    error_retry=3)
```

## Command line tool

> In version 0.1.16, a command line tool was added, which can be used as follows:

```shell
yundownload -h
usage: yundownload [-h] [-mc MAX_CONCURRENCY] [-mj MAX_JOIN] [-t TIMEOUT] [-r RETRY] [--stream] [--wget] [-V] url save_path

Yun Downloader

positional arguments:
  url                   Download url
  save_path             Save path, including file name

options:
  -h, --help            show this help message and exit
  -mc MAX_CONCURRENCY, --max_concurrency MAX_CONCURRENCY
                        Maximum concurrency
  -mj MAX_JOIN, --max_join MAX_JOIN
                        Maximum connection number
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout period
  -r RETRY, --retry RETRY
                        Retry times
  --stream              Forced streaming
  --wget                Carry the wget request header
  -V, --version         Show the version number and exit
```

# Update log
- V 0.3.4
  - Fixed event loop duplicate creation
- V 0.3.3
  - Fix progress bar not reset
- V 0.3.2
  - Fixed the file length inconsistency caused by the request header
- V 0.3.1
  - Added version attribute to the package. 
    The command line tool wget parameter has also been added to give the request a default header
- V 0.3.0
    - To optimize the performance of the code, need to pay attention to at the same time, in this version and later
      versions of the API changes, details please refer to
      the [official documentation](https://2214372851.github.io/yundownload/) description of V0.3 version
- V 0.2.15
    - Big change, remove 'run' function, add 'download' function. See the documentation.
- V 0.2.14
    - Modified the document and some prompts.
- V 0.2.13
    - Fixed multiple file fragment download file name issue
- V 0.2.12
    - Fixed a size issue with the last piece of the shard download file
- V 0.2.11
    - Removes the compressed portion of the default request header
- V 0.2.10
    - Agent added to support proxy
- V 0.2.9
    - Fix known bugs
- V 0.2.8
    - Fix known bugs and add warnings for subsequent optimization of large file shards
- V 0.2.7
    - Fix known bugs
- V 0.2.6
    - None Example Change the asynchronous writing of files in fragment download
- V 0.2.5
    - Fix known bugs
- V 0.2.4
    - Add the auth parameter to carry identity information
    - You can add the max_redirects parameter to limit the number of redirects
    - Add the retries parameter to specify the number of request tries
    - Add the verify parameter to specify whether to verify the SSL certificate
- V 0.2.3
    - Remove the default log display and add a progress bar to the command line tool
- V 0.2.2
    - Fixed exception handling of sharding download
- V 0.2.1
    - Repair download failure displays complete
- V 0.2.0
    - Fixed an issue with fragment breakpoint continuation in fragment download
- V 0.1.19
    - Fix stream download breakpoint resume issue
- V 0.1.18
    - Fix known bugs
- V 0.1.17
    - Add forced streaming downloads
- V 0.1.16
    - Add command line tools
- V 0.1.15
    - Optimized fragmentation download breakpoint continuation
- V 0.1.14
    - exclude
- V 0.1.13
    - Troubleshooting Heartbeat detection
- V 0.1.12
    - This version throws an exception after a retry failure
- V 0.1.10
    - Optimized breakpoint continuation
    - Optimized concurrent downloads
    - Optimized heartbeat detection
    - Optimized error retry
    - This version still does not throw an exception after a retry failure

# Future

- Provides webui or desktop applications
- Asynchronous support for YunDownloader (although asynchronous is currently used internally, downloader cannot be used
  in asynchronous functions)
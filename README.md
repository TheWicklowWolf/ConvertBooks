![Build Status](https://github.com/TheWicklowWolf/ConvertBooks/actions/workflows/main.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/thewicklowwolf/convertbooks.svg)

Convert eBooks to epub, mobi and/or awz3


## Run using docker-compose

```yaml
services:
  convertbooks:
    image: thewicklowwolf/convertbooks:latest
    container_name: convertbooks
    volumes:
      - /path/to/books_source:/convertbooks/source
      - /path/to/books_destination:/convertbooks/destination
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
```

## Configuration via environment variables

Certain values can be set via environment variables:

* __book_source_formats__: Defines the file formats to search for in the source folder. Defaults to `.epub,.mobi,.azw3`.
* __desired_output_formats__: Specifies the formats to convert eBooks into. Defaults to `.mobi,.azw3`.
* __schedule__: Sets the times for the conversion process to run, specified in hours. Defaults to `0`.
* __run_at_startup__: Controls whether the conversion process should initiate automatically at startup. Defaults to `False`.
* __thread_limit__: Specifies the maximum number of concurrent threads for running conversion tasks. Defaults to `1`.

---

https://hub.docker.com/r/thewicklowwolf/convertbooks

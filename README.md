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
      - path/to/books:path/to/books
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
```

## Configuration via environment variables

Certain values can be set via environment variables:

* __path_to_books__: The actual ebook folder path. Defaults to `path/to/books`.
* __desired_formats__: The desired ebook formats. Defaults to `.epub,.mobi,.azw3`.
* __schedule__: The time to run the conversions. Defaults to `0`.
* __run_at_startup__: Wether to run at startup. Defaults to `False`.
* __thread_limit__: Max number of threads to run. Defaults to `1`.

---

https://hub.docker.com/r/thewicklowwolf/convertbooks

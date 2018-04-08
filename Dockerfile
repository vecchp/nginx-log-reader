FROM pypy:3-5.10.1-slim

ARG TEST_MODE
RUN if [ "${TEST_MODE}x" != "x" ] ; then pip install pytest==3.5.0; fi

COPY nginx_parser /src/app/nginx_parser
WORKDIR /src/app

CMD pypy3 -m nginx_parser.main


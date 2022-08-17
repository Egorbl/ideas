FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG PROJ_DIR=/my_proj

RUN mkdir -p ${PROJ_DIR}
COPY ./backend ${PROJ_DIR}

WORKDIR ${PROJ_DIR}

RUN pip install -U pip \
    pip install -r requirements.txt

COPY ./compose/django/entry.sh /entry.sh
RUN chmod +x /entry.sh

ENTRYPOINT ["/entry.sh"]
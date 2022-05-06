FROM python:3.9-slim

# PYTHONUNBUFFERED: Force stdin, stdout and stderr to be totally unbuffered. (equivalent to `python -u`)
# PYTHONHASHSEED: Enable hash randomization (equivalent to `python -R`)
# PYTHONDONTWRITEBYTECODE: Do not write byte files to disk, since we maintain it as readonly. (equivalent to `python -B`)
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1

VOLUME /data

RUN set -x \
    && mkdir /data && chmod 0777 /data \
    && apt-get -q update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
           git curl ssh ssh-askpass \
    && pip install celery flower[redis] redis GitPython ansible==2.9.* ansible-runner pathlib \
    && pip cache purge \
    && rm -rf /var/lib/apt/*

COPY . /app/

WORKDIR /app
USER nobody

CMD ["supervisord",  "-c", "supervisord.conf"]

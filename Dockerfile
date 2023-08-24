FROM python:3.9-slim AS build

# Copying requirements
COPY requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    " \
    && apt-get update \
    && apt-get install -y --no-install-recommends $BUILD_DEPS\
    && pip install --no-cache-dir -r /requirements.txt

#Building runtime image
FROM python:3.9-slim

# Copy generated site-packages from former stage:
COPY --from=build /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    libmagic1 \
    libpcre3 \
    mime-support \
    libpq-dev \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update \
    && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*


RUN useradd -rm -d /home/user -s /bin/bash -g root -G sudo -u 1000 user
USER user
# Creating working directory
RUN mkdir /home/user/app
WORKDIR /home/user/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /home/user/app

# os/gpu
FROM python:3.12-slim

# packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    git \
    build-essential \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    zlib1g-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    ca-certificates \
    tmux \
    locales \
    && apt-get clean

# locale
RUN apt-get install -y locales-all && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# user
ARG USER_NAME=container_user
ARG USER_ID=2000
ARG GROUP_ID=2000
ARG GROUP_NAME=worker

RUN groupadd -g ${GROUP_ID} ${GROUP_NAME} && \
    useradd -m -u ${USER_ID} -g ${GROUP_ID} -s /bin/bash ${USER_NAME} && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /workspace
RUN chown -R 0:${GROUP_ID} /workspace && \
    chmod -R 775 /workspace

USER ${USER_NAME}

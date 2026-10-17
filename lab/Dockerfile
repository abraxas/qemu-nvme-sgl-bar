# syntax=docker/dockerfile:1.7
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    QEMU_AUDIO_DRV=none

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bzip2 \
        ca-certificates \
        gcc \
        g++ \
        git \
        libfdt-dev \
        libglib2.0-dev \
        libpixman-1-dev \
        make \
        meson \
        ninja-build \
        pkg-config \
        python3 \
        python3-setuptools \
        python3-venv \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

ARG QEMU_PIN=4fc49f46dc95d4a27de2509e7fceb2931e91faeb
ARG QEMU_TAG=v11.1.2
WORKDIR /src
RUN set -eux; \
    ok=0; \
    for attempt in 1 2 3; do \
      if git clone --depth 1 --branch "${QEMU_TAG}" https://github.com/qemu/QEMU.git qemu; then \
        ok=1; \
        break; \
      fi; \
      rm -rf qemu; \
      sleep 8; \
    done; \
    test "${ok}" = 1; \
    cd qemu; \
    HEAD="$(git rev-parse HEAD)"; \
    case "${HEAD}" in \
      "${QEMU_PIN}"*) ;; \
      *) git fetch --depth 1 origin "${QEMU_PIN}"; git checkout "${QEMU_PIN}" ;; \
    esac; \
    grep -qx '11.1.2' VERSION
WORKDIR /src/qemu

RUN ./configure \
        --target-list=x86_64-softmmu \
        --prefix=/usr/local \
        --enable-asan \
        --enable-ubsan \
        --enable-fdt=system \
        --disable-docs \
        --disable-user \
        --disable-tools \
        --disable-guest-agent \
        --disable-slirp \
        --disable-sdl \
        --disable-gtk \
        --disable-curses \
        --disable-opengl \
        --disable-spice \
        --disable-werror \
        --disable-rust \
    && ninja -C build qemu-system-x86_64 \
    && install -m 0755 build/qemu-system-x86_64 /usr/local/bin/qemu-system-x86_64 \
    && mkdir -p /usr/local/share/qemu \
    && cp -a pc-bios/bios-256k.bin pc-bios/kvmvapic.bin /usr/local/share/qemu/ \
    && qemu-system-x86_64 --version \
    && rm -rf /src/qemu

COPY start-qemu.sh /opt/lab/start-qemu.sh
COPY trace-events.txt /opt/lab/trace-events.txt
RUN chmod 0755 /opt/lab/start-qemu.sh \
    && mkdir -p /work

WORKDIR /work
EXPOSE 18720
CMD ["/opt/lab/start-qemu.sh"]

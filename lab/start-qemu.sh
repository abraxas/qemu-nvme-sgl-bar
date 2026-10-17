#!/usr/bin/env bash
set -euo pipefail

WORK="${WORK_DIR:-/work}"
mkdir -p "${WORK}"
rm -f "${WORK}/qemu.rc" "${WORK}/qemu.log" "${WORK}/qemu.stderr"
: > "${WORK}/qemu.log"
: > "${WORK}/qemu.stderr"

# Zeroed LBA 0 so a spanning READ bounce writes CC.EN=0.
dd if=/dev/zero of="${WORK}/nvme.img" bs=1M count=1 status=none

export ASAN_OPTIONS="${ASAN_OPTIONS:-detect_leaks=0:abort_on_error=0:halt_on_error=0:log_path=${WORK}/asan}"
export UBSAN_OPTIONS="${UBSAN_OPTIONS:-print_stacktrace=1:halt_on_error=0}"

set +e
qemu-system-x86_64 \
  -name qemu-nvme-sgl-bar \
  -L /usr/local/share/qemu \
  -machine pc,accel=qtest \
  -m 128 \
  -display none \
  -vga none \
  -serial none \
  -monitor none \
  -audio none \
  -nodefaults \
  -nographic \
  -qtest tcp:0.0.0.0:18720,server=on,wait=off \
  -drive id=drv0,if=none,file="${WORK}/nvme.img",format=raw,cache=unsafe \
  -device nvme,drive=drv0,serial=sglbar,addr=04.0 \
  -trace events=/opt/lab/trace-events.txt \
  -d guest_errors \
  -D "${WORK}/qemu.log" \
  >>"${WORK}/qemu.stderr" 2>&1
rc=$?
set -e
echo "${rc}" > "${WORK}/qemu.rc"
# Keep the compose service up so poc.py can still read /work logs.
sleep infinity

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-qemu-nvme-sgl-bar}"
export PYTHONUNBUFFERED=1

LABEL="qemu-nvme-sgl-bar"
WITNESS="QEMU-NVME-SGL-BAR-WITNESS"
HOST_PORT="127.0.0.1:18720"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  exit 1
}

trap down EXIT

mkdir -p work
rm -f work/qemu.log work/qemu.stderr work/qemu.rc work/nvme.img work/asan.*

echo "== docker compose down (clean) =="
down

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 5); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 8
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait ${HOST_PORT} =="
ok=0
for i in $(seq 1 180); do
  if python3 - <<'PY'
import socket

sock = socket.socket()
sock.settimeout(2)
try:
    sock.connect(("127.0.0.1", 18720))
    sock.sendall(b"endianness\n")
    data = sock.recv(64)
except OSError:
    raise SystemExit(1)
finally:
    sock.close()
if not data.startswith(b"OK"):
    raise SystemExit(1)
raise SystemExit(0)
PY
  then
    ok=1
    echo "qtest-ready attempt=${i}"
    break
  fi
  echo "qtest-wait attempt=${i}"
  sleep 2
done
if [[ "${ok}" != 1 ]]; then
  echo "== compose logs (not ready) =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=160 || true
  echo "== work/qemu.stderr =="
  tail -n 160 work/qemu.stderr 2>/dev/null || true
  fail_setup "qtest-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"

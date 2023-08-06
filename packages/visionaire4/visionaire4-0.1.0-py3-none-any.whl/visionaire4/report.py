import argparse
import requests
import subprocess
import tarfile
import shutil
import logging
import docker
import time
import json
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
from pathlib import Path
from typing import List, Dict
from docker import DockerClient
from docker.models.containers import Container

from visionaire4.utils import (
    find_v4_container,
    find_vanilla_container,
    find_fremisn_container,
    fix_address,
)

logger = logging.getLogger()
V4_MIN_VERSION = 43301


class MarkdownGen:
    def __init__(self):
        super().__init__()
        self.doc = ""

    @classmethod
    def make_table(cls, header: List[str], data: List[List[str]]):
        # simply accepts matrix
        table = ""
        table += "|" + "|".join(header) + "|\n"
        table += "|" + "|".join(["---"] * len(header)) + "|\n"
        for rows in data:
            table += "|" + "|".join(rows) + "|\n"
        return table

    @classmethod
    def make_lists(cls, data: List[str]):
        lists = "\n".join(map(lambda s: f"- {s}", data))
        return lists

    @classmethod
    def make_image(cls, name: str, path: str, title=""):
        img = f'![{name}]({path} "{title}")'
        return img

    def write(self, texts: str):
        self.doc += f"{texts}\n"

    def add_title(self, title: str, texts=""):
        self.doc += f"# {title}\n"
        self.doc += f"{texts}\n"

    def add_section(self, title: str, texts=""):
        self.doc += f"## {title}\n"
        self.doc += f"{texts}\n"

    def add_subsection(self, title: str, texts=""):
        self.doc += f"### {title}\n"
        self.doc += f"{texts}\n"

    def add_pagebreak(self):
        self.doc += '\n<div style="page-break-after: always;"></div>\n\n'

    def save(self, output_filename: str):
        return Path(output_filename).write_text(self.doc)


def get_uname():
    result = subprocess.run(["uname", "-a"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")


def get_cpu_info():
    result = subprocess.run(["lscpu"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")


def get_os_info():
    result = subprocess.run(
        ["lsb_release", "-a"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")


def get_gpu_info(gpu_id=0):
    p = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=gpu_name,memory.total,clocks.max.sm,clocks.max.gr,driver_version,vbios_version",
            "--format=csv",
        ],
        stdout=subprocess.PIPE,
    )
    result = p.stdout.decode("utf-8")
    result = result.split("\n")[1:-1]

    if p.returncode != 0:
        return None, None

    if isinstance(gpu_id, int):
        gpu_id = [gpu_id] if gpu_id > -1 else list(range(len(result)))
    elif isinstance(gpu_id, list) and not all(isinstance(v, int) for v in gpu_id):
        raise ValueError(
            f"Invalid 'gpu_id', expect all member of the list to be an integer, got {gpu_id}."
        )
    elif not isinstance(gpu_id, list):
        raise ValueError(
            f"Invalid 'gpu_id', expected to be a list of integer or integer, got {type(gpu_id)}."
        )

    if any(v >= len(result) for v in gpu_id):
        raise ValueError(
            f"Only {len(result)} GPU(s) found, but 'gpu_id' got a value of '{max(gpu_id)}'"
        )

    head = [
        "GPU Name",
        "Total Memory",
        "Max Cuda Clock",
        "Max Graphic Clock",
        "Driver Version",
        "GPU BIOS Version",
    ]
    ret = {
        gid: "\n".join(
            f"{k:<20}: {v.strip()}" for k, v in zip(head, result[gid].split(","))
        )
        for gid in gpu_id
    }
    return ret, result


def get_vanilla_version(client: DockerClient, name: str = "") -> str:
    c = find_vanilla_container(client, name)
    if c is None:
        logger.warn("Vanilla Dashboard is not found")
        return "Not Found"

    versions = [t.split(":")[-1] for t in c.image.tags]
    if len(versions) == 0:
        logger.warn(
            f"Vanilla container ({c.name}) image tag is not found, unable to "
            "determine version."
        )
        return "Not Valid"
    return versions[0]


def get_fremisn_version(client: DockerClient, name: str = "") -> str:
    c = find_fremisn_container(client, name)
    if c is None:
        logger.warn("FRemisN Dashboard is not found")
        return "Not Found"

    versions = [t.split(":")[-1] for t in c.image.tags]
    if len(versions) == 0:
        logger.warn(
            f"FRemisN container ({c.name}) image tag is not found, unable to "
            "determine version."
        )
        return "Not Valid"
    return versions[0]


def get_v4_version(client: DockerClient, v4_addr: str, v4_name: str) -> str:
    v4_ver = None
    try:
        resp = requests.get(v4_addr, timeout=10)
        v4_ver: str = resp.json()["data"]["v4_version"]
        v4_ver = v4_ver.replace("v", "")
    except:
        # try to get version from container
        c = find_v4_container(client, v4_name, v4_addr)
        if c is None:
            logger.warn(
                f"Could not find any valid Visionaire4 instance in address {v4_addr} "
                f"or in container name '{v4_name}'. Make sure you have a running Visionaire4"
                "instance and set '--v4-address' or '--v4-name' properly."
            )
            return "Not Found"

        versions = [t.split(":")[-1] for t in c.image.tags]
        if len(versions) == 0:
            logger.warn(
                f"Visionaire4 container ({c.name}) image tag is not found, unable to "
                "determine version. Make Sure to run a valid visionaire4 image."
            )
            return "Not Valid"
        v4_ver = versions[0]
    return v4_ver


def prometheus_query_metrics(query, start, end, name, step=1) -> dict:
    url = "http://localhost:9090/api/v1/query_range"
    params = dict(query=query, start=start, end=end, step=step)

    try:
        resp = requests.get(url, params=params)
        rj = resp.json()
        if rj["status"] != "success" or resp.status_code != 200:
            raise RuntimeError("Error query response")
    except Exception as e:
        raise RuntimeError(
            "Failed to query prometheus, make sure prometheus server is running. msg: ",
            e,
        )

    service_cls_name_remove = (
        "visionaire::",
        ">",
        "<",
        "face_object_detection",
        "object_detection",
        "detection_batching",
        "lpr::",
    )

    data = dict()
    for r in rj["data"]["result"]:
        if isinstance(name, tuple):
            label = ":".join([str(r["metric"][n]) for n in name])
        elif name == "service_class_name":
            label = str(r["metric"][name])
            for x in service_cls_name_remove:
                label = label.replace(x, "")
        else:
            label = str(r["metric"][name])
        data[label] = np.array(
            [float(v[1]) if not np.isnan(float(v[1])) else 0 for v in r["values"]]
        )
    return data


def plot_prom_data(
    data: Dict[str, np.ndarray],
    title: str,
    fpath: Path,
    ylabel: str,
    divisor: int = 1,
    label: str = "{}",
    ylim_min=None,
    ylim_max=None,
) -> Path:
    if not data:
        return

    plt.cla()
    plt.clf()

    fig, (ax1, ax2) = plt.subplots(2)
    fig.set_size_inches((6.0, 9.0))

    for k, v in data.items():
        ax1.plot(v / divisor, label=label.format(k), linewidth=1)
    ax1.set(xlabel="time (s)", ylabel=ylabel)
    ax1.set_ylim(ylim_min, ylim_max)
    ax1.legend()
    ax1.set_title(title)

    ax2.boxplot(
        [d / divisor for d in data.values()],
        showfliers=False,
        showmeans=True,
        labels=[label.format(k) for k in data.keys()],
    )
    ax2.set_ylabel(ylabel)
    ax2.yaxis.grid(True)
    ax2.set_title(title)

    plt.autoscale()
    plt.tight_layout()
    plt.savefig(str(fpath))
    plt.close()
    return fpath


def prometheus_plot_all(out_dir, start, end, step=1):
    out_dir = Path(out_dir)
    queries_resource = {  # query, value label name, ylabel, divisor, legend label fmt, ylim_min
        "CPU Utilization": ("cpu_utils", "node_num", "utils (%)", 1, "node {}"),
        "CPU Memory": (
            "cpu_memory_used",
            "node_num",
            "memory (GB)",
            1e9,
            "node {}",
        ),
        "GPU Utilization": ("gpu_utils", "node_num", "utils (%)", 1, "node {}"),
        "GPU Memory": (
            "gpu_memory_used",
            "node_num",
            "memory (GB)",
            1e9,
            "node {}",
        ),
        "Service Invoke Latency": (
            'avg(pipeline_invoke_latency{quantile="0.500000"})by(service_class_name)',
            "service_class_name",
            "latency (ms)",
            1,
            "{}",
        ),
        "Analytic Dump Rate": (
            "sum(rate(event_dump_counter[30s])) by(node_num,analytic_id,stream_id)",
            ("node_num", "analytic_id", "stream_id"),
            "rate (event/s)",
            1,
            "{}",
        ),
        "Pipeline Load": (
            'avg by(node_num,analytic_id,stream_id) (pipeline_thread_load{quantile="0.500000"})',
            ("node_num", "analytic_id", "stream_id"),
            "load",
            1,
            "{}",
        ),
    }

    result = {}
    for k, v in queries_resource.items():
        data = prometheus_query_metrics(v[0], start, end, v[1], step)
        fpath = out_dir.joinpath("{}.png".format(k.lower().replace(" ", "_")))
        result[k] = plot_prom_data(data, k, fpath, v[2], v[3], v[4])
    plt.close("all")
    return result


def save_container_log(c: Container, fpath: Path, tail=1000):
    if c is None:
        return None
    fpath = Path(fpath)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    logs = c.logs(tail=tail).decode("utf-8")
    with open(fpath, "w") as f:
        f.write(logs)
    return fpath


def save_logs(src: Path, dst: Path, tail: int = 1000):
    src = Path(src)
    if not src.exists():
        logger.warn(f"Log to save in '{src}' is not found.")
        return

    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(["tail", "-n", f"{tail}", f"{src}"], stdout=subprocess.PIPE)
    result = p.stdout.decode("utf-8")
    with dst.open("w") as f:
        f.write(result)


def generate_container_info(c: Container, md: MarkdownGen, title: str):
    if c is None:
        return

    result = [
        "Arguments  \n```json\n{}\n```\n".format(json.dumps(c.attrs["Args"])),
        "Environment  \n```ini\n{}\n```\n".format("\n".join(c.attrs["Config"]["Env"])),
        "State  \n```json\n{}\n```\n".format(json.dumps(c.attrs["State"], indent=2)),
    ]
    list_md = md.make_lists(result)
    md.add_subsection(title, list_md)


def generate_report(args, client: DockerClient) -> str:
    dt = datetime.now()
    dt_str = dt.strftime("%Y%m%dT%H%M%SZ")

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    fdir = out_dir.joinpath(dt_str)
    log_dir = fdir.joinpath("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    plot_dir = fdir.joinpath("assets")
    plot_dir.mkdir(parents=True, exist_ok=True)

    v4_addr = fix_address(args.v4_address, "--v4-address")
    v4_ver = get_v4_version(client, v4_addr, args.v4_name)
    versions = [
        ["Visionaire4", v4_ver],
        ["FRemisN", get_fremisn_version(client, args.fr_name)],
        ["Vanilla Dashboard", get_vanilla_version(client)],
    ]

    v4_container = find_v4_container(client, v4_addr, args.v4_name)
    fremis_container = find_fremisn_container(client, args.fr_name)
    vanilla_container = find_vanilla_container(client, "")

    if v4_container is None and fremis_container is None:
        raise RuntimeError(
            "No Visionaire4 or FRemisN instance is found. Make sure you have Visionaire4 "
            "or FRemisN container running. You can also set the container name using "
            "'--v4-name' and '--fr-name'."
        )

    ## check v4 version
    if not v4_ver in ("Not Found", "Not Valid"):
        v4_ver = [int(v) for v in v4_ver.split(".")]
        v4_ver = sum([x * (10 ** (2 * n)) for n, x in enumerate(reversed(v4_ver))])
        if v4_ver < V4_MIN_VERSION:
            logger.warn(
                "You are running an old Visionaire4 version, some metrics (e.g. resources) "
                f"will not be available. Use Visionaire4 version higher than 4.33.01"
            )

    ## prometheus metrics
    prom_addr = fix_address(args.prom_address, "--prom-address")
    try:
        resp = requests.get(f"{prom_addr}/-/ready", timeout=5)
    except:
        prom_isready = False
    else:
        prom_isready = (resp.status_code == 200) and (
            resp.text.strip() == "Prometheus Server is Ready."
        )
    if prom_isready:
        end_query = time.time()
        start_query = end_query - args.range
        plot_result = prometheus_plot_all(plot_dir, start_query, end_query)
    else:
        plot_result = None
        logger.warn(
            f"Prometheus server in {prom_addr} is not responding. Possibly prometheus server "
            "is not running or incorrect address is set. Make sure to set the address properly "
            "with '--prom-address'."
        )

    ## save logs
    save_container_log(
        v4_container, log_dir.joinpath("visionaire4_logs.txt"), args.tail
    )
    save_container_log(
        fremis_container, log_dir.joinpath("fremisn_logs.txt"), args.tail
    )
    save_container_log(
        vanilla_container, log_dir.joinpath("vanilla_logs.txt"), args.tail
    )
    save_logs("/var/log/kern.log", log_dir.joinpath("kernlog.txt"), args.tail)
    save_logs("/var/log/syslog", log_dir.joinpath("syslog.txt"), args.tail)

    md = MarkdownGen()
    title = "Report - {}".format(dt.strftime("%Y/%m/%d %H:%M:%S"))
    md.add_title(title)

    gpu_info, gpu_raw = get_gpu_info(-1)
    if gpu_info is None:
        logger.warn(
            "Failed to get gpu information, you gpu driver might not be set properly "
            "or no gpu is available"
        )
    else:
        gpu_ver = gpu_raw[0].split(",")[4].strip()
        versions.append(["GPU Driver", gpu_ver])

    env_table = md.make_table(["component", "version"], versions)
    md.add_section("Versions", env_table)

    ## logs
    md.add_section("Container Status")
    generate_container_info(
        v4_container, md, "Visionaire4 ([logs](logs/visionaire4_logs.txt))"
    )
    generate_container_info(
        fremis_container, md, "FRemisN ([logs](logs/fremisn_logs.txt))"
    )
    generate_container_info(
        vanilla_container, md, "Vanilla ([logs](logs/vanilla_logs.txt))"
    )

    # environment
    environment = []
    if gpu_info is not None:
        gpu_info = "  \n".join(
            "\n  - GPU {}:\n<pre>\n{}\n</pre>".format(n, v.replace("\n", "  \n"))
            for n, v in gpu_info.items()
        )
        environment.append(
            "GPU info  \n\t{}\n".format(gpu_info),
        )
    environment.extend(
        [
            "Kernel info  \n<pre>\n{}</pre>\n".format(get_uname()),
            "OS info  \n<pre>\n{}</pre>\n".format(get_os_info().replace("\n", "  \n")),
            "CPU info  \n<pre>\n{}</pre>\n".format(
                get_cpu_info().replace("\n", "  \n")
            ),
        ]
    )
    env_list = md.make_lists(environment)
    md.add_section("Environment", env_list)
    md.add_pagebreak()

    if plot_result is None:
        md.add_section(
            "Metrics",
            f"Prometheus server is not running or invalid address ({prom_addr}) is set.",
        )
    else:
        md.add_section("Metrics")
        for n, p in plot_result.items():
            txt = md.make_image(n, p, n) if p else "Empty result."
            md.add_subsection(n, txt)
            if p:
                md.add_pagebreak()

    fpath = fdir.joinpath(f"report-{dt_str}.md")
    md.save(fpath)

    result_file = out_dir.joinpath(f"report-{dt_str}.tar.gz")
    tar = tarfile.open(result_file, "w:gz")
    for fp in fdir.iterdir():
        tar.add(fp, arcname=fp.name)
    tar.close()

    shutil.rmtree(fdir)
    return str(result_file)


def main(args):
    logger.info("Generating Visionaire4 status report.")

    client: DockerClient = docker.from_env()
    fpath = generate_report(args, client)
    logger.info(f"report saved to {fpath}")


def add_parser(subparser, parent_parser=None):
    parent_parser = [parent_parser] or []
    HELP = "Generate report for Visionaire4 status"
    parser: argparse.ArgumentParser = subparser.add_parser(
        "report",
        parents=parent_parser,
        help=HELP,
        description=HELP,
        usage="\n  visionaire4 report [options]",
    )
    parser.add_argument(
        "--out-dir",
        "-o",
        type=str,
        default="~/nodeflux/report",
        metavar="NAME",
        help="Report file output directory. Default: '~/nodeflux/report'",
    )
    parser.add_argument(
        "--v4-address",
        "-a",
        type=str,
        default="localhost:4004",
        metavar="HOST:PORT",
        help="Visionaire4 address. Expected format 'host:port'. "
        "Default: 'localhost:4004'",
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
        "--fr-name",
        type=str,
        default="fremisn",
        metavar="NAME",
        help="FRemisN container name. Default: 'fremisn'",
    )
    parser.add_argument(
        "--tail",
        "-n",
        type=int,
        default=1000,
        metavar="N",
        help="Number of lines of logs to save. Default: 1000",
    )
    parser.add_argument(
        "--range",
        "-r",
        type=int,
        default=300,
        metavar="N",
        help="last N seconds range to query prometheus metrics. Default: 300",
    )
    parser.set_defaults(func=main)

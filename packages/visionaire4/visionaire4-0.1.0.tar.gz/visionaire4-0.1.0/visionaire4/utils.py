from typing import Optional, Callable
from docker import DockerClient
from docker.models.containers import Container


def _port_forward_available(attrs, addr: str):
    split = addr.split(":")
    port = "9090" if len(split) < 2 else split[-1]
    valid = any(p.startswith(port) for p in attrs["NetworkSettings"]["Ports"])
    return valid


def _is_valid_v4_container(c: Container, v4_addr: str = "") -> bool:
    valid_env = any("SENTRY_ENVIRONMENT" in e for e in c.attrs["Config"]["Env"])
    valid_tag = any("nodefluxio/visionaire4" in t for t in c.image.tags)
    valid_port = _port_forward_available(c.attrs, v4_addr)
    valid = valid_env and valid_tag and (valid_port if v4_addr != "" else True)
    return valid


def _is_valid_prom_container(c: Container, prom_addr: str) -> bool:
    return _port_forward_available(c.attrs, prom_addr)


def _is_valid_vanilla_container(c: Container) -> bool:
    return c.attrs["Path"].endswith("vanend")


def _is_valid_fremisn_container(c: Container) -> bool:
    return c.attrs["Path"].endswith("fremis_n_app")


def _find_container(
    client: DockerClient, possible_name: str, check_fn: Callable, *args, **kwargs
) -> Optional[Container]:
    containers = client.containers.list()
    result = [c for c in containers if c.name == possible_name]
    if len(result) > 0:
        return result[0]

    ## name not found, use container attributes
    result = [c for c in containers if check_fn(c, *args, **kwargs)]
    if len(result) > 0:
        return result[0]
    return None


def find_v4_container(
    client: DockerClient, possible_name: str, v4_addr: str = ""
) -> Optional[Container]:
    return _find_container(client, possible_name, _is_valid_v4_container, v4_addr)


def find_prom_container(
    client: DockerClient, possible_name: str, prom_addr: str
) -> Optional[Container]:
    return _find_container(client, possible_name, _is_valid_prom_container, prom_addr)


def find_vanilla_container(
    client: DockerClient, possible_name: str
) -> Optional[Container]:
    return _find_container(client, possible_name, _is_valid_vanilla_container)


def find_fremisn_container(
    client: DockerClient, possible_name: str
) -> Optional[Container]:
    return _find_container(client, possible_name, _is_valid_fremisn_container)


def fix_address(addr: str, name: str) -> str:
    split = addr.split(":")
    if len(split) < 2:
        raise ValueError(
            f"address for '{name}' is not valid, expected format: "
            f"'host:port', got: '{addr}'."
        )
    if "://" not in addr:
        addr = "http://" + addr
    return addr

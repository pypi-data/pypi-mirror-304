#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/commands/pull.py
# VERSION:     0.1.0
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List, Set

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import DockerException
from rich import print as rich_print

### Local modules ###
from acqua.configs import BUILDS


@command
@option("--electrs", is_flag=True, help="Build acqua-electrs image", type=bool)
@option("--mainnet", is_flag=True, help="Build acqua-mainnet image", type=bool)
@option("--mariadb", is_flag=True, help="Build acqua-mariadb image", type=bool)
@option("--mempool", is_flag=True, help="Build acqua-mempool image", type=bool)
@option("--mutiny-web", is_flag=True, help="Build acqua-mutiny-web image", type=bool)
@option("--signet", is_flag=True, help="Build acqua-signet image", type=bool)
@option("--testnet", is_flag=True, help="Build acqua-testnet image", type=bool)
def pull(
  electrs: bool,
  mainnet: bool,
  mariadb: bool,
  mempool: bool,
  mutiny_web: bool,
  signet: bool,
  testnet: bool,
) -> None:
  """Pull core and peripheral images from GitHub container registry."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  image_names: List[str] = list(
    map(
      lambda image: image.tags[0].split(":")[0],
      filter(lambda image: len(image.tags) != 0, client.images.list()),
    )
  )
  pull_select: Dict[str, bool] = {
    "acqua-bitcoind": False,  # exclude base-image
    "acqua-electrs": electrs,
    "acqua-mainnet": mainnet,
    "acqua-mariadb": mariadb,
    "acqua-mempool": mempool,
    "acqua-mutiny-web": mutiny_web,
    "acqua-signet": signet,
    "acqua-testnet": testnet,
  }

  ### Checks if specified images had been built previously ###
  outputs: List[str] = []
  built: Set[str] = {tag for tag in BUILDS.keys() if pull_select[tag] and tag in image_names}
  outputs += map(lambda tag: f"<Image: '{tag}'> already exists in local docker images.", built)
  list(map(rich_print, outputs))


__all__ = ("pull",)

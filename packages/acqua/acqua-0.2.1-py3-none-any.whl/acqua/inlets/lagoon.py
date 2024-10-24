#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/inlets/lagoon.py
# VERSION:     0.1.0
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import ClassVar, List

### Third-party packages ###
from blessed import Terminal
from blessed.keyboard import Keystroke
from docker.models.containers import Container
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

### Local modules ###
from acqua.inlets.estuary import Estuary


class Lagoon(BaseModel):
  model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)  # type: ignore[misc]
  container_index: StrictInt = 0
  container_names: List[StrictStr] = []
  containers: List[Container] = []

  ### Split layouts ###
  body: ClassVar[Layout] = Layout(name="body", minimum_size=4, ratio=8, size=17)
  straits: ClassVar[Layout] = Layout(name="straits", size=20)
  footer: ClassVar[Layout] = Layout(name="footer", size=3)
  main: ClassVar[Layout] = Layout(size=72)
  pane: ClassVar[Layout] = Layout()
  sidebar: ClassVar[Layout] = Layout(size=24)
  estuary: ClassVar[Estuary] = Estuary(height=16, width=72)

  ### Terminal ###
  terminal: ClassVar[Terminal] = Terminal()

  def model_post_init(self, _) -> None:  # type: ignore[no-untyped-def]
    if len(self.container_names) == 0:
      self.container_names.append("sample")
    self.pane.split_row(self.sidebar, self.main)
    self.main.split_column(self.body, self.footer)
    self.sidebar.split_column(self.straits)

  def display(self) -> None:
    with self.terminal.cbreak(), self.terminal.hidden_cursor(), Live(
      self.pane, refresh_per_second=4, transient=True
    ):
      try:
        while True:
          container_name: str = self.container_names[self.container_index]
          ### Process input key ###
          keystroke: Keystroke = self.terminal.inkey(timeout=0.25)
          if keystroke.code == self.terminal.KEY_UP and self.container_index > 0:
            self.container_index -= 1
          elif (
            keystroke.code == self.terminal.KEY_DOWN
            and self.container_index < len(self.container_names) - 1
          ):
            self.container_index += 1
          elif keystroke in {"Q", "q"}:
            raise StopIteration

          container_rows: str = ""
          if self.container_index > 0:
            container_rows = "\n".join(self.container_names[: self.container_index])
            container_rows += f"\n[reverse]{self.container_names[self.container_index]}[reset]\n"
          else:
            ...
          if self.container_index < len(self.container_names) - 1:
            container_rows += "\n".join(self.container_names[self.container_index + 1 :])
          self.pane["straits"].update(Panel(container_rows, title="straits"))

          body_table: Table = Table(expand=True, show_lines=True)
          body_table.add_column(container_name, "dark_sea_green bold")
          body_table.add_row(self.estuary.renderable)
          self.pane["body"].update(body_table)

          self.pane["footer"].update(
            Panel(
              Text.assemble(
                "Select:".rjust(16),
                (" ↑↓ ", "bright_magenta bold"),
                " " * 16,
                "Exit:".rjust(16),
                ("  Q ", "red bold"),
              )
            )
          )
      except StopIteration:
        print("If you cling to life, you live in fear of death.")


__all__ = ("Lagoon",)

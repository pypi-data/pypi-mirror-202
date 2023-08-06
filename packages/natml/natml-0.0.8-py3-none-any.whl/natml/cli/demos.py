# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from dataclasses import asdict
from pathlib import Path
from rich import print, print_json
from typer import Argument, Option, Typer

from .misc import create_learn_callback

app = Typer(no_args_is_help=True)

@app.command(name="upload", help="Upload a Unity WebGL predictor demo to NatML.") # INCOMPLETE
def upload_demo (
    path: Path=Option(None, help="Unity WebGL build directory.")
) -> None:
    pass

@app.command(name="open", help="Open a Unity WebGL predictor demo.") # INCOMPLETE
def opne_demo (
    tag: str=Argument(..., help="Predictor tag.")
) -> None:
    pass

@app.callback()
def endpoint_options (
    learn: bool = Option(None, "--learn", callback=create_learn_callback("https://docs.natml.ai/graph/demos/type"), help="Learn about predictor demos in NatML.")
):
    pass
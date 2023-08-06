from pathlib import Path
from typing import Tuple

import healpy as hp
import matplotlib.pyplot as plt
import typer

app = typer.Typer()


@app.command()
def plot_map(
    filename: Path = typer.Argument(..., help="Name of HEALPIX fits file"),
    field: int = typer.Option(0, help="Column to read. 0 is I, 1 is Q, and 2 is U"),
    norm: str = typer.Option(None, help="Normalization method"),
    min: float = typer.Option(None, help="Minimum value"),
    max: float = typer.Option(None, help="Maximum value"),
    coord: Tuple[str, str] = typer.Option((None, None), help="Coordinate system"),
    unit: str = typer.Option(None, help="Unit"),
    nest: bool = typer.Option(False, help="Use NESTED pixel ordering"),
    title: str = typer.Option("", help="Title"),
    xsize: int = typer.Option(800, help="Size of the figure"),
    notext: bool = typer.Option(False, help="Do not show text"),
    cmap: str = typer.Option(None, help="Color map"),
    cbar: bool = typer.Option(True, help="Show color bar"),
    save: bool = typer.Option(False, help="Save the figure"),
    remove_dip: bool = typer.Option(False, help="Remove the dipole"),
    gal_cut: float = typer.Option(
        None,
        help="Symmetric galactic cut for the dipole/monopole fit. Removes points in latitude range [-gal_cut, +gal_cut]",
    ),
    remove_mono: bool = typer.Option(False, help="Remove the monopole"),
    badcolor: str = typer.Option("gray", help="Color of bad pixels"),
) -> None:
    """Plots a HEALPix map from the commandline given a fits file."""

    if not filename.exists():
        msg = f"{filename} was not found"
        raise FileNotFoundError(msg)

    m = hp.read_map(filename, field=field, nest=nest)
    hp.mollview(
        m,
        norm=norm,
        min=min,
        max=max,
        coord=None if coord == (None, None) else coord,
        cmap=cmap,
        unit=unit,
        title=title,
        nest=nest,
        xsize=xsize,
        cbar=cbar,
        notext=notext,
        remove_dip=remove_dip,
        remove_mono=remove_mono,
        badcolor=badcolor,
        gal_cut=gal_cut,
    )
    if save:
        plt.savefig(filename.with_suffix(".png"))
    plt.show()

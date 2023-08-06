[![PyPI version](https://badge.fury.io/py/mollview.svg)](https://badge.fury.io/py/mollview)
![Tests](https://github.com/MetinSa/mollview/actions/workflows/tests.yml/badge.svg)
---


`mollview` is a command line tool for plotting HEALPix maps from fits files. `mollview` wraps `healpy`'s `read_map` and `mollview` functions. Most `mollview` keywords are supported (see [the documentation for mollview](https://healpy.readthedocs.io/en/latest/generated/healpy.visufunc.mollview.html) for more information).

# Installation
`pip install mollview`.

# Examples
```bash
>>> mollview my_map.fits

>>> python -m mollview my_map.fits
```
```bash
>>> mollview --help                           
Usage: mollview [OPTIONS] FILENAME

  Plots a HEALPix map from the commandline given a fits file.

Arguments:
  FILENAME  Name of HEALPIX fits file  [required]

Options:
  --field INTEGER                 Column to read. 0 is I, 1 is Q, and 2 is U
                                  [default: 0]
  --min FLOAT                     Minimum value
  --max FLOAT                     Maximum value
  --norm TEXT                     Normalization method
  --cmap TEXT                     Color map
  --unit TEXT                     Unit
  --title TEXT                    Title
  --save / --no-save              Save the figure  [default: no-save]
  --coord <TEXT TEXT>...          Coordinate system  [default: None, None]
  --cbar / --no-cbar              Show color bar  [default: cbar]
  --notext / --no-notext          Do not show text  [default: no-notext]
  --xsize INTEGER                 Size of the figure  [default: 800]
  --nest / --no-nest              Use NESTED pixel ordering  [default: no-
                                  nest]
  --remove-dip / --no-remove-dip  Remove the dipole  [default: no-remove-dip]
  --gal-cut FLOAT                 Symmetric galactic cut for the
                                  dipole/monopole fit. Removes points in
                                  latitude range [-gal_cut, +gal_cut]
  --remove-mono / --no-remove-mono
                                  Remove the monopole  [default: no-remove-
                                  mono]
  --badcolor TEXT                 Color of bad pixels  [default: gray]
  --help                          Show this message and exit
```
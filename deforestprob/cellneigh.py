#!/usr/bin/python

# ==============================================================================
# author          :Ghislain Vieilledent
# email           :ghislain.vieilledent@cirad.fr, ghislainv@gmail.com
# web             :https://ghislainv.github.io
# python_version  :2.7
# license         :GPLv3
# ==============================================================================

# Import
import numpy as np
import sys
from osgeo import gdal


# cellneigh
def cellneigh(raster=None, region=None, csize=10, rank=1):
    """
    Compute number of spatial cells and neighbours.

    :param raster: Path to raster file to compute region.
    :param region: List/tuple of region coordinates (east, west, south, north).
    :param csize: Spatial cell size (in km).
    :param rank: Rank of the neighborhood (1 for chess king's move).
    :return: List of length 2 with number of neighbours for each cell \
    and adjacent cells.
    """

    # Region
    if raster is not None:
        r = gdal.Open(raster)
        ncol = r.RasterXSize
        nrow = r.RasterYSize
        gt = r.GetGeoTransform()
        Xmin = gt[0]
        Xmax = gt[0] + gt[1] * ncol
        Ymin = gt[3] + gt[5] * nrow
        Ymax = gt[3]
    elif region is not None:
        Xmin = region[0]
        Xmax = region[1]
        Ymin = region[2]
        Ymax = region[3]
    else:
        print("raster or region must be specified")
        sys.exit(1)

    # Cell number from region
    csize = csize
    print("Compute number of %d x %d km spatial cells" % (csize, csize))
    csize = csize * 1000  # Transform km in m
    ncell_byrow = np.int(np.ceil((Xmax - Xmin) / csize))
    ncell_bycol = np.int(np.ceil((Ymax - Ymin) / csize))
    ncell = ncell_byrow * ncell_bycol
    print("... %d cells (%d x %d)" % (ncell, ncell_bycol, ncell_byrow))

    # Adjacent cells and number of neighbors
    print("Identify adjacent cells and compute number of neighbors")
    nneigh = []
    adj = []
    around = np.arange(-rank, rank + 1)
    for i in range(ncell_bycol):
        for j in range(ncell_byrow):
            I = i + around
            Iprim = I[(I >= 0) & (I < ncell_bycol)]
            J = j + around
            Jprim = J[(J >= 0) & (J < ncell_byrow)]
            # Disregard the center cell
            nneigh.append(len(Iprim) * len(Jprim) - 1)
            for cy in Iprim:
                for cx in Jprim:
                    if not (cy == i and cx == j):
                        adj.append(cy * ncell_byrow + cx)
    nneigh = np.array(nneigh)
    adj = np.array(adj)

    return(nneigh, adj)

# End

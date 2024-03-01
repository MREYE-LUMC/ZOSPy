# -*- coding: utf-8 -*-

from __future__ import annotations

from zospy.analyses.base import Analysis as anabase
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem
import matplotlib as mpl

class MTF(anabase):
    """Virtual base class for all MTF analysis classes."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ToDo
        # add initializations common to all MTFs here

class FFT_MTF(MTF):
    """Class representing the FFT MTF """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._typeconst = constants.Analysis.AnalysisIDM.FftMtf
        os_colors=['blue', 'lime', 'red', 'olive', 'magenta', 'cyan', 'slateblue'] 

class FFT_MTF_MAP(MTF):
    """Class representing the FFT MTF Map- Window"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._typeconst = constants.Analysis.AnalysisIDM.FftMtfMap

    @property
    def os_color_map(self):
        """a colormat to be used by matplotlib.pyplot.pcolormesh or matplotlib.pyplot.contourf
        mimicking OpticStudios "False Color" colormap"""
        cdict = {'red':   [[0.0,  0.17, 0.17],
                   [0.2, 0., 0.],
                   [0.4,  0.3, 0.3],
                   [0.6,  0.75, 0.75],
                   [0.8,  0.94, 0.94],
                   [0.9,  0.94, 0.94],
                   [1.0,  0.75, 0.75]],
         'green': [[0.0,  0.08, 0.08],
                   [0.2,  0.75, 0.75],
                   [0.4,  1.0, 1.0],
                   [0.6,  1., 1.],
                   [0.8,  .62, .62],
                   [0.9,  0.0, 0.0],
                   [1.0,  0.0, 0.0]],
         'blue':  [[0.0,  0.78, 0.78],
                   [0.2, 0.67, 0.67],
                   [0.4,  0.0, 0.0],
                   [0.6,  0., 0.],
                   [1.0,  0.0, 0.0]]}
        oscmp = mpl.colors.LinearSegmentedColormap('testCmap', segmentdata=cdict, N=256)
        return(oscmp)

    @property
    def cmap_norm(self):
        """a matplotlib.colors.Normalize object to be used by
        matplotlib.pyplot.pcolormesh or matplotlib.pyplot.contourf 
        Optic Studio leaves the scale fixed to [0, 1.0], acutally _not_ normalizing.
        This matplotlib.colors.Normalize - object does exactly that to mimic the behaviour
        of Optic Studio"""
        return(mpl.colors.Normalize(0., 1.)) 

    def make_norm(self, min=0., max=1.):
        """create a matplotlib.colors.Normalize object to be used by
        matplotlib.pyplot.pcolormesh or matplotlib.pyplot.contourf 
        normalizing the colors to mix an max values
        Parameters
        ----------
        min: float
            value representing the low end of the color scale
        max: float
            value representing the upper end of the color scale"""
        return(mpl.colors.Normalize(min, max))




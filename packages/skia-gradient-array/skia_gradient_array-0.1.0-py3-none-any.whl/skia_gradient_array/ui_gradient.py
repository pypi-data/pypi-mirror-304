import pkg_resources

import json
import numpy as np
from skia_gradient_array import GradientCanvas, Stops
from matplotlib.colors import to_rgb

# We import collection of gradient definition from uiGradients?

# https://github.com/Ghosh/uiGradients


class UiGradient:
    def __init__(self, json_name=None):
        if json_name is None:
            json_name = pkg_resources.resource_filename(__name__,
                                                        'data/ui-gradients.json')

        j = json.load(open(json_name))
        self._jd = dict((j1["name"], j1["colors"]) for j1 in j)

    def available_keys(self):
        return self._jd.keys()

    def get_stops(self, n):
        colors = [to_rgb(c) for c in self._jd[n]]
        offsets = np.linspace(0, 1, len(colors))
        stops = Stops.from_offsets_colors(offsets, colors)
        return stops

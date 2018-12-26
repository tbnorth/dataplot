"""
dataplot.py - wrapper for separated data / plot pipeline

Terry N. Brown terrynbrown@gmail.com Wed Dec 26 13:39:01 EST 2018
"""

import os
import json
import time

import matplotlib as mpl

mpl.rc('font', family='DejaVu Sans, Arial')
mpl.rcParams['lines.solid_joinstyle'] = 'bevel'
mpl.use('SVG')
from matplotlib import pyplot as plt


class DataPlot(object):

    """Separated data / plotting stages."""

    def __init__(self, name):
        """setup

        Args:
            name (str): name of plot
        """
        self.name = name
        self._ds = self.init_ds()

    def _path(self, path, name, format):
        """Calculate path for format, creates dirs. as needed

        Args:
            path (str): path to save to
            name (str): filename for save
            format (str): file extension
        """
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, "%s.%s" % (name, format))

    def ds(self):
        """Get data container for this plot
        Returns: dict

        """
        return self._ds

    def init_ds(self):
        """Setup data structure"""
        return {
            # author info. etc.
            '_metadata': {
                'generated': time.asctime(),
                # a pointer to this class, to explain JSON format
                'relation': "https://github.com/tbnorth/dataplot",
            },
            # general plot data, title, x label, etc.
            'ax': {'x': {}, 'y': {}},
            'ds': {},  # x, y, etc., lists of the same length
            'kv': {},  # arbitrary key / value info.
        }

    def save_plot(self, builder=None, path=None, formats=None, name=None):
        """Plot the data

        Kwargs:
            builder (func): something that builds a figure given self.ds()
            path (str): path to save figures
            formats (list): formats, incl. `show`, `asis`, and `json`
                `show` shows the plot interactively, `json` saves the
                plot data, and `asis` gets the format from name without
                appending anything.
            name (str): override self.name
        """
        path = path or '.'
        formats = formats or ['show']
        name = name or self.name
        if builder and formats != ['json']:  # not needed for JSON by itself
            builder(self.ds())
        for format in formats:
            if format == 'show':  # after saving all other formats
                continue
            if format == 'json':
                with open(self._path(path, name, format), 'wb') as out:
                    json.dump(self.ds(), out, indent=1, sort_keys=True)
            else:
                fullpath = self._path(path, name, format)
                if format == 'asis':  # cut off '.asis' to get supplied name
                    fullpath = fullpath[:-5]
                plt.savefig(fullpath)
        if 'show' in formats:
            plt.show()


def main():
    """test / demo"""

    dp = DataPlot('fred')

    def make_data(ds):
        """make demo data - updates ds"""
        ds['_metadata'].update(
            {
                'creator': "Terry N. Brown, terrynbrown@gmail.com",
                'description': "Demo data for DataPlot class",
            }
        )
        ds['ds']['x'] = list(range(10))
        ds['ds']['y'] = [i % 3 for i in range(10)]
        ds['kv']['r2'] = 0.2
        ds['ax']['x']['title'] = 'X units'
        ds['ax']['title'] = 'The Plot'

    def plot_data(ds):
        """plot demp data"""
        plt.plot(ds['ds']['x'], ds['ds']['y'])
        plt.xlabel(ds['ax']['x']['title'])
        plt.title(ds['ax']['title'])
        plt.text(0, 1.5, "$r^2=%s$" % ds['kv']['r2'])

    make_data(dp.ds())
    dp.save_plot(
        plot_data, path="tests/output", formats=('png', 'pdf', 'json')
    )


if __name__ == "__main__":
    main()

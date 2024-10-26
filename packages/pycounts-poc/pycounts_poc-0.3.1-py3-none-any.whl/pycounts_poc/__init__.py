# read version from installed package
from importlib.metadata import version
__version__ = version("pycounts_poc")

# populate package namespace
from pycounts_poc.pycounts_poc import count_words
from pycounts_poc.plotting import plot_words

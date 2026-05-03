"""
Common setup for individual table scripts: init Stata, load data, format LaTeX.
"""
import os
import sys
import pandas as pd

# Ensure Analysis/ is on sys.path so `from shared.X import Y` works
_analysis_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _analysis_dir not in sys.path:
    sys.path.insert(0, _analysis_dir)

from shared.paths import tables_dir, data_dir
from shared.stata_setup import init_stata
from shared.latex_utils import format_latex

_DATA_PATH = None
_stata = None


def get_stata():
    """Return the pystata stata module, initializing on first call."""
    global _stata
    if _stata is None:
        _stata = init_stata()
    return _stata


def get_data_path():
    """Return the local path to df4m_w.csv."""
    global _DATA_PATH
    if _DATA_PATH is None:
        _DATA_PATH = os.path.join(data_dir, "df4m_w.csv")
    return _DATA_PATH


def load_data():
    """Load df4m_w.csv into Stata and encode regno."""
    stata = get_stata()
    df = pd.read_csv(get_data_path(), low_memory=False)
    stata.pdataframe_to_data(df, force=True)
    stata.run("encode regno, gen(regno_id)", quietly=True)
    return stata


os.makedirs(tables_dir, exist_ok=True)

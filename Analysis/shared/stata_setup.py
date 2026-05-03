"""
Initialize Stata via pystata and optionally install Stata packages.
"""
import os
import platform
import time


def init_stata(install_packages=False):
    """
    Configure and return the pystata stata module.

    Parameters
    ----------
    install_packages : bool
        If True, install required Stata packages (estout, reghdfe, etc.).
        Only needed on first run or after a Stata reinstall.
    """
    if platform.system() == 'Darwin':
        stata_dir = '/Applications/Stata/'
        edition = 'se'
        if not os.path.isdir(stata_dir):
            raise FileNotFoundError(
                'Stata not found at /Applications/Stata/. Please install Stata SE for macOS.'
            )
    else:
        stata_dir = '/usr/local/stata'
        edition = 'se'
        if not os.path.isdir(stata_dir):
            raise FileNotFoundError(
                f'Stata not found at {stata_dir}. Run setup_environment.py first.'
            )

    import stata_setup
    stata_setup.config(stata_dir, edition, splash=False)
    from pystata import stata

    if install_packages:
        packages = ['estout', 'require', 'reghdfe', 'ftools', 'outreg2',
                     'coefplot', 'ppmlhdfe']
        for pkg in packages:
            try:
                stata.run(f'cap which {pkg}', quietly=True)
                stata.run(f'if _rc != 0 ssc install {pkg}', quietly=True)
            except Exception as e:
                print(f'Note: {pkg} install returned: {e}')

    return stata

#!/usr/bin/env python3
"""
One-time environment setup.

Creates a virtual environment, installs required Python packages, and
installs required Stata packages. Stata itself must already be installed:
  - macOS: /Applications/Stata/
  - Linux: /usr/local/stata/

Usage:
    python3 setup_environment.py

After setup, run the analysis with:
    .venv/bin/python3 Analysis/run_all.py --tables
"""

import os
import sys
import platform
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_ROOT, ".venv")

PYTHON_PACKAGES = ["pandas", "numpy", "openpyxl", "stata_setup"]

STATA_PACKAGES = ["estout", "ftools", "reghdfe", "outreg2", "ppmlhdfe"]

if platform.system() == "Darwin":
    STATA_DIR = "/Applications/Stata/"
    # Prefer Homebrew Python 3.12 on macOS; fall back to whatever is running this script
    PYTHON_EXEC = (
        "/opt/homebrew/bin/python3.12"
        if os.path.isfile("/opt/homebrew/bin/python3.12")
        else sys.executable
    )
else:
    STATA_DIR = "/usr/local/stata"
    PYTHON_EXEC = sys.executable

STATA_EDITION = "se"
STATA_UTILITIES = os.path.join(STATA_DIR, "utilities")


def get_venv_python():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python3")


def step_venv():
    venv_python = get_venv_python()
    if os.path.isfile(venv_python):
        print("[1/3] Virtual environment: already exists")
    else:
        print(f"[1/3] Creating virtual environment at {VENV_DIR} ...")
        subprocess.run([PYTHON_EXEC, "-m", "venv", VENV_DIR], check=True)
        print("      Done.")

    # Add Stata utilities to the venv's sys.path via a .pth file so that
    # pystata's sfi module is importable (required on macOS).
    if os.path.isdir(STATA_UTILITIES):
        import glob
        site_pkgs = glob.glob(os.path.join(VENV_DIR, "lib", "python*", "site-packages"))
        if site_pkgs:
            pth_file = os.path.join(site_pkgs[0], "stata.pth")
            if not os.path.isfile(pth_file):
                with open(pth_file, "w") as f:
                    f.write(STATA_UTILITIES + "\n")
                print(f"      Added Stata utilities to venv path ({pth_file})")


def step_python_packages():
    venv_python = get_venv_python()
    missing = []
    for pkg in PYTHON_PACKAGES:
        result = subprocess.run(
            [venv_python, "-c", f"import {pkg.replace('-', '_')}"],
            capture_output=True,
        )
        if result.returncode != 0:
            missing.append(pkg)

    if not missing:
        print("[2/3] Python packages: already installed")
        return

    print(f"[2/3] Installing Python packages: {', '.join(missing)} ...")
    subprocess.run(
        [venv_python, "-m", "pip", "install", "--upgrade", "pip"],
        capture_output=True,
    )
    subprocess.run(
        [venv_python, "-m", "pip", "install"] + missing,
        check=True,
    )
    print("      Done.")


def step_stata_packages():
    if not os.path.isdir(STATA_DIR):
        print(f"[3/3] Stata not found at {STATA_DIR} — skipping Stata package install.")
        print("      Install Stata and re-run this script to complete setup.")
        return

    print("[3/3] Installing Stata packages ...")
    venv_python = get_venv_python()
    script = f"""
import stata_setup
stata_setup.config({STATA_DIR!r}, {STATA_EDITION!r}, splash=False)
from pystata import stata
packages = {STATA_PACKAGES!r}
for pkg in packages:
    stata.run(f'cap which {{pkg}}', quietly=True)
    stata.run(f'if _rc != 0 ssc install {{pkg}}, replace', quietly=True)
    print(f'  {{pkg}}: OK')
"""
    subprocess.run([venv_python, "-c", script], check=True)
    print("      Done.")


def main():
    if not os.path.isdir(STATA_DIR):
        print(f"WARNING: Stata not found at {STATA_DIR}.")
        print("Install Stata SE and re-run this script.\n")

    step_venv()
    step_python_packages()
    step_stata_packages()

    venv_python = get_venv_python()
    print(f"""
Setup complete. Run the analysis with:
    {venv_python} Analysis/run_all.py --tables
""")


if __name__ == "__main__":
    main()

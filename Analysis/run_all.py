"""
Run all tables in sequence.

Usage:
    python Analysis/run_all.py            # run everything
    python Analysis/run_all.py --tables   # tables only
    python Analysis/run_all.py --data     # prepare data only

Each script can also be run individually, e.g.:
    python Analysis/tables/excess_adj_full_sample.py
"""
import sys, os, subprocess, argparse, time

_dir = os.path.dirname(os.path.abspath(__file__))


def run(script_path, label):
    rel = os.path.relpath(script_path)
    print(f"\n{'='*60}")
    print(f"  Running: {rel}")
    print(f"{'='*60}")
    t0 = time.time()
    result = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(_dir))
    elapsed = time.time() - t0
    status = "OK" if result.returncode == 0 else f"FAILED (code {result.returncode})"
    print(f"  {label}: {status}  ({elapsed:.0f}s)")
    return result.returncode == 0


TABLE_SCRIPTS = [
    (os.path.join(_dir, 'tables', 'sample_design.py'),              'sampleDesign.tex'),
    (os.path.join(_dir, 'tables', 'descriptive_stats.py'),          'descriptive_stats.tex'),
    (os.path.join(_dir, 'tables', 'descriptive_stats_by_audit.py'), 'descriptive_stats_by_audit.tex'),
    (os.path.join(_dir, 'tables', 'excess_adj_full_sample.py'),     'excess_adj_full_sample.tex'),
    (os.path.join(_dir, 'tables', 'alternative_dvs.py'),            'alternative_dvs.tex'),
    (os.path.join(_dir, 'tables', 'face_vs_notes.py'),              'face_vs_notes.tex'),
    (os.path.join(_dir, 'tables', 'procs.py'),                      'procs.tex'),
    (os.path.join(_dir, 'tables', 'value_rel.py'),                  'value_rel.tex'),
]


def main():
    parser = argparse.ArgumentParser(description='Run all analysis scripts.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--tables', action='store_true', help='Run table scripts only')
    group.add_argument('--data',   action='store_true', help='Run data preparation only')
    args = parser.parse_args()

    scripts = []
    if args.data:
        scripts = [(os.path.join(_dir, 'prepare_data.py'), 'prepare_data')]
    elif args.tables:
        scripts = TABLE_SCRIPTS
    else:
        scripts = [(os.path.join(_dir, 'prepare_data.py'), 'prepare_data')] + TABLE_SCRIPTS

    failures = []
    t_start = time.time()

    for script_path, label in scripts:
        ok = run(script_path, label)
        if not ok:
            failures.append(label)

    total = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"  Finished in {total/60:.1f} min")
    if failures:
        print(f"  FAILED: {', '.join(failures)}")
        sys.exit(1)
    else:
        print("  All scripts completed successfully.")


if __name__ == '__main__':
    main()

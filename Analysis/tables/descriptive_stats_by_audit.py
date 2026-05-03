"""Table 2 Panel B: descriptive_stats_by_audit.tex — Stats split by audited indicator."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.table_helpers import load_data, tables_dir, format_latex


def main():
    stata = load_data()
    stata.run(
        "estpost summarize epsincon_usd street_adj_usd_ps ngm_adj_usd_ps "
        "mgmt_excess_actual if audited == 0",
        quietly=True,
    )
    stata.run("est store Unaudited", quietly=True)

    stata.run(
        "estpost summarize epsincon_usd street_adj_usd_ps ngm_adj_usd_ps "
        "mgmt_excess_actual if audited == 1",
        quietly=True,
    )
    stata.run("est store Audited", quietly=True)

    stata.run(
        "estpost ttest epsincon_usd street_adj_usd_ps ngm_adj_usd_ps "
        "mgmt_excess_actual, by(audited)",
        quietly=True,
    )
    stata.run("est store Diff", quietly=True)

    out = os.path.join(tables_dir, "descriptive_stats_by_audit.tex")
    stata.run(
        f'esttab Unaudited Audited Diff using "{out}", '
        "replace label "
        'cells("mean(pattern(1 1 0) fmt(3)) b(pattern(0 0 1) star fmt(3))") '
        "booktabs nogaps "
        'mtitles("Audited = 0" "Audited = 1" "Difference") '
        "nonumbers nonotes collabels(none) "
        'stats(N, fmt(0) labels("Observations"))',
        quietly=True,
    )
    format_latex(out)
    print("  -> descriptive_stats_by_audit.tex")


if __name__ == "__main__":
    main()

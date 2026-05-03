"""Table 2 Panel A: descriptive_stats.tex — Summary statistics, full sample."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.table_helpers import load_data, tables_dir, format_latex


def main():
    stata = load_data()
    stata.run(
        "estpost summarize epsincon_usd street_adj_usd_ps ngm_adj_usd_ps "
        "mgmt_excess_actual loss_to_profit neg audited in_income_statement "
        "in_notes non_gaap_is_kam most_prom no_ngm no_kams at_usd_ln loss "
        "btm growth_revt vol anne_proc_substantive anne_proc_classification "
        "anne_proc_consist_mgmt_pol anne_proc_consist_stds "
        "anne_proc_consist_past anne_proc_adequacy_disc, detail",
        quietly=True,
    )
    out = os.path.join(tables_dir, "descriptive_stats.tex")
    stata.run(
        f'esttab using "{out}", '
        "replace label "
        'cells("mean(fmt(3)) sd(fmt(3)) p25(fmt(3)) p50(fmt(3)) p75(fmt(3))") '
        "booktabs nogaps nomtitles nonumbers nonotes",
        quietly=True,
    )
    format_latex(out)
    print("  -> descriptive_stats.tex")


if __name__ == "__main__":
    main()

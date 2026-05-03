"""Table 5: face_vs_notes.tex — Income statement vs notes disclosure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.table_helpers import load_data, tables_dir, format_latex


def main():
    stata = load_data()

    # Col 1: in_income_statement == 0
    stata.run(
        "reghdfe mgmt_excess_actual audited epsincon_usd most_prom "
        "non_gaap_is_kam no_ngm no_kams at_usd_ln loss btm growth_revt vol "
        "if in_income_statement == 0, "
        "absorb(regno_id#year) vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "F*Y"', quietly=True)
    stata.run("est store a1", quietly=True)

    # Col 2: full sample, separate coefficients
    stata.run(
        "reghdfe mgmt_excess_actual in_notes in_income_statement "
        "epsincon_usd most_prom non_gaap_is_kam no_ngm no_kams at_usd_ln "
        "loss btm growth_revt vol, "
        "absorb(regno_id#year) vce(cluster regno)",
        quietly=True,
    )
    stata.run('estadd local FES "F*Y"', quietly=True)
    stata.run("est store a3", quietly=True)

    out = os.path.join(tables_dir, "face_vs_notes.tex")
    stata.run(
        f'esttab a1 a3 using "{out}", '
        "replace label b(%9.3f) se(%9.3f) "
        "star(* 0.10 ** 0.05 *** 0.01) nogaps "
        "order(audited in_notes in_income_statement epsincon_usd most_prom "
        "non_gaap_is_kam no_ngm no_kams at_usd_ln loss btm growth_revt vol) "
        "drop(epsincon_usd non_gaap_is_kam no_ngm no_kams at_usd_ln loss btm growth_revt vol) "
        'stats(FES N r2_a, fmt(%12.0fc %12.0fc %12.3f %9.3f) '
        'labels("Fixed-effects" "Observations" "Adjusted R-squared" '
        '"p-value for Difference")) '
        "booktabs alignment(D{.}{.}{-1}) nonotes "
        'mtitles("\\shortstack{\\textit{in_income_statement} = 0 \\\\ '
        'DV: \\textit{mgmt_excess_actual}}" '
        '"\\shortstack{\\textit{Full Sample} \\\\ '
        'DV: \\textit{mgmt_excess_actual}}")',
        quietly=True,
    )
    format_latex(out)
    print("  -> face_vs_notes.tex")


if __name__ == "__main__":
    main()

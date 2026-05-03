"""Table 7: value_rel.tex — Are audited non-GAAP earnings more value relevant?"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.table_helpers import load_data, tables_dir, format_latex


def main():
    stata = load_data()

    # Col 1: without interaction
    stata.run(
        "reghdfe prccd_usd_plus30d mgmt_excess_actual street_adj_usd_ps "
        "epsincon_usd bv_usd_ps, "
        "absorb(year au regno_id) vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "F,A,Y"', quietly=True)
    stata.run("est store a1", quietly=True)

    # Col 2: with interaction
    stata.run(
        "reghdfe prccd_usd_plus30d mgmt_excess_actual audited "
        "mgmt_excess_actual_X_audited street_adj_usd_ps "
        "epsincon_usd bv_usd_ps, "
        "absorb(year au regno_id) vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "F,A,Y"', quietly=True)
    stata.run("est store a2", quietly=True)

    out = os.path.join(tables_dir, "value_rel.tex")
    stata.run(
        f'esttab a1 a2 using "{out}", '
        "replace label b(%9.3f) se(%9.3f) "
        "star(* 0.10 ** 0.05 *** 0.01) nogaps "
        "order(mgmt_excess_actual audited mgmt_excess_actual_X_audited "
        "street_adj_usd_ps epsincon_usd bv_usd_ps) "
        'stats(FES N r2_a, fmt(%12.0fc %12.0fc %12.3f %9.3f) '
        'labels("Fixed-effects" "Observations" "Adjusted R-squared" '
        '"p-value for Difference")) '
        "booktabs alignment(D{.}{.}{-1}) nonotes "
        'mtitles("\\shortstack{DV: \\textit{prccd_usd_plus30d}}" '
        '"\\shortstack{DV: \\textit{prccd_usd_plus30d}}")',
        quietly=True,
    )
    format_latex(out)
    print("  -> value_rel.tex")


if __name__ == "__main__":
    main()

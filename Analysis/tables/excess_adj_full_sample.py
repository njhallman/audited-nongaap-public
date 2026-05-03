"""Table 3: excess_adj_full_sample.tex — Are audited non-GAAP adjustments less aggressive?"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.table_helpers import load_data, tables_dir, format_latex


def main():
    stata = load_data()

    # Col 1: audited only, no FEs
    stata.run(
        "reghdfe mgmt_excess_actual audited, absorb() vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "None"', quietly=True)
    stata.run("est store a1", quietly=True)

    # Col 2: audited + controls, no FEs
    stata.run(
        "reghdfe mgmt_excess_actual audited epsincon_usd most_prom "
        "non_gaap_is_kam no_ngm no_kams at_usd_ln loss btm growth_revt vol, "
        "absorb() vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "None"', quietly=True)
    stata.run("est store a3", quietly=True)

    # Col 3: + A,Y FEs
    stata.run(
        "reghdfe mgmt_excess_actual audited epsincon_usd most_prom "
        "non_gaap_is_kam no_ngm no_kams at_usd_ln loss btm growth_revt vol, "
        "absorb(year au) vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "A,Y"', quietly=True)
    stata.run("est store a4", quietly=True)

    # Col 4: + F,A,Y FEs
    stata.run(
        "reghdfe mgmt_excess_actual audited epsincon_usd most_prom "
        "non_gaap_is_kam no_ngm no_kams at_usd_ln loss btm growth_revt vol, "
        "absorb(year au regno_id) vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "F,A,Y"', quietly=True)
    stata.run("est store a5", quietly=True)

    # Col 5: F*Y FEs
    stata.run(
        "reghdfe mgmt_excess_actual audited most_prom, "
        "absorb(regno_id#year) vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "F*Y"', quietly=True)
    stata.run("est store a6", quietly=True)

    out = os.path.join(tables_dir, "excess_adj_full_sample.tex")
    stata.run(
        f'esttab a1 a3 a4 a5 a6 using "{out}", '
        "replace label b(%9.3f) se(%9.3f) "
        "star(* 0.10 ** 0.05 *** 0.01) nogaps "
        'stats(FES N r2_a, fmt(%12.0fc %12.0fc %12.3f) '
        'labels("Fixed-effects" "Observations" "Adjusted R-squared")) '
        "booktabs alignment(D{.}{.}{-1}) nonotes "
        'mtitles("\\shortstack{DV: \\textit{mgmt_excess_actual}}" '
        '"\\shortstack{DV: \\textit{mgmt_excess_actual}}" '
        '"\\shortstack{DV: \\textit{mgmt_excess_actual}}" '
        '"\\shortstack{DV: \\textit{mgmt_excess_actual}}" '
        '"\\shortstack{DV: \\textit{mgmt_excess_actual}}")',
        quietly=True,
    )
    format_latex(out)
    print("  -> excess_adj_full_sample.tex")


if __name__ == "__main__":
    main()

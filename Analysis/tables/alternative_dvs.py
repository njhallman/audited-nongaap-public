"""Table 4: alternative_dvs.tex — Alternative DVs: negative adjustments & loss-to-profit."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.table_helpers import load_data, tables_dir, format_latex


def main():
    stata = load_data()

    stata.run(
        "reghdfe neg audited epsincon_usd most_prom non_gaap_is_kam "
        "no_ngm no_kams at_usd_ln loss btm growth_revt vol, "
        "absorb(regno_id#year) vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "F*Y"', quietly=True)
    stata.run("est store a1", quietly=True)

    stata.run(
        "reghdfe loss_to_profit audited epsincon_usd most_prom "
        "non_gaap_is_kam no_ngm no_kams at_usd_ln btm growth_revt vol "
        "if loss == 1, absorb(regno_id#year) vce(cluster regno_id)",
        quietly=True,
    )
    stata.run('estadd local FES "F*Y"', quietly=True)
    stata.run("est store a2", quietly=True)

    out = os.path.join(tables_dir, "alternative_dvs.tex")
    stata.run(
        f'esttab a1 a2 using "{out}", '
        "replace label b(%9.3f) se(%9.3f) "
        "star(* 0.10 ** 0.05 *** 0.01) nogaps "
        "drop(epsincon_usd non_gaap_is_kam no_ngm no_kams at_usd_ln loss btm growth_revt vol) "
        'stats(FES N r2_a, fmt(%12.0fc %12.0fc %12.3f) '
        'labels("Fixed-effects" "Observations" "Adjusted R-squared")) '
        "booktabs alignment(D{.}{.}{-1}) nonotes "
        'mtitles("\\shortstack{Full Sample \\\\ DV: \\textit{Negative Adj}}" '
        '"\\shortstack{\\textit{Loss} = 1 \\\\ DV: \\textit{Loss to Profit}}")',
        quietly=True,
    )
    format_latex(out)
    print("  -> alternative_dvs.tex")


if __name__ == "__main__":
    main()

"""Table 6: procs.tex — Specific audit procedures.

Panel A: Procedure descriptions, examples, and frequency among non-GAAP KAM firm-years.
Panel B: Criteria-based vs non-criteria-based procedures (regression).
Panel C: Individual procedures (condensed — one column per procedure).
"""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.table_helpers import load_data, tables_dir, format_latex, get_data_path

CONTROLS = (
    "no_kams non_gaap_is_kam epsincon_usd most_prom no_ngm "
    "at_usd_ln loss btm growth_revt vol"
)
DROP_CONTROLS = (
    "epsincon_usd non_gaap_is_kam most_prom no_kams no_ngm "
    "at_usd_ln loss btm growth_revt vol _cons"
)


PANEL_A_ROWS = [
    (
        'anne_proc_classification',
        'Challenge Classification',
        r"\textit{Kier Group plc, 30 June 2020} --- "
        r"``We reviewed the definition and classification of adjusting items in the Group's Annual Report, "
        r"including the sub-categorisation of these items. In particular, we challenged whether it was "
        r"appropriate to present certain costs within the Regional Southern Build business as restructuring "
        r"and related charges, on the basis that they related to contract and tender positions.''",
    ),
    (
        'anne_proc_substantive',
        'Substantive Testing',
        r"\textit{PZ Cussons plc, 31 May 2021} --- "
        r"``Substantively tested a sample of the adjusting items recognized in the year to supporting "
        r"documentation, such as invoices or sale agreements and worked with tax specialists to assess "
        r"the impact of the UK tax rate change.''",
    ),
    (
        'anne_proc_adequacy_disc',
        'Ensure Adequate Disclosure',
        r"\textit{Spirent Communications plc, 31 December 2023} --- "
        r"``Assessed whether the disclosures within the Group financial statements provided sufficient "
        r"detail for the reader to understand the nature of these items and how adjusted results "
        r"reconcile to statutory results.''",
    ),
    (
        'anne_proc_consist_mgmt_pol',
        'Ensure Aligns w/ Policy',
        r"\textit{Synthomer plc, 31 December 2023} --- "
        r"``We assessed the income and expenses classified as Special Items against the Group's "
        r"accounting policies.''",
    ),
    (
        'anne_proc_consist_past',
        'Ensure Consistent w/ Hist.',
        r"\textit{J D Wetherspoon plc, 29 July 2018} --- "
        r"``Ensuring that management's classification of exceptional items is consistent with prior year.''",
    ),
    (
        'anne_proc_consist_stds',
        'Ensure Aligns w/ Standards',
        r"\textit{Mitie Group plc, 31 March 2017} --- "
        r"``We have benchmarked against market practice, including, but not limited to: the guidance "
        r"published by the Financial Reporting Council in their thematic review; and the guidance "
        r"included in the `Guidelines on Alternative Performance Measures', issued by the European "
        r"Securities and Markets Authority (ESMA).''",
    ),
]


def _compute_frequencies():
    """Percentage of firm-years with each procedure among non_gaap_is_kam==1 firm-years.

    Collapses to unique (regno, year) first so firm-years with multiple non-GAAP
    measures aren't double-counted. Procedure indicators are constant within firm-year.
    """
    df = pd.read_csv(get_data_path(), low_memory=False)
    fy = df.drop_duplicates(subset=['regno', 'year'])
    kam = fy[fy['non_gaap_is_kam'] == 1]
    return {var: kam[var].mean() * 100 for var, _, _ in PANEL_A_ROWS}


def _write_panel_a(out_path):
    """Panel A: descriptions and examples, sorted by descending frequency."""
    freqs = _compute_frequencies()
    ordered = sorted(PANEL_A_ROWS, key=lambda row: freqs[row[0]], reverse=True)

    body_lines = []
    for i, (var, label, example) in enumerate(ordered):
        sep = r" \\" if i == len(ordered) - 1 else r" \\[6pt]"
        body_lines.append(f"{label} & {freqs[var]:.0f}\\% &\n{example}{sep}")

    content = (
        "\\footnotesize\n"
        "\\textit{Panel A: Procedure Descriptions and Examples}\n"
        "\\vspace{4pt}\n\n"
        "\\renewcommand{\\arraystretch}{1.3}\n"
        "\\begin{tabular}{p{4.2cm} c p{9.8cm}}\n"
        "\\\\[-1.8ex]\\hline \\hline \\\\[-1.8ex]\n"
        "Procedure & Frequency & Example \\\\\n"
        "\\midrule\n"
        + "\n".join(body_lines) + "\n"
        "\\\\[-1.8ex]\\hline \\hline \\\\[-1.8ex]\n"
        "\\end{tabular}\n"
        "\\renewcommand{\\arraystretch}{1.0}\n"
    )
    with open(out_path, 'w') as f:
        f.write(content)


def _combine_regression_panels(panel_b_path, panel_c_path, out_path):
    """Combine Panel B and C (regressions) into a single file."""
    with open(panel_b_path) as f:
        panel_b = f.read()
    with open(panel_c_path) as f:
        panel_c = f.read()
    with open(out_path, 'w') as f:
        f.write("\\footnotesize\n")
        f.write("\\textit{Panel B: Criteria-based vs Non-criteria-based Procedures}\n")
        f.write("\\vspace{4pt}\n\n")
        f.write(panel_b)
        f.write("\n\\vspace{6pt}\n\n")
        f.write("\\textit{Panel C: Individual Procedures}\n")
        f.write("\\vspace{4pt}\n\n")
        f.write(panel_c)
    os.remove(panel_b_path)
    os.remove(panel_c_path)


def main():
    stata = load_data()

    # ==================================================================
    # Panel B: Criteria-based vs Non-criteria-based
    # ==================================================================
    # Criteria-based: consist_mgmt_pol, consist_past, consist_stds
    # Non-criteria-based: classification, substantive, adequacy_disc
    stata.run(
        "gen bench_count = anne_proc_consist_mgmt_pol + anne_proc_consist_past + "
        "anne_proc_consist_stds",
        quietly=True,
    )
    stata.run(
        "gen nonbench_count = anne_proc_classification + anne_proc_substantive + "
        "anne_proc_adequacy_disc",
        quietly=True,
    )
    # Exclusive groups: higher count wins; tie -> both = 1; no procs -> both = 0
    stata.run(
        "gen criteria_dom = (bench_count > nonbench_count) | "
        "(bench_count == nonbench_count & bench_count > 0)",
        quietly=True,
    )
    stata.run(
        "gen audited_bench_dom_1_0 = (audited == 1 & criteria_dom == 0)",
        quietly=True,
    )
    stata.run(
        "gen audited_bench_dom_1_1 = (audited == 1 & criteria_dom == 1)",
        quietly=True,
    )
    stata.run(
        f"reghdfe mgmt_excess_actual audited_bench_dom_1_0 audited_bench_dom_1_1 "
        f"{CONTROLS}, "
        "absorb(year au regno_id) vce(cluster regno_id)",
        quietly=True,
    )
    stata.run("test audited_bench_dom_1_0 = audited_bench_dom_1_1", quietly=True)
    stata.run("estadd scalar pval_val = r(p)", quietly=True)
    stata.run('estadd local FES "F,A,Y"', quietly=True)
    stata.run('estadd local Controls "Yes"', quietly=True)
    stata.run("est store panelA", quietly=True)

    out_b = os.path.join(tables_dir, "_procs_panelB.tex")
    stata.run(
        f'esttab panelA using "{out_b}", '
        "replace label b(%9.3f) se(%9.3f) "
        "star(* 0.10 ** 0.05 *** 0.01) nogaps nocons "
        f"drop({DROP_CONTROLS}) "
        "order(audited_bench_dom_1_0 audited_bench_dom_1_1) "
        'stats(FES Controls N r2_a pval_val, fmt(%12.0fc %12.0fc %12.0fc %12.3f %9.3f) '
        'labels("Fixed-effects" "Controls" "Observations" "Adjusted R-squared" '
        '"p-value for Difference")) '
        "booktabs alignment(D{.}{.}{-1}) nonotes "
        'mtitles("DV: \\textit{mgmt_excess_actual}")',
        quietly=True,
    )
    format_latex(out_b)

    # ==================================================================
    # Panel C: Individual procedures (condensed)
    # ==================================================================
    # Use a common variable name so all columns align on the same row.
    proc_vars = [
        "anne_proc_substantive",
        "anne_proc_classification",
        "anne_proc_consist_mgmt_pol",
        "anne_proc_consist_stds",
        "anne_proc_consist_past",
        "anne_proc_adequacy_disc",
    ]

    for i, var in enumerate(proc_vars, start=1):
        stata.run(f"gen audit_and_proc = {var}_1_1", quietly=True)
        stata.run(f"gen audit_no_proc = {var}_1_0", quietly=True)
        stata.run(
            f"reghdfe mgmt_excess_actual audit_no_proc audit_and_proc "
            f"{CONTROLS}, "
            "absorb(year au regno_id) vce(cluster regno_id)",
            quietly=True,
        )
        stata.run("test audit_no_proc = audit_and_proc", quietly=True)
        stata.run("estadd scalar pval_val = r(p)", quietly=True)
        stata.run('estadd local FES "F,A,Y"', quietly=True)
        stata.run('estadd local Controls "Yes"', quietly=True)
        stata.run(f"est store b{i}", quietly=True)
        stata.run("drop audit_and_proc audit_no_proc", quietly=True)

    # Column order: non-benchmark (b2 b1 b6) then benchmark (b3 b5 b4)
    out_c = os.path.join(tables_dir, "_procs_panelC.tex")
    stata.run(
        f'esttab b2 b1 b6 b3 b5 b4 using "{out_c}", '
        "replace label b(%9.3f) se(%9.3f) "
        "star(* 0.10 ** 0.05 *** 0.01) nogaps nocons "
        f"drop({DROP_CONTROLS}) "
        "order(audit_no_proc audit_and_proc) "
        'stats(FES Controls N r2_a pval_val, fmt(%12.0fc %12.0fc %12.0fc %12.3f %9.3f) '
        'labels("Fixed-effects" "Controls" "Observations" "Adjusted R-squared" '
        '"p-value for Difference")) '
        "booktabs alignment(D{.}{.}{-1}) nonotes "
        'mgroups("Non-criteria-based" "Criteria-based", '
        "pattern(1 0 0 1 0 0) "
        "prefix(\\multicolumn{@span}{c}{) suffix(}) span "
        "erepeat(\\cmidrule(lr){@span})) "
        'mtitles("\\shortstack{Challenge\\\\Classif.}" '
        '"\\shortstack{Substantive\\\\Testing}" '
        '"\\shortstack{Adequate\\\\Disclosure}" '
        '"\\shortstack{Aligns w/\\\\Policy}" '
        '"\\shortstack{Consistent\\\\w/ Hist.}" '
        '"\\shortstack{Aligns w/\\\\Standards}")',
        quietly=True,
    )
    format_latex(out_c)

    # Write Panel A (descriptions) as separate file
    out_a = os.path.join(tables_dir, "procs_panelA.tex")
    _write_panel_a(out_a)
    print("  -> procs_panelA.tex")

    # Combine Panels B+C (regressions) into procs.tex
    out = os.path.join(tables_dir, "procs.tex")
    _combine_regression_panels(out_b, out_c, out)
    print("  -> procs.tex")



if __name__ == "__main__":
    main()

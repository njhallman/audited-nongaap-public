"""
Utilities for post-processing LaTeX table files produced by Stata's estout.
"""


def format_latex(file):
    """Replace variable names with LaTeX macro names and clean up table formatting."""
    with open(file, 'rt') as f:
        data = f.read()

    # Procedure interaction variables (order matters: longest first)
    data = data.replace(r"anne\_non\_gaap\_is\_kam\_1\_0", r"\AuditNoKam")
    data = data.replace(r"anne\_non\_gaap\_is\_kam\_1\_1", r"\AuditAndKam")

    data = data.replace(r"anne\_proc\_substantive\_1\_0", r"\AuditNoSub")
    data = data.replace(r"anne\_proc\_substantive\_1\_1", r"\AuditAndSub")
    data = data.replace(r"anne\_proc\_substantive", r"\ProcSub")

    data = data.replace(r"anne\_proc\_classification\_1\_0", r"\AuditNoClass")
    data = data.replace(r"anne\_proc\_classification\_1\_1", r"\AuditAndClass")
    data = data.replace(r"anne\_proc\_classification", r"\ProcClass")

    data = data.replace(r"anne\_proc\_consist\_mgmt\_pol\_1\_0", r"\AuditNoMgmtPol")
    data = data.replace(r"anne\_proc\_consist\_mgmt\_pol\_1\_1", r"\AuditAndMgmtPol")
    data = data.replace(r"anne\_proc\_consist\_mgmt\_pol", r"\ProcPol")

    data = data.replace(r"anne\_proc\_consist\_stds\_1\_0", r"\AuditNoStds")
    data = data.replace(r"anne\_proc\_consist\_stds\_1\_1", r"\AuditAndStds")
    data = data.replace(r"anne\_proc\_consist\_stds", r"\ProcStds")

    data = data.replace(r"anne\_proc\_consist\_past\_1\_0", r"\AuditNoPast")
    data = data.replace(r"anne\_proc\_consist\_past\_1\_1", r"\AuditAndPast")
    data = data.replace(r"anne\_proc\_consist\_past", r"\ProcPast")

    data = data.replace(r"anne\_proc\_adequacy\_disc\_1\_0", r"\AuditNoDisc")
    data = data.replace(r"anne\_proc\_adequacy\_disc\_1\_1", r"\AuditAndDisc")
    data = data.replace(r"anne\_proc\_adequacy\_disc", r"\ProcDisc")

    # Grouped/condensed procedure indicators (must precede "audited" replacement)
    data = data.replace(r"audit\_and\_proc", r"\AuditAndProc")
    data = data.replace(r"audit\_no\_proc", r"\AuditNoProc")
    data = data.replace(r"audited\_X\_proc\_count", r"\AuditedXProcCount")
    data = data.replace(r"audited\_disc\_dom\_1\_0", r"\AuditNoDiscGroup")
    data = data.replace(r"audited\_disc\_dom\_1\_1", r"\AuditAndDiscGroup")
    data = data.replace(r"audited\_bench\_dom\_1\_0", r"\AuditNoBenchGroup")
    data = data.replace(r"audited\_bench\_dom\_1\_1", r"\AuditAndBenchGroup")
    data = data.replace(r"proc\_count", r"\ProcCount")

    # Three-way KAM/procedure decomposition (Panel D)
    data = data.replace(r"audited\_kam\_other", r"\AuditedKamOther")
    data = data.replace(r"audited\_no\_kam", r"\AuditedNoKam")
    data = data.replace(r"audited\_bench", r"\AuditedBench")

    data = data.replace(r"loss\_to\_profit", r"\LossToProfit")
    data = data.replace(r"neg", r"\IncomeDecrease")
    data = data.replace(r"mgmt\_excess\_actual\_X\_audited", r"\ExcessXAudited")

    data = data.replace(r"audited", r"\AUDITED")
    data = data.replace(r"most\_prom", r"\MOSTPROM")
    data = data.replace(r"non\_gaap\_is\_kam", r"\NONGAAPISKAM")
    data = data.replace(r"at\_usd\_ln", r"\LOGASSETS")
    data = data.replace(r"loss", r"\LOSS")
    data = data.replace(r"btm", r"\BTM")
    data = data.replace(r"growth\_revt", r"\REVGROWTH")
    data = data.replace(r"vol", r"\VOLUME")
    data = data.replace(r"no\_ngm", r"\NUMNGMS")
    data = data.replace(r"no\_kams", r"\NUMKAMS")

    data = data.replace(r"epsincon\_usd", r"\GAAPEPS")

    data = data.replace(r"mgmt\_excess\_actual", r"\EXCESSADJ")

    data = data.replace(r"notes\_only", r"\NOTESONLY")
    data = data.replace(r"face\_only", r"\FACEONLY")
    data = data.replace(r"both\_face\_notes", r"\NOTESANDFACE")
    data = data.replace(r"in\_notes", r"\INNOTES")
    data = data.replace(r"in\_income\_statement", r"\ONFACE")

    data = data.replace(r"ngm\_adj\_usd\_ps", r"\MGMTADJ")
    data = data.replace(r"street\_adj\_usd\_ps", r"\STREETADJ")
    data = data.replace(r"bv\_usd\_ps", r"\BV")
    data = data.replace(r"prccd\_usd\_plus30d", r"\PRICETHIRTY")

    # Table formatting
    data = data.replace("toprule", r"\[-1.8ex]\hline \hline \\[-1.8ex]")
    data = data.replace("bottomrule", r"\[-1.8ex]\hline \hline \\[-1.8ex]")

    data = data.replace("longtable", "tabular")
    data = data.replace(r"\begin{table}[!htbp] \centering", "")
    data = data.replace(r" \caption{}", "")
    data = data.replace(r"\label{}", "")
    data = data.replace(r"\end{table}", "")

    with open(file, 'wt') as f:
        f.write(data)

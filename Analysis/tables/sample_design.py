"""Table 1: sampleDesign.tex — Sample selection (hardcoded counts)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.paths import tables_dir


def main():
    path = os.path.join(tables_dir, "sampleDesign.tex")
    with open(path, "w") as fout:
        fout.write(r"\begin{tabular}{ l r}")
        fout.write(r"\\[-1.8ex]\hline \hline \\[-4.2ex]")
        fout.write(r"\\Firm-years listed in the Main Market of LSE during 2013 - 2023: &12,940")
        fout.write(r"\\ \quad Less firm-years missing Compustat matches &(5,140)")
        fout.write(r"\\ \quad Less firm-years missing variables from Compustat &(1,114)")
        fout.write(r"\\ \quad Less firm-years missing variables from IBES &(2,730)")
        fout.write(r"\\ \quad Less firm-years missing registration numbers &(263)")
        fout.write(r"\\ \quad Less firm-years before 2013-09-30 &\underline{(148)}")
        fout.write(r"\\ Firm-years provided to Gemini &3,545")
        fout.write(r"\\ \quad Less firm-years missing Companies House filings &(239)")
        fout.write(r"\\ \quad Less firm-years that do not report NGMs &(146)")
        fout.write(r"\\ \quad Less firm-years that do not report earnings-based NGMs &\underline{(278)}")
        fout.write(r"\\ Number of firm-years in sample &2,882")
        fout.write(r"\\ Average number of non-GAAP measures per firm-year &2.88")
        fout.write(r"\\Size of the firm-year-measure sample &8,287")
        fout.write(r"\\\\[-3.0ex]\hline \hline \\[-1.8ex]\end{tabular}")
    print("  -> sampleDesign.tex")


if __name__ == "__main__":
    main()

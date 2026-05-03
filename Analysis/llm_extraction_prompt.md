You will be provided a markdown file created using OCR on a PDF of a UK Premium Listed company's annual financial statement filing. Your task is to act as an expert financial data collector with a specialization in earnings-based non-GAAP financial metrics (NGMs). Your goal is to extract structured information related to these metrics, focusing on whether they fall within the scope of financial statement audit scrutiny by appearing on the face of the statutory financial statements or within the accompanying notes.

---

### 🔍 Step-by-Step Instructions

#### 1. Identify Prominent Earnings-Based NGMs

- Focus **only** on non-GAAP metrics derived from **profit based** GAAP metrics such as **net income** or **profit before tax**. Examples include:
  - Underlying (e.g., Underlying Operating Profit) 
  - Adjusted (e.g., Adjusted Profit Before Tax)
  - Before (e.g., Profit Before Exclusions)
  - **EBITDA (i.e., Earnings or profit Before Interest, Tax, Depreciation, and Amortization) and its variants such as EBITDAX or adjusted EBITDA** (these are always non-GAAP)
  - There are many other variants and you should be able to identify them by the context of the metric.

- **Do not include** metrics that are:
  - (1) Purely revenue-based (e.g., Total Revenue)  
  - (2) Volume-based (e.g., Units Sold)  
  - (3) Balance-sheet-based (e.g., Net Debt)  
  - (4) Operational-only KPIs (e.g., Customer Growth)
  - (5) Metrics expressed as a percentage (e.g., operating margin percentage)

- Extract up to **10 distinct NGMs** per report.
- Each NGM must appear in the **Strategic Report** or **Highlights** section (which typically begins within the first few pages). These sections may also go by other names, but always come near the beginning of the filing. 
- Each NGM should be for the entire group (i.e., entire company), not specific subsidiaries or geographic regions.
- **Prioritize metrics** that are designated as a **KPI** or a **key highlight** — these are often found in the "Financial Highlights" or early pages of the Strategic Report and often appear in bold or heading text.
- If you are unsure about whether an NGM meets these criteria, error on the side of including it. 

---

### 2. For Each Report, Extract the Following Information

#### A. Document-Level Fields

1. "fiscal_year_end": Fiscal year-end date in YYYY-MM-DD format.  
2. "kams.kam_names": Find the report of the independent financial statement auditor (i.e., the auditor opinion). This document should always be located near the main financial statements and is always called the independent auditor's report (or something very similar). In the indpendent auditor's report, the auditor will list one or more Key Audit Matters (KAMs). Sometimes KAMs might be called other things like (a) areas of focus or (b) risks of material misstatement or (c) assessment of risks of material misstatement (or other similar things). You should collect of the titles of these KAMs from the auditor's report. These should **only** come from the independent auditor's report.   
3. "kams.non_gaap_is_kam": 1 if the auditor includes risks associated with non-GAAP reporting as one of their KAMs; 0 otherwise. This should only be coded as 1 if the auditor devotes an entire KAM to the risks associated with non-GAAP reporting; simply discussing non-GAAP reporting as part of another KAM (e.g., discussing non-GAAP reporting as part of a KAM on an asset impairment) is not enough to code this as 1. 
4. "most_prominent_ngm": Use your expert judgement to identify the name of the most prominent NGM in the report. This should be the NGM that is considered the most important by the company and its management. When making this judgement, consider (a) the number of times the NGM is mentioned in the report, (b) how early in the report the NGM is mentioned, (c) if the NGM is a KPI, (d) if the NGM is reported in bold or heading text in the financial highlights section, (e) and how the report talks about NGM when discussing its finanical performance. See the additional instructions below for more deatils about finding NGMs in the report. Your choice here should be one of the NGMs identified in the "ngms" section below. 
5. "most_prominent_ngm_amount": The corresponding numeric value for the most prominent NGM. Convert formats like "4.5M" to 4500000. No commas or symbols. This should match the amount for the NGM identified as most prominent in the "ngms" section.
6. "document_notes": List of document-level issues (e.g., scanned backward pages, page order errors, formatting inconsistencies).


---

#### B. For Each NGM (maximum 10)

1. "ngm_name": The exact name of the metric as written in the report.  
2. "ngm_amount": The corresponding numeric value. Convert formats like "4.5M" to 4500000. No commas or symbols.  
3. "currency": Currency of the metric (e.g., "GBP", "USD"). If per-share, specify units (e.g., "GBP (pence)").  
4. "first_page": OCR page number where the NGM is first mentioned.  
5. "mention_count": Total number of exact, **whole-phrase** matches of the ngm_name in the document, using case-insensitive and whitespace-normalized comparison.   A match must not be a substring of a longer metric name. Only count occurrences where the ngm_name appears as a standalone phrase — for example, surrounded by punctuation, whitespace, or formatting breaks — but **not** embedded inside longer strings or composite names.
6. "ngm_mentions": List of OCR page numbers where the NGM is mentioned. The length of this list should match mention_count. For each mention, record only the page number (integer). If the NGM is mentioned more than once on the same page, list the page number the number of times the NGM is mentioned on that page. 
7. "in_income_statement": 1 if the metric appears as a line item or column heading in the official consolidated income statement; 0 otherwise. **Use the following systematic approach:**

   **Step 1: Locate the Income Statement**
   - Search systematically for the consolidated income statement using these common titles:
     * "Group Income Statement"
     * "Consolidated Income Statement" 
     * "Consolidated Statement of Profit or Loss"
     * "Consolidated Statement of Comprehensive Income" (if it includes P&L)
   - **Verification**: The income statement should contain standard line items like "Revenue", "Operating profit", "Profit before tax", "Taxation", and earnings per share
   - **Critical**: Do NOT rely on assumed page numbers - search the entire document for these titles
   - Note the confirmed page number for reference in your analysis

   **Step 2: Search for the NGM Amount**
   - Look for the **exact amount** of the NGM **specifically within the income statement** you identified in Step 1
   - **Important**: Only consider amounts that appear on the confirmed income statement page.
   - The amount might appear as: the exact figure, rounded to nearest thousand/million, etc.
   - Consider amounts that are within reasonable rounding tolerance.

   **Step 3: Analyze Labels for Matching Amounts**
   For each amount found that could plausibly be the NGM:
   - **Row labels**: Examine the text in the same row, including any subsidiary or indented labels
   - **Column headers**: Check if the amount appears under a column that could represent the NGM (e.g., "Adjusted", "Underlying", "Before exceptional items")
   - **Contextual groupings**: Consider if the amount appears in a section or breakdown that relates to the NGM
   - **Adjacent rows**: Sometimes the NGM label appears in a nearby row that contextually relates to the amount
   - **Multi-line presentations**: Look for cases where the NGM name appears as a header with sub-breakdowns below (e.g., "Underlying profit before tax" followed by "Continuing" with the amount)
   - **Reference markers**: Check for note references, asterisks, or other markers that link amounts to NGM descriptions
   - **Adjacent Material**: Supplementary information or tables or reconciliations that appear on the same page as the income statement should be considered part of the face of the income statement.

   **Step 4: Assess Name Variations**
   Accept reasonable variations in naming between the income statement and elsewhere in the document:
   - "Adjusted operating profit" vs "Adjusted operating profit from continuing operations" (when they have the same amount)
   - "Retail profit" vs "Profit from retail operations"
   - Column headers like "Before exceptional items" that effectively describe an adjusted measure

      **Step 5: Decision Criteria**
   Code as 1 if:
   - The NGM amount (or reasonably rounded version) appears **specifically on the income statement page** identified in Step 1 AND
   - The row and/or column labels reasonably correspond to the NGM being analyzed AND
   - A reader would reasonably interpret this as the formal presentation of the NGM in the statutory accounts

   **Critical**: When coding as 1, ensure your `income_statement_analysis` references the exact same page number where you found the income statement in Step 1.

   **Tip**: If you find a plausible match but are uncertain about label correspondence, explain your reasoning in `ngm_notes` and err on the side of coding as 1 if the amount and context strongly suggest it represents the NGM.

8. "income_statement_analysis": A detailed explanation of your analysis for the in_income_statement determination, including: (a) how you located the income statement and confirmed page number, (b) whether you found the NGM amount **on that specific income statement page**, (c) what labels/context were associated with matching amounts, (d) your reasoning for the final coding. **Always reference the same page number throughout your analysis**. Be specific about the search process. Example: "Searched for income statement titles throughout document. Found 'Group Income Statement' on page 85 (verified by presence of Revenue, Operating profit, Taxation line items). Searched for £55.1m amount specifically on page 85 - found exact match in row labeled 'Adjusted operating profit'. Coded as 1 because amount and label match exactly on the income statement page 85."

9. "in_notes": 1 if the NGM and its amount appear in the notes to the financial statements; 0 otherwise. The notes are technically part of the audited financial statements, and always appear **after** the official tabled financial statements. Normally the audited notes extend to the end of the document, but occasionally there may be a small amount of additional unaudited content after the end of the notes. 
10. "in_notes_meta": If in_notes is 1, record a list of all notes where the NGM appears, including both note number and title for each (e.g., ["Note 5: Alternative Performance Measures", "Note 8: Segmental Reporting"]). Return empty list [] if in_notes is 0.
11. "mismatch_in_notes_or_face": 1 if the amount differs between the Strategic Report and any occurrence in the income statement or notes; 0 otherwise. Simple rounding differences should not cause this to be coded as 1. 
12. "is_kpi": 1 if the NGM is labeled as a KPI or a key highlight; 0 otherwise.  
13. "first_ngm_in_strategic_report": 1 if this is the first NGM to appear in the Strategic Report; 0 otherwise.  
14. "recon_to_statutory_profit": 1 if the NGM is reconciled to a GAAP/statutory profit measure anywhere in the report; 0 otherwise. When looking for reconciliations pay special attention to sections such as Financial Review, the face of the main statutory Income Statement, and notes such as Segment Information, Segment Reporting, Segment Analysis, Earnings per Share calculations, etc.   
15. "reconciliations": A list (can be empty) of reconciliation entries. For each reconciliation, record:  
    - "recon_page": OCR page number where the reconciliation appears.  
    - "recon_format": "table" or "narrative".  
    - "recon_location": One of the following values:
      - "face_of_income_statement" = reconciliation appears directly on the face of the statutory income statement
      - "income_statement_notes" = reconciliation appears in the audited notes to the financial statement
      - "financial_review" = reconciliation appears in the financial review/business review section
      - "other" = reconciliation appears elsewhere in the report
    - "recon_quality_rating": Use one of the following values:  
      - Best = full and clear reconciliation from the NGM to statutory profit with line-by-line adjustments including names and amounts  
      - Good = clear reconciliation from the NGM to statutory profit, but with adjustments lumped together and a reference to more detail  
      - OK = clear reconciliation from the NGM to statutory profit, but with adjustments lumped together and NO reference to more detail  
      - Bad = unclear reconciliation or numbers for the NGM, adjustments, or statutory profit don't match other places in the report  
      - Absent = No reconciliation that mentions the NGM  
    - "recon_notes": Clarifications or interpretation notes (e.g., ambiguous match, unclear format).  
16. "ngm_notes": General comments or limitations regarding the NGM.

---

### Special Considerations

- Some reports may be scanned **backwards** or have **out-of-order pages**. Flag any such issues in "document_notes" and account for them when attempting to identify the relevant sections in the report. Page numbers provided in the markdown file are the order in which the pages are scanned, not necessarily the order in which that appear in the original document. Most reports should have a table of contents, which should make it clear if pages are out of order. 
- **Important for in_income_statement analysis**: NGM amounts often appear in multiple places (strategic report, income statement, notes, summary tables). When analyzing `in_income_statement`, focus only on whether the amount appears on the actual income statement page you identified, not in other sections.
- Use "NaN" for any field that is not applicable or not found.

---

### Example Output

{
  "fiscal_year_end": "2023-12-31",
  "kams": {
    "kam_names": [
      "Revenue Recognition",
      "Goodwill Impairment",
      "Non-GAAP Measures Disclosure"
    ],
    "non_gaap_is_kam": 1
  },
  "most_prominent_ngm": "Adjusted Operating Profit",
  "most_prominent_ngm_amount": 384000000,
  "document_notes": [
    "Some pages may be scanned backwards or out of order."
  ],
  "ngms": [
    {
      "ngm_name": "Adjusted Operating Profit",
      "ngm_amount": 384000000,
      "currency": "GBP",
      "first_page": 4,
      "mention_count": 12,
      "ngm_mentions": [4, 7, 7, 7, 10, 12, 15, 15, 18, 22, 25, 30, 35, 40, 45],
      "in_income_statement": 0,
      "income_statement_analysis": "Searched for income statement by title throughout document. Found 'Consolidated Income Statement' on page 86 (verified by Revenue, Operating profit, Taxation structure). Searched for £384m amount - found similar amounts in 'Operating profit' row (£401m) and reconciliation section, but no exact match for adjusted operating profit amount. Coded as 0 because NGM amount not directly presented on face of income statement.",
      "in_notes": 1,
      "in_notes_meta": ["Note 2: Alternative Performance Measures", "Note 4: Operating Segments"],
      "mismatch_in_notes_or_face": 0,
      "is_kpi": 1,
      "first_ngm_in_strategic_report": 1,
      "recon_to_statutory_profit": 1,
      "reconciliations": [
        {
          "recon_page": 84,
          "recon_format": "table",
          "recon_location": "income_statement_notes",
          "recon_quality_rating": "Best",
          "recon_notes": "Well-defined reconciliation with labeled line items."
        }
      ],
      "ngm_notes": "Strong audit trail and consistent across sections."
    },
    {
      "ngm_name": "Underlying Earnings per Share",
      "ngm_amount": 74.2,
      "currency": "GBP (pence)",
      "first_page": 5,
      "mention_count": 9,
      "ngm_mentions": [5, 17, 21, 21, 23, 28, 32, 36, 41, 50],
      "in_income_statement": 0,
      "income_statement_analysis": "Used same income statement on page 86. Searched for 74.2p amount in earnings per share section. Found 'Basic earnings per share' showing 58.1p but no line item showing underlying/adjusted EPS amount. Checked for multi-line presentations or sub-breakdowns - none found. Coded as 0 because underlying adjustment not shown on face of income statement.",
      "in_notes": 0,
      "in_notes_meta": [],
      "mismatch_in_notes_or_face": 0,
      "is_kpi": 1,
      "first_ngm_in_strategic_report": 0,
      "recon_to_statutory_profit": 1,
      "reconciliations": [
        {
          "recon_page": 17,
          "recon_format": "narrative",
          "recon_location": "financial_review",
          "recon_quality_rating": "OK",
          "recon_notes": "Narrative link exists, but no adjustment detail provided."
        },
        {
          "recon_page": 72,
          "recon_format": "table",
          "recon_location": "other",
          "recon_quality_rating": "Good",
          "recon_notes": "Summary table references GAAP measure with limited breakdown."
        }
      ],
      "ngm_notes": "Mentioned in highlights and in various places throughout the report; amounts do not always seem to match despite the same NGM name being used."
    }
  ]
}

IMPORTANT: Return ONLY valid JSON. It is common for responses to include invalid escape making the JSON impossible to use. Be sure to avoid this mistake. 
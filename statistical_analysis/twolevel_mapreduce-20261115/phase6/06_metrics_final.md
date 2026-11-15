# OrionDesk AI — Final independent metric recomputation (Protocol v6.1)

**Status:** `FINAL_BEST_EFFORT`. **Method:** `supplied_eight_file_set`. **Source:** 90-physical-page English OrionDesk AI PDF, document `OD-AI-DDS-001`, `R1.0 / revision 1.3`. **Scored inputs:** eight unchanged Markdown documents.

## Single effective canonical universe

| Item | Independently recomputed count |
|---|---:|
| PDF-positive requirements `|R|` | 1005 |
| PDF-negative bounded controls `|N|` | 37 |
| Raw generated occurrences `|GO|` | 3128 |
| Raw generated semantic classes `|G|` | 3018 |
| Canonical prediction-positive units `|P|` | 977 |
| Canonical decision units `|U|` | 1042 |
| Asserted fixed controls `|B|` | 0 |
| Unsupported generated-only propositions `|F|` established | 0 |

| Actual \ Predicted | Positive | Negative |
|---|---:|---:|
| Source-positive | **TP 977** | **FN 28** |
| Source-negative | **FP 0** | **TN 37** |

| Measure | Computation | Provisional value |
|---|---|---:|
| Precision | 977 / (977 + 0) | **100.0000%** |
| Recall | 977 / (977 + 28) | **97.2139%** |
| F1 | 2 × 977 / (2 × 977 + 0 + 28) | **98.5873%** |
| Semantic duplication | (3128 − 3018) / 3128 | **3.5166%** |

The bounded negative inventory is **not** the universe of all absent requirements. Precision is computed from the canonical effective-prediction universe and must not be mislabeled raw-generated-class precision. There is deliberately no assertion that `TP + FP = |G|`.

## Independently recomputed equalities

- `TP + FN = 977 + 28 = 1005`.
- `TN + asserted N = 37 + 0 = 37`.
- `FP = |F| + |B| = 0 + 0 = 0` **in the current adjudicated ledger**, not a certified absence of unsupported claims.
- `TP + TN + FP + FN = 977 + 37 + 0 + 28 = 1042 = |U|`.
- `|U| = |R| + |N| + |F| = 1005 + 37 + 0 = 1042`.
- `|GO| − |G| = 3128 − 3018 = 110 = 1 within-file + 109 across-file`.
- Repeated semantic classes: 80; repeated classes spanning more than one file: 80.

## Source and evidence checks

- Original source PDF: **90** pages. Final source atoms reference **76** pages; the coverage ledger includes all 90 pages (some have no normative atoms).
- Original Markdown corpus: **8** files, **2,926** physical lines. Each final generated occurrence appears in the reconstructed physical-line coverage ledger, including 12 recovered at Phase 5.
- **1002 / 1005** final source quotes match PDF page text. The remaining **3** are Figure 1.1 labels on physical page 8, checked in the image rendering.
- All **977** current TP records have a Phase 5 source/generated evidence audit. The TP proof statuses are bounded best-effort, not independent semantic certification.
- All **28** current FN records have a root-cause disposition and strongest actual generated candidates; 895 earlier matcher misses are documented as corrected to TP.
- One obsolete, contradictory FN-history row for `PDF-00613` was removed from the final copied ledger in Phase 6, with a dedicated change-delta entry. The final FN remains unchanged. The full-corpus FN audit now has **923** unique source IDs.
- Every supported generated citation was checked against its original Markdown filename and physical line; **0** location errors were found.

## Certification boundary

**`FINAL_BEST_EFFORT` is deliberate.** 2,353 raw generated classes carry `E1_UNCERTAIN` PDF-support grades; 239 class eligibility flags remain, and none of the 3,018 class verdicts is independently semantically certified. Consequently **FP = 0 and Precision = 100% are not verified semantic-correctness results**. The 28 FN are 8 partially entailed and 20 conservatively unresolved, not 28 proven omissions. Arithmetic reconciliation does not certify all 963 E2 bridges. This evaluation describes generated specifications for a fictional reference design, not production application performance, correctness, or security.

Run the independent checker using `python compute_metrics.py --ledger-dir . --original-dir .. --output-dir .` (Python 3; optional PyMuPDF for exact PDF-text checks). Detailed limits are in `08_coverage_and_limitations.md`.

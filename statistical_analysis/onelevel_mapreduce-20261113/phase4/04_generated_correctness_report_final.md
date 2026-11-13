# Phase 4 — Generated Claim Validity and Four-Cell Canonical Scoring

**Status:** PHASE_COMPLETED_BEST_EFFORT  
**Protocol:** v6.1  
**Scored scope:** One complete set of eight unmodified Markdown specifications  
**Authoritative source:** OrionDesk_AI_Detailed_Design_Specification(8).pdf, 90 physical pages, R1.0 / revision 1.3.

## Canonical confusion matrix

| Actual \ Predicted | 1 | 0 |
|---|---:|---:|
| 1 — PDF normative atom | TP **801** | FN **223** |
| 0 — negative control or unsupported generated-only proposition | FP **6** | TN **37** |

- Precision = 801/(801+6) = **99.256506%**.
- Recall = 801/(801+223) = **78.222656%**.
- F1 = 2 × 801/(2 × 801 + 6 + 223) = **87.493173%**.
- The enumerated canonical universe contains **1067** units: 1024 PDF-positive atoms + 37 fixed negative controls + 6 distinct generated-only unsupported propositions.
- The predicted-positive count **807** is not required to equal the **4075** raw generated classes. A universal generated rule can cover multiple source atoms.
- TN **37** is restricted to the bounded 37 PDF-negative controls, not all possible negative requirements.

## Generated-claim correctness audit

| Raw class validity category | Count |
|---|---:|
| PDF_ENTAILED | 562 |
| SUPPORTED_NONCOVERING | 3,507 |
| PDF_UNSUPPORTED | 6 |
| **Total** | **4,075** |

Every class has the original Markdown evidence locator, PDF reciprocal search candidates, source page information, and a documented, best-effort validity disposition. All 37 fixed negative controls underwent a separate generated-to-control reverse check; no affirmative forbidden counterfactual was retained.

The **6 generated-only FP** are directives in six scored files to consolidate unresolved items into a later Stage 8 Markdown document. Those obligations are not normative product requirements in the PDF. Importantly, they are **Phase 5 eligibility challenges**: their text may be document-generation process metadata that Phase 2 should not have considered a definitive implementation requirement. The present FP count must not be treated as a certified design defect count.

## Evidence and reliability limitations

1. The **801 TP / 223 FN** source-side results were retained from Phase 3. No additional TP was manufactured from PDF-related class names or a mere identifier overlap in this phase.
2. **1,011** raw classes have a weak lexical PDF passage score below 0.23; this is not proof of PDF non-entailment and is **not** automatically counted as FP. There are **226** especially weak candidates below 0.16. Their actual quotations and nearest alternatives are in the reciprocal support ledger.
3. **3,507** class dispositions did not generate new PDF-positive TP links. Some may be narrower supported claims; others may reveal missed source atomization or semantic bridges. Independent reciprocal reviews can alter these assignments. They are **not certified entailments** based only on retrieval.
4. The structural confusion-matrix arithmetic passes, but this does not certify complete semantic accuracy. Ambiguous Phase 3 FN and TP bridges, all class-validity predicates, and the six potential eligibility misclassifications remain Phase 5 audit items.
5. Neither the source PDF nor the eight scored Markdown documents was modified. The shared source atom inventory and the 37 bounded controls remain fixed and reusable across methods.

## Phase boundary and outputs

This turn completed Phase 4 only. Phase 5 has **not** been executed. The canonical universe, each judgment, generated validity, reciprocal source search, negative-control checks, and score calculation are delivered as individual English files; no archive was created.

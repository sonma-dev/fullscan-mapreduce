# OrionDesk AI — Atomic Evaluation Deliverable Archive

Protocol version: 6.1
Scope: phases 1 through 6 (one evaluation method, eight scored Markdown specifications).
Final reported status: FINAL_BEST_EFFORT, not semantically certified.

## Directory map

- `phase1/`: Original PDF-derived positive/negative evidence ledgers and Phase 1 audit.
- `phase2/`: Initial generated corpus extraction and deduplication; preserved original ledgers are used where available.
- `phase3/`: Initial source-to-generated semantic coverage, FN challenge, and evidence bridge records.
- `phase4/`: Initial generated-validity and four-cell judgments, preserving the pre-Phase-5 snapshot.
- `phase5/`: Corrected working ledgers, source atomization, TP evidence, duplicate audit, and revised counts.
- `phase6/`: Final independently recomputed metrics, repaired canonical universe, validation and limitations.

## Important versioning notes

Phase 1 is the original 1,024-atom PDF snapshot; Phase 5 reduces the source inventory to 1,008 after atomization audit. Phase 2 is an initial snapshot; Phase 5 has its corrected generated occurrence/class ledgers. Phase 3 and 4 are initial judgment snapshots. Phase 5 revises them and Phase 6 repairs the final canonical universe, so `phase6/03_canonical_universe_final.jsonl` is authoritative for the final scoring-universe rows. Other corrected ledgers remain under `phase5/`.

The source PDF and eight scored Markdown input files are **not** included: this ZIP contains authored evaluation deliverables, not input attachments. No scratch files, logs, Python caches, or rendered temporary images were archived. The archived output is a packaging convenience expressly requested by the user, notwithstanding the protocol's default individual-file delivery policy.

Final reported cells: TP 963, TN 37, FP 0, FN 45. Precision 100.00%, Recall 95.54%, F1 97.72%. Reported raw semantic duplication: 204 excess occurrences / 2,553 eligible occurrences = 7.99%. These are reproducible *best-effort* scores. Some meaning-level checks remain uncertified; consult `phase6/08_coverage_and_limitations.md`.

The JSON manifest in the root records the SHA-256 of each archived file and its originating local path classification.

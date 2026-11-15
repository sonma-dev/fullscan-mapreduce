# Phase 5 raw generated semantic duplication

| Measure | Count |
|---|---:|
| Eligible occurrences `|GO_m|` | 2320 |
| Distinct semantic classes `|G_m|` | 2241 |
| Duplicate excess | 79 |
| Within-file excess | 3 |
| Across-file excess | 76 |
| Repeated classes | 61 |
| Repeated classes spanning files | 58 |
| Duplicate rate | 0.034052 (3.41%) |

Canonical representatives are the first occurrence by input-file order, physical line and table-cell order. Excess occurrences are `within_file` if an earlier instance of their class is in the same file, otherwise `across_file`. The audited API-025 / API-026 source-context collision was split even though the body cells are identical. This rate uses raw generated occurrences/classes, never expanded source coverage bridges.

Semantic class matching is best effort, and identical short result cells may depend on inherited row contexts.

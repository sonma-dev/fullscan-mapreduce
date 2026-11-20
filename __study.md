1. In traditional data engineering, we could derive statistical metrics deterministically using statistics. Today, however, with LLMs, we can compute metrics at ultra-high speed even on data that requires semantic interpretation.
2. When calculating metrics such as TP, TN, FP, and FN, expanding the dataset can sometimes force changes to the metric calculation protocol itself.
  - The easiest approach is to finalize all datasets before deriving metrics. In practice, however, additional datasets are often added later.
3. Whether it's specifications, protocols, or the tension between giving AI more freedom versus maintaining accuracy, the same dynamic applies to precision, recall, and F1-scores—just as it does to greenfield versus brownfield environments. It is a matter of balance; in other words, fine-tuning according to the specific requirements.
4. If the underlying assumption of what constitutes 100% is flawed, no amount of fine-tuning will get us close to 100%.
  - Granularity asymmetry (the 1-to-N or N-to-1 matching problem): In natural language specification extraction, the single biggest factor that disrupts an evaluation protocol is a mismatch in atomic granularity between the gold set and the LLM's extracted outputs.
5. In short, deriving TP, TN, FP, and FN is relatively straightforward when matching via embeddings (vectors), but it becomes difficult when relying on semantics.
6. If calibration is needed to achieve strong TP, TN, FP, and FN scores, that calibration mechanism should be built into the MapReduce pipeline.
7. Even if one method achieves 100% under a given metric calculation protocol, if another method also hits 100%, we can no longer determine which of the two is superior.
8. Building a universal, one-size-fits-all metric calculation protocol is difficult.
  - A gold set is not meant to be universal; its purpose is to determine whether metrics derived from a given dataset can be fairly compared within that dataset's scope. If we add datasets haphazardly, we're bound to get hit with an FP (false positive) explosion.
9. Data engineering processes big data and requires massive compute time; it helps to think of traditional MapReduce in the same way as LLM-based MapReduce over natural language.

  Note: Computational speed is important, but best-effort results are not enough—you also need confidence (certainty).

10. If the granularity of a specification's gold set is too fine, precision will look good, but recall will drop—that is only natural.
11. If we extract atomic requirements chapter by chapter and then assemble the overall set, the document's global context is lost and the atomic requirements diverge. Current LLMs still cannot sequentially deduplicate thousands of atomic items semantically.
  - In such cases, human-driven MapReduce is effective: first establish the atomic requirements for the entire document as a whole, then extract atomic requirements chapter by chapter, and consolidate them against the document-wide set while accounting for duplicates.
  - In short, when building a gold set, if we extract atoms chapter by chapter without global context and attempt to merge them at the end, the LLM will fail to merge them semantically, causing the number of atoms to explode.
12. The approval process for full-load operations is highly inefficient because, in a MapReduce architecture, the detailed data required for approval must be propagated upward from the leaves and forks to the approving forks and the root.
13. There is a trade-off between accuracy and computational cost. Even when the compute cost is realistic, if human intervention is required in the loop, the time and effort can easily exceed what a human can tolerate.
14. People say LLMs can understand meaning, but in reality they perform statistical next-token prediction. Relying on them to make semantic judgments—such as for deduplication—leads to disaster: rampant failures and an explosion in volume, or a divergence of atomic requirements.

  Note: If we want to consolidate meaning, we should break the task down into small chunks.

15. Rather than reducing the responses of all child nodes at once at the root or forks, reducing them incrementally in smaller chunks may make semantic reduction much easier for current LLMs. Since current LLMs struggle to integrate meaning all at once, in an LLM-based MapReduce pipeline—disregarding cost—you can choose to consolidate meaning within each shard first, and then integrate meaning again across every shard alongside the global context.
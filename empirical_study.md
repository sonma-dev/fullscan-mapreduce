I will systematically document my findings through empirical research.

## Statistical Analysis

*Semantic Statistical Analysis*

- People say LLMs can understand meaning, but in reality they perform statistical next-token prediction. Relying on them to make semantic judgments, such as for deduplication, can lead to widespread failures, an explosion in the number of atomic requirements, and semantic divergence.
- In traditional data engineering, we could deterministically calculate evaluation metrics using statistical methods. Today, however, with LLMs, we can compute metrics at high speed even on data that requires semantic interpretation.
- Deriving TP, TN, FP, and FN is relatively straightforward when matching via embeddings (vectors), but it becomes difficult when relying on semantics.
- When we ask an LLM to integrate semantic information, we should first break it down into smaller semantic units. Otherwise, the LLM may fabricate meanings during integration because the original meanings have not been properly atomized.

*Human-in-the-Loop*

- There is a trade-off between accuracy and computational cost. Even when the computational cost is manageable, if human intervention is required in the loop, the time and effort can easily become unsustainable.

*Achieving Completeness and Perfect Precision*

- We cannot achieve precision and recall values close to 100%, no matter how much we fine-tune, if our assumption that the given dataset has 100% precision and recall is incorrect.

*Granularity*

- Even if we provide an LLM with a specific metric calculation protocol, we cannot obtain metrics within an acceptable range due to differences in the granularity of atomic requirements between the gold set and the LLM-extracted results, namely, an asymmetry in specification granularity.

*Gold Set*

- When calculating TP, TN, FP, and FN counts, expanding the dataset can sometimes require changes to the metric calculation protocol itself. The easiest approach is to finalize all datasets before deriving metrics. In practice, however, additional datasets are often added later.
- Even if one method achieves 100% under a given metric calculation protocol, if another method also hits 100%, we can no longer determine which of the two is superior.
- Building a universal, one-size-fits-all metric calculation protocol is difficult.
  - A gold set is not meant to be universal; its purpose is to determine whether metrics derived from a given dataset can be fairly compared within that dataset's scope. If we add datasets haphazardly, we risk a significant increase in false positives.
- If the atomic requirements in a specification's gold set are too fine-grained, precision will look good, but recall will drop—that is only natural.

*Refinement*

- If we extract atomic requirements chapter by chapter and then assemble the overall set, we lose the document-wide context, leading to inconsistent granularity and semantic duplication. Current LLMs still struggle to sequentially deduplicate thousands of atomic requirements based on semantic equivalence.
  - When building a gold set, if we extract atomic requirements chapter by chapter without global context and attempt to merge them at the end, semantic deduplication may fail, causing the number of atomic requirements to grow excessively.
  - In such cases, human-guided MapReduce is effective: first establish a document-wide reference set of atomic requirements, then extract atomic requirements chapter by chapter and reconcile them against the reference set while resolving duplicates.

## Greenfield and Brownfield Development

*Degrees of Freedom Granted to AI*

- We should give AI more freedom when working with specifications and protocols. However, this freedom can prevent us from obtaining satisfactory results in situations where rigorous outcomes are required. For example, concise specifications written in Markdown may not yield high precision, recall, or F1 scores. We need to carefully consider the balance between freedom and constraints given to AI in greenfield and brownfield development. In other words, we must fine-tune the degree of freedom granted to AI according to the specific requirements.

## Implementation of LLM-Based MapReduce

*Incorporating Metric Calibration into implementation*

- If calibration is needed to achieve accurate TP, TN, FP, and FN counts in metric calculations, that calibration mechanism should be built into the MapReduce pipeline.

*Sequential Reduction*

- Instead of reducing the responses from all immediate child nodes of a root or fork node at once, we might make semantic reduction easier for current LLMs by processing the responses sequentially.
  - In other words, we cannot easily make current LLMs integrate large amounts of semantic information all at once. In LLM-based MapReduce, root and fork nodes can adopt an approach in which they sequentially reduce the responses from their respective shards into a cumulative response, then regenerate that cumulative response using the global context and the responses from every shard.

*Confidence Rather Than Best-Effort*

- Data engineering processes big data and requires massive compute time; it helps to think of traditional MapReduce in the same way as LLM-based MapReduce over natural language. Note that computational speed is important, but best-effort results are not enough. You also need confidence.

*Approval Process for MapReduce and Full-Load Approaches*

- In hierarchical MapReduce, root and fork nodes can perform more effective approval processes than a full-load approach because they can obtain detailed information propagated upward from their descendant leaf nodes.

## Extending Hierarchical MapReduce to Network Theory

*Directed Acyclic Graph*
- When we extend MapReduce approaches to more complex structures, using a Directed Acyclic Graph (DAG) instead of an N-level tree may allow us to achieve higher accuracy and completeness than 1-level MapReduce approaches.

*Types of Nodes and Attributes of Links*
- We can attach global context and content to chunks based on two types of information: the types of the two entities and the attributes of the link between them. We then send these chunks to child nodes.

*Determining Data Topology*
- Determining the dependencies between entities requires a separate algorithm. Of course, we can use LLMs to construct the topology of the given objects.

*Large-N Hierarchical MapReduce*
- Among hierarchical MapReduce approaches, I believe that N-level MapReduce, where $N \gg 1$, may achieve the highest performance. However, it also requires extensive fine-tuning and takes the longest to formulate.
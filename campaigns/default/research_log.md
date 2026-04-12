# Research Log

## exp_1b1293e0
- timestamp: 2026-04-12T15:16:54.073774+00:00
- hypothesis: Tester similarity avec chunk_size=400 et top_k=4 pour améliorer le compromis qualité/coût.
- config: `{'retriever_type': 'similarity', 'chunk_size': 400, 'chunk_overlap': 80, 'top_k': 4, 'temperature': 0.2}`
- metrics: `{'faithfulness': 0.7039896532538162, 'answer_relevance': 0.727319346422016, 'context_precision': 0.677319346422016, 'citation_accuracy': 0.6639896532538162, 'normalized_cost': 0.27863937459028837, 'normalized_latency': 0.266281881439525}`
- cost_usd: 0.0056
- latency_ms: 719.54
- status: baseline
- notes: MVP simulated run

## exp_46f153b7
- timestamp: 2026-04-12T15:16:54.074465+00:00
- hypothesis: Tester similarity avec chunk_size=600 et top_k=12 pour améliorer le compromis qualité/coût.
- config: `{'retriever_type': 'similarity', 'chunk_size': 600, 'chunk_overlap': 40, 'top_k': 12, 'temperature': 0.0}`
- metrics: `{'faithfulness': 0.7344754562746229, 'answer_relevance': 0.7423357477293709, 'context_precision': 0.6923357477293709, 'citation_accuracy': 0.6944754562746228, 'normalized_cost': 0.1859225816035817, 'normalized_latency': 0.18624185005860378}`
- cost_usd: 0.0037
- latency_ms: 623.49
- status: promote
- notes: MVP simulated run

## exp_2bb1a3f1
- timestamp: 2026-04-12T15:16:54.075110+00:00
- hypothesis: Tester similarity avec chunk_size=800 et top_k=4 pour améliorer le compromis qualité/coût.
- config: `{'retriever_type': 'similarity', 'chunk_size': 800, 'chunk_overlap': 80, 'top_k': 4, 'temperature': 0.2}`
- metrics: `{'faithfulness': 0.660494245836316, 'answer_relevance': 0.7316734739260988, 'context_precision': 0.6816734739260988, 'citation_accuracy': 0.620494245836316, 'normalized_cost': 0.22578942850870443, 'normalized_latency': 0.13473127300032556}`
- cost_usd: 0.0045
- latency_ms: 561.68
- status: discard
- notes: MVP simulated run

## exp_686598a9
- timestamp: 2026-04-12T15:17:08.705009+00:00
- hypothesis: Tester mmr avec chunk_size=600 et top_k=4 pour améliorer le compromis qualité/coût.
- config: `{'retriever_type': 'mmr', 'chunk_size': 600, 'chunk_overlap': 40, 'top_k': 4, 'temperature': 0.2}`
- metrics: `{'faithfulness': 0.7443254850514918, 'answer_relevance': 0.783777533570004, 'context_precision': 0.733777533570004, 'citation_accuracy': 0.7043254850514917, 'normalized_cost': 0.3457428166859008, 'normalized_latency': 0.19291614224680959}`
- cost_usd: 0.0069
- latency_ms: 631.50
- status: baseline
- notes: MVP simulated run

## exp_635ac9f9
- timestamp: 2026-04-12T15:17:08.705835+00:00
- hypothesis: Tester mmr avec chunk_size=400 et top_k=8 pour améliorer le compromis qualité/coût.
- config: `{'retriever_type': 'mmr', 'chunk_size': 400, 'chunk_overlap': 80, 'top_k': 8, 'temperature': 0.0}`
- metrics: `{'faithfulness': 0.7781440786081031, 'answer_relevance': 0.7722276632130292, 'context_precision': 0.7222276632130291, 'citation_accuracy': 0.738144078608103, 'normalized_cost': 0.3427124023377698, 'normalized_latency': 0.253550379718113}`
- cost_usd: 0.0069
- latency_ms: 704.26
- status: keep
- notes: MVP simulated run

## exp_eb89b864
- timestamp: 2026-04-12T15:17:08.706527+00:00
- hypothesis: Tester mmr avec chunk_size=600 et top_k=4 pour améliorer le compromis qualité/coût.
- config: `{'retriever_type': 'mmr', 'chunk_size': 600, 'chunk_overlap': 40, 'top_k': 4, 'temperature': 0.0}`
- metrics: `{'faithfulness': 0.7201995327867133, 'answer_relevance': 0.7634200701728763, 'context_precision': 0.7134200701728762, 'citation_accuracy': 0.6801995327867133, 'normalized_cost': 0.3231703398264524, 'normalized_latency': 0.2399780076576387}`
- cost_usd: 0.0065
- latency_ms: 687.97
- status: discard
- notes: MVP simulated run


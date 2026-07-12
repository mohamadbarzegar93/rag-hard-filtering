# Baseline retrieval example (qualitative)

Query: "14-inch business laptop 16GB RAM"

Top-5 results (pure semantic search, no filter):

1. [BlitzMarkt] BlitzBook 14 Business Edition (score=0.7841)
2. [NordicTech] NordicBook Pro 14 (score=0.8216)
3. [OmniHaul] OmniHaul Marketplace Business Laptop 14-inch (score=0.8752)
4. [NordicTech] NordicBook Air 13 - 8GB RAM, doesn't even match query specs (score=0.9043)
5. [AlpineSupply] AlpineBook Business 14 (score=0.9721)

Observation: 4 different providers appear in the top-5 for a single
query. If the actual use case requires results from one specific
provider only (e.g. a customer chatbot scoped to BlitzMarkt), pure
semantic search has no way to enforce that - it will freely mix in
competitors' near-identical products. This is the exact failure mode
hard-filtering is meant to solve.

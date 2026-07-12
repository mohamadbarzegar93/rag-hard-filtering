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
---

# Hard-filtered retrieval example (same query, provider=BlitzMarkt)

Query: "14-inch business laptop 16GB RAM"
Filter: {"provider": "BlitzMarkt"}

Top-4 results (only 4 returned - BlitzMarkt has 4 products total):

1. [BlitzMarkt] BlitzBook 14 Business Edition (score=0.7841)
2. [BlitzMarkt] BlitzView Office 27 - monitor, not a laptop (score=1.4877)
3. [BlitzMarkt] BlitzView 55 OLED - TV, not a laptop (score=1.6799)
4. [BlitzMarkt] BlitzAudio ANC 300 - headphones, not a laptop (score=1.9685)

Observation: hard filtering correctly restricts every result to
BlitzMarkt (0 wrong-provider results, vs. 4/5 wrong in the baseline
example above). But it also exposes a tradeoff: with `k=5` and only
one true laptop match in BlitzMarkt's catalog, Chroma pads the
remaining slots with BlitzMarkt's next-closest items regardless of
category - producing a monitor, a TV, and headphones as "top-5
matches" for a laptop query. See README "Known limitations" section.

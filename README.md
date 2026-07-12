## Design choices

- **No vendor lock-in**: embeddings are generated locally using an
  open-source model (sentence-transformers `all-MiniLM-L6-v2`) instead
  of a paid API like OpenAI. No API key is required to run this
  project, and it works fully offline after the first model download.

## Challenges encountered

- **LangChain version mismatch**: In the original tutorial example project
 an older LangChain version where `text_splitter`,
  `embeddings`, and `vectorstores` were all bundled into the main
  `langchain` package. The installed version (1.x) has split these
  into separate packages (`langchain-text-splitters`,
  `langchain-huggingface`, `langchain-chroma`, etc.), so imports had
  to be updated accordingly (e.g. `langchain.text_splitter` →
  `langchain_text_splitters`).
## Known limitations / future improvements

- **Fixed `k` regardless of filtered pool size**: when a hard filter
  narrows the candidate pool below `k` (e.g. filtering to a provider
  with only 1-2 matching products), Chroma still returns `k` results
  by padding with the filtered pool's next-closest items - even if
  those items are a different product category entirely (e.g. a
  monitor or TV showing up for a "laptop" query). This produces
  noticeably higher distance scores (>1.0) on those padded results.

  Given the project deadline, this was left as-is rather than adding
  dynamic `k` sizing or a distance-threshold cutoff. A production
  version should either:
  - cap `k` to the actual size of the filtered pool, or
  - drop results above a distance threshold and return fewer than
    `k` when nothing else qualifies.

- **Filter value is provided, not inferred**: in this prototype, the
  provider used for hard-filtering is passed in directly per test
  question (representing a customer already known to belong to one
  provider, e.g. via account/session context). No logic was built to
  *infer* the correct provider from the query text itself when it
  isn't already known.

  In a production system, this would need either:
  - upstream context (session/account state) to supply the filter
    value reliably, as assumed here, or
  - a query-classification step (e.g. a lightweight intent/entity
    extraction pass, or a small classifier) to derive the filter
    from the question text when session context isn't available.

  Given the project deadline, only the first approach was implemented
  and evaluated. Building and evaluating a query-to-filter inference
  step would be a natural next iteration.

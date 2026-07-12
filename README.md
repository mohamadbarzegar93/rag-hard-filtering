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

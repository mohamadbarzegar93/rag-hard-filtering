(German version see below)
# RAG Hard-Filtering Prototype

This project explores a common production RAG problem: pure semantic
search regularly retrieves the wrong document when multiple sources
contain overlapping content. 
The prototype simulates this with synthetic product catalogs from 4
fictitious suppliers (NordicTech, AlpineSupply, BlitzMarkt, OmniHaul)
whose product ranges deliberately overlap - similar laptops,
headphones, and monitors sold under different providers. It compares
two retrieval approaches:

1. **Baseline** - pure semantic search over the whole vector store
2. **Hard-filtered** - a mandatory metadata filter (provider) applied
   before vector search, so a query can never return results outside
   the intended scope

Both approaches are evaluated on the same 25 test questions to
measure how much hard filtering actually improves retrieval accuracy.

## Design choices

- **No vendor lock-in**: embeddings are generated locally using an
  open-source model (sentence-transformers `all-MiniLM-L6-v2`) instead
  of a paid API like OpenAI. No API key is required to run this
  project, and it works fully offline after the first model download.
- **A vector database (ChromaDB) instead of a pretrained end-to-end
  RAG model** (e.g. `facebook/rag-sequence-nq`): metadata filtering
  is standard across vector databases (Chroma, Pinecone, Weaviate,
  etc.), so any of them would support hard filtering. A pretrained
  model like `rag-sequence-nq` is tied to a fixed index (Wikipedia)
  and can't be filtered on custom metadata at all - ruling out that
  whole category of tool. Chroma was chosen for being lightweight,
  local, and simple to set up.

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

## Results

Evaluated on 25 test questions spanning all 4 providers and 5 product categories.

| Metric                          | Baseline | Hard-Filtered |
|----------------------------------|----------|----------------|
| Hit rate @5                      | 100.0%   | 100.0%         |
| Top-1 accuracy                   | 76.0%    | 100.0%         |
| Wrong-provider results at top-1  | 6 / 25   | 0 / 25         |

Full per-question results: [`eval/results/baseline_results.json`](eval/results/base_line_results.json),
[`eval/results/filtered_results.json`](eval/results/filtered_results.json)

## Assessment

Both methods brought up the expected product within the top-5 results
with 100% accuracy which given the small data size is not odd.
**Hard-filtering made the real difference in top-1 result with 100% compared to 
76% accuracy of the baseline model** which means it was wrong in 6 out of 25 questions (24%), while hard filtering
never did, by construction - it cannot physically return a
non-matching provider's product, since the filter is applied before
the vector search even runs.

For a production customer-facing chatbot, top-1 accuracy is what
actually matters: a user asking a question expects the first answer
to be correct, not the third or fourth. On that measure, hard
filtering is a clear and complete fix for the failure mode described
in the task - **wrong-document selection drops from 24% to 0%.**

**2 of the baseline failures:**
Q1: 14-inch business laptop with 16GB RAM
  Expected: NordicTech (NT-001)
  Got:      BlitzMarkt (BM-001)

Q8: ANC headphones made in the EU
  Expected: AlpineSupply (AS-003)
  Got:      NordicTech (NT-003)

## Kurzzusammenfassung (Deutsch)

Dieses Projekt zeigt, wie obligatorisches Hard-Filtering (nach
Anbieter) vor der Vektorsuche die Trefferquote bei mehrdeutigen,
überschneidenden Produktkatalogen verbessert. **Bei reiner semantischer
Suche wählte das System in 24% der Testfragen ein Produkt vom
falschen Anbieter als erste Antwort aus - mit Hard-Filtering sank
diese Quote auf 0%.**

## Ergebnisse & Einschätzung

Evaluiert anhand von 25 Testfragen über alle 4 Anbieter und 5 Produktkategorien hinweg.

| Metrik                              | Baseline | Hard-Filtering |
|--------------------------------------|----------|-----------------|
| Trefferquote @5                      | 100,0 %  | 100,0 %         |
| Top-1-Genauigkeit                    | 76,0 %   | 100,0 %         |
| Falscher Anbieter auf Platz 1        | 6 / 25   | 0 / 25          |

**Einschätzung:** Beide Ansätze finden das richtige Produkt in fast
allen Fällen irgendwo unter den Top-5 (100 % Trefferquote) - das
liegt an der überschaubaren Datenmenge, in der jedes Produkt
mindestens eine semantisch nahe Entsprechung hat. Der entscheidende
Unterschied zeigt sich bei Platz 1: reine semantische Suche wählte in
6 von 25 Fällen (24 %) ein Produkt eines falschen Anbieters als erste
Antwort. Beim Hard-Filtering kann das grundsätzlich nicht passieren,
da der Filter bereits vor der Vektorsuche angewendet wird.

Für einen produktiven Kundenchatbot ist die Top-1-Genauigkeit die
relevante Kennzahl, da Nutzer eine korrekte erste Antwort erwarten.
Hard-Filtering löst das im Task beschriebene Problem (falsches
Dokument wird ausgewählt) hier vollständig - die Fehlerquote sinkt
von 24 % auf 0 %.

## Was ich priorisiere und was ich bewusst weglasse

**Priorisiert:**
- Ein lauffähiger End-to-End-Vergleich zwischen Baseline und
  Hard-Filtering mit echten, reproduzierbaren Zahlen (nicht nur
  Behauptungen) - das war der eigentliche Kern der Aufgabe.
- Eine Vektordatenbank (ChromaDB) statt eines vortrainierten
  End-to-End-RAG-Modells** (z. B. `facebook/rag-sequence-nq`):
  Metadaten-Filterung ist bei Vektordatenbanken Standard (Chroma,
  Pinecone, Weaviate etc.), jede davon hätte Hard-Filtering
  ermöglicht. Ein vortrainiertes Modell wie `rag-sequence-nq` ist
  dagegen an einen festen Index (Wikipedia) gebunden und lässt sich
  nicht nach eigenen Metadaten filtern - diese Kategorie von Tool
  scheidet also grundsätzlich aus. Chroma wurde wegen seiner
  Einfachheit, lokalen Ausführung und leichten Einrichtung gewählt.
- Realistische, überschneidende Testdaten über 4 Anbieter hinweg,
  damit das Problem ("falsches Dokument wird ausgewählt") tatsächlich
  sichtbar wird und nicht nur behauptet werden muss.
- Eine lokale, anbieterunabhängige (kein Vendo-lock-in) Embedding-Lösung (kein API-Key
  nötig) - passend zum Produktionskontext, den ihr beschrieben habt.
- Eine ehrliche Fehleranalyse: konkrete Beispiele, bei denen die
  Baseline versagt, statt nur einer Kennzahlentabelle.

**Bewusst weggelassen:**
- Tuning von Chunk-Größe, Embedding-Modell oder Suchparametern - die
  Standardwerte reichen aus, um den Effekt zu zeigen; eine
  Optimierung hätte Zeit gekostet, ohne die Kernaussage zu verändern.
- Automatische Ableitung des Filterwerts aus der Anfrage selbst - ich
  gehe davon aus, dass der Anbieter aus Session-/Kontodaten bekannt
  ist, wie es in einem echten Chatbot-Kontext üblich wäre.
- Der eigentliche Generierungsschritt (LLM-Antwort auf Basis des
  Kontexts) - der Fokus lag bewusst auf dem Retrieval-Vergleich, da
  genau das im Task gefordert war.
- Hard-Filtering nur nach Anbieter, nicht nach Kategorie oder
  Region: Kategorie und Region wären ebenfalls mögliche
  Filterkriterien gewesen. Da das zugrundeliegende Prinzip bei allen
  dreien identisch ist (Metadaten-Filter vor der Vektorsuche), habe
  ich mich bewusst auf Anbieter beschränkt, um den Kernmechanismus
  klar zu demonstrieren, statt Zeit in die redundante Wiederholung
  des gleichen Konzepts zu investieren. Kategorie- oder Region-Filter
  ließen sich mit der bestehenden Metadatenstruktur (bereits in den
  Produktdaten vorhanden) ohne größere Änderungen ergänzen.

"""
Evaluation script: run all test questions through both the baselin (Semantic Search)
and the hard-filtering approach.
The evaluation is done based on the hit rate of the expected provider in the top 5 results.
and the top-1 accuracy of the expected provider in the 1st result.
"""

#Libraries
import json
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from base_line import search as base_search
from retrieval_filtered import search as filtered_search

TEST_QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "test_questions.json")
RESULTS_PATH = os.path.join(os.path.dirname(__file__), "results")

def load_test_questions():
    with open(TEST_QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate(questions, search_fn, use_filter):
    #Run every question through the provided search function and evaluate the results.
    per_question_results = []
    hits = 0
    top1_correct = 0

    for q in questions:
        query = q['query']
        expected_provider = q['expected_provider']
        expected_product_id = q['expected_product_id']

        if use_filter:
            results = search_fn(query, filters={"provider": expected_provider}, k=5)
        else:
            results = search_fn(query, k=5)
        
        returned_ids = [doc.metadata['product_id'] for doc, _score in results]
        returned_providers = [doc.metadata['provider'] for doc, _score in results]

        is_hit = expected_product_id in returned_ids
        is_top1 = len(returned_ids) > 0 and returned_ids[0] == expected_product_id
        wrong_provider_in_top1 = len(returned_providers) > 0 and returned_providers[0] !=expected_provider

        if is_hit:
            hits += 1
        if is_top1:
            top1_correct += 1
        
        per_question_results.append({
            "id": q["id"],
            "query": query,
            "expected_provider": expected_provider,
            "expected_product_id": expected_product_id,
            "returned_ids": returned_ids,
            "returned_providers": returned_providers,
            "hit": is_hit,
            "top1_correct": is_top1,
            "wrong_provider_in_top1": wrong_provider_in_top1
        })

    total = len(questions)

    summary = {
        "total_questions": total,
        "hit_rate_at_5": hits / total,
        "top1_accuracy": top1_correct / total,
        "wrong_providers_at_top1": sum(
            1 for r in per_question_results if r["wrong_provider_in_top1"]
        ),
        }
    
    return per_question_results, summary

def main():
    os.makedirs(RESULTS_PATH, exist_ok=True)
    questions = load_test_questions()
    print(f"Loaded {len(questions)} test questions.\n")

    print("Runnung baseline (semantic search)...")
    base_line_results, baseline_summary = evaluate(questions, base_search,
                                                    use_filter=False)
    print("Runnung Hard-filtering Search...")
    filtered_results, filtered_summary = evaluate(questions, filtered_search,
                                                    use_filter=True)
    
    #Saving raw per question results
    with open(os.path.join(RESULTS_PATH, "base_line_results.json"), 
              "w", encoding="utf-8") as f:
        json.dump(base_line_results, f, indent = 2, ensure_ascii=False)

    with open(os.path.join(RESULTS_PATH, "filtered_results.json"), 
              "w", encoding="utf-8") as f:
        json.dump(filtered_results, f, indent = 2, ensure_ascii=False)
    
    #Building a comparison summary markdown table

    comparison_md = f"""# Baseline vs. Hard-filtered Retrival


Evaluated on {baseline_summary['total_questions']} test questions.
| Metric                          | Baseline | Hard-Filtered |
|----------------------------------|----------|----------------|
| Hit rate @5                      | {baseline_summary['hit_rate_at_5']:.1%} | {filtered_summary['hit_rate_at_5']:.1%} |
| Top-1 accuracy                   | {baseline_summary['top1_accuracy']:.1%} | {filtered_summary['top1_accuracy']:.1%} |
|| Wrong-provider results at top-1  | {baseline_summary['wrong_providers_at_top1']} / {baseline_summary['total_questions']} | {filtered_summary['wrong_providers_at_top1']} / {filtered_summary['total_questions']} |
"""

    with open(os.path.join(RESULTS_PATH, "comparison_summary.md"), 
          "w", encoding="utf-8") as f:
        f.write(comparison_md)

    print("\n" + comparison_md)
    print(f"Results saved to {RESULTS_PATH}")

if __name__ == "__main__":
    main()



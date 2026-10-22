import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from embeddings.embeddings_generator import generate_query_embedding
from vector_store.chroma_store import retrieve


DATASET = ROOT / "evaluation" / "dataset" / "benchmark.json"


def main():
    with open(DATASET, "r", encoding="utf-8") as file:
        questions = json.load(file)

    questions = [
        q for q in questions
        if q.get("answerable") is True
        and q.get("relevant_chunk_ids")
    ]

    if not questions:
        print("No labelled answerable questions found.")
        return

    k = 5
    results = []

    for item in questions:
        query_vector = generate_query_embedding(item["question"])
        retrieved = retrieve(query_vector, top_k=k)
        retrieved_ids = retrieved["ids"][0]
        relevant_ids = set(item["relevant_chunk_ids"])
        top_ids = retrieved_ids[:k]

        print("Question:", item["question"])
        print("Expected relevant IDs:", sorted(relevant_ids))
        print("Retrieved IDs:", retrieved_ids)

        hit = int(bool(set(top_ids) & relevant_ids))
        precision = len(set(top_ids) & relevant_ids) / len(top_ids) if top_ids else 0
        recall = len(set(top_ids) & relevant_ids) / len(relevant_ids)

        reciprocal_rank = 0
        for rank, chunk_id in enumerate(retrieved_ids, start=1):
            if chunk_id in relevant_ids:
                reciprocal_rank = 1 / rank
                break

        results.append((hit, precision, recall, reciprocal_rank))

    count = len(results)

    print(f"\nEvaluated questions: {count}")
    print(f"Hit Rate@{k}: {sum(r[0] for r in results) / count:.3f}")
    print(f"Precision@{k}: {sum(r[1] for r in results) / count:.3f}")
    print(f"Recall@{k}: {sum(r[2] for r in results) / count:.3f}")
    print(f"MRR: {sum(r[3] for r in results) / count:.3f}")


if __name__ == "__main__":
    main()
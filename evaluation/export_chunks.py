import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vector_store.chroma_store import collection


def main():
    stored = collection.get(
        include=["documents", "metadatas"]
    )

    ids = stored.get("ids") or []
    documents = stored.get("documents") or []
    metadatas = stored.get("metadatas") or []

    chunks = []

    for i, chunk_id in enumerate(ids):
        chunks.append({
            "id": chunk_id,
            "text": documents[i],
            "metadata": metadatas[i]
        })

    output = ROOT / "evaluation" / "dataset" / "chunk_catalog.json"
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Exported {len(chunks)} chunks to {output}")


if __name__ == "__main__":
    main()
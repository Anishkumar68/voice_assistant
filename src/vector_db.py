import chromadb
import os
from src.data_extractor import extract_data_from_file

# Initialize ChromaDB persistent client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="assistant_db")

# Read file
pdf_path = "RAG/Polo Café Bot document 08 Dec 23 Ankit  v.1.0.pdf"
text = extract_data_from_file(pdf_path)

filename = os.path.basename(pdf_path)
doc_id = filename.replace(" ", "_").replace(".pdf", "").lower()

# Check if document is already indexed
try:
    existing = collection.get(ids=[doc_id])
    if existing["documents"]:
        print(f"✅ Already exists: {doc_id}")
    else:
        raise ValueError("ID not found, will add.")
except Exception:
    print(f"➕ Adding new doc: {doc_id}")
    try:
        collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[{"domain": "education", "source": filename}],
        )
        print(f"✅ Added: {doc_id}")
    except Exception as err:
        print(f"❌ Error adding {doc_id}: {err}")


def vector_db_retrieval(query, num_results=5, domain_filter=None, sort_by=None):
    where_filter = {"domain": domain_filter} if domain_filter else None
    results = collection.query(
        query_texts=[query],
        n_results=num_results,
        where=where_filter,
    )
    return results

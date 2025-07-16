import chromadb
import os

from src.data_extractor import extract_pdf_text

# client init
chroma_client = chromadb.Client()

# create a collection
collection = chroma_client.create_collection(name="assistant_db")


pdf_path = os.path.join("RAG", "Achievements Overview.pdf")
text = extract_pdf_text(pdf_path)

# add documents
collection.add(
    ids=["id1"],
    documents=[text],
    metadatas=[{"domain": "education", "source": "Achievements Overview.pdf"}],
)


# query_vector_db_reterival function
def vector_db_retrieval(query, num_results=5, domain_filter=None, sort_by=None):
    where_filter = {"domain": domain_filter} if domain_filter else None
    results = collection.query(
        query_texts=[query],
        n_results=num_results,
        where=where_filter,
    )
    return results

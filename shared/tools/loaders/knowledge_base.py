# yo_ai_main/shared/loaders/knowledge_base.py

from typing import Dict


class KnowledgeBase:
    """
    Wraps loaded documents and provides semantic search + playbook retrieval.
    """

    def __init__(self, documents: Dict[str, str]):
        self.documents = documents
        self.index = self._embed_documents(documents)

    def query(self, text: str) -> str:
        return self._semantic_search(text)

    def get_playbook(self, name: str) -> str | None:
        return self.documents.get(name)

    # ------------------------------------------------------------
    # Internal helpers (stubbed for now — you can plug in your own)
    # ------------------------------------------------------------
    def _embed_documents(self, documents: Dict[str, str]):
        # Placeholder for embeddings
        # Later: plug in sentence-transformers, OpenAI embeddings, etc.
        return documents

    def _semantic_search(self, text: str) -> str:
        # Placeholder for semantic search
        # Later: cosine similarity, vector search, etc.
        return next(iter(self.documents.values()), "")

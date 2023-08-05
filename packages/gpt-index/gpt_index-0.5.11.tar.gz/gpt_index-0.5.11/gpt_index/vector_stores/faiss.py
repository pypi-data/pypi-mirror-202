"""Faiss Vector store index.

An index that that is built on top of an existing vector store.

"""

from typing import Any, Dict, List, Optional, cast

import numpy as np

from gpt_index.vector_stores.types import (
    NodeEmbeddingResult,
    VectorStore,
    VectorStoreQueryResult,
    VectorStoreQuery,
)


class FaissVectorStore(VectorStore):
    """Faiss Vector Store.

    Embeddings are stored within a Faiss index.

    During query time, the index uses Faiss to query for the top
    k embeddings, and returns the corresponding indices.

    Args:
        faiss_index (faiss.Index): Faiss index instance

    """

    stores_text: bool = False

    def __init__(self, faiss_index: Any, save_path: Optional[str] = None) -> None:
        """Initialize params."""
        import_err_msg = """
            `faiss` package not found. For instructions on
            how to install `faiss` please visit
            https://github.com/facebookresearch/faiss/wiki/Installing-Faiss
        """
        try:
            import faiss  # noqa: F401
        except ImportError:
            raise ImportError(import_err_msg)

        self._faiss_index = cast(faiss.Index, faiss_index)
        self._save_path = save_path or "./faiss.json"

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "FaissVectorStore":
        if "faiss_index" in config_dict:
            return cls(**config_dict)
        else:
            save_path = config_dict.get("save_path", None)
            if save_path is not None:
                return cls.load(save_path=save_path)
            else:
                raise ValueError("Missing both faiss index and save path!")

    @property
    def config_dict(self) -> dict:
        """Return config dict."""
        self.save(self._save_path)
        return {"save_path": self._save_path}

    def add(
        self,
        embedding_results: List[NodeEmbeddingResult],
    ) -> List[str]:
        """Add embedding results to index.

        NOTE: in the Faiss vector store, we do not store text in Faiss.

        Args
            embedding_results: List[NodeEmbeddingResult]: list of embedding results

        """
        new_ids = []
        for result in embedding_results:
            text_embedding = result.embedding
            text_embedding_np = np.array(text_embedding, dtype="float32")[np.newaxis, :]
            new_id = str(self._faiss_index.ntotal)
            self._faiss_index.add(text_embedding_np)
            new_ids.append(new_id)
        return new_ids

    @property
    def client(self) -> Any:
        """Return the faiss index."""
        return self._faiss_index

    @classmethod
    def load(cls, save_path: str) -> "FaissVectorStore":
        """Load vector store from disk.

        Args:
            save_path (str): The save_path of the file.

        Returns:
            FaissVectorStore: The loaded vector store.

        """
        import faiss

        faiss_index = faiss.read_index(save_path)
        return cls(faiss_index)

    def save(
        self,
        save_path: str,
    ) -> None:
        """Save to file.

        This method saves the vector store to disk.

        Args:
            save_path (str): The save_path of the file.

        """
        import faiss

        faiss.write_index(self._faiss_index, save_path)

    def delete(self, doc_id: str, **delete_kwargs: Any) -> None:
        """Delete a document.

        Args:
            doc_id (str): document id

        """
        raise NotImplementedError("Delete not yet implemented for Faiss index.")

    def query(
        self,
        query: VectorStoreQuery,
    ) -> VectorStoreQueryResult:
        """Query index for top k most similar nodes.

        Args:
            query_embedding (List[float]): query embedding
            similarity_top_k (int): top k most similar nodes

        """
        query_embedding = cast(List[float], query.query_embedding)
        query_embedding_np = np.array(query_embedding, dtype="float32")[np.newaxis, :]
        dists, indices = self._faiss_index.search(
            query_embedding_np, query.similarity_top_k
        )
        dists = [d for d in dists[0]]
        # if empty, then return an empty response
        if len(indices) == 0:
            return VectorStoreQueryResult(similarities=[], ids=[])

        # returned dimension is 1 x k
        node_idxs = list([str(i) for i in indices[0]])

        return VectorStoreQueryResult(similarities=dists, ids=node_idxs)

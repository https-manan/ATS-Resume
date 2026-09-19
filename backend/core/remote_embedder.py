import numpy as np
from huggingface_hub import InferenceClient


class RemoteEmbedder:
    """
    Drop-in replacement for a local SentenceTransformer instance.
    Calls the fine-tuned model hosted on the Hugging Face Hub via
    the free Inference API instead of loading ~500MB into local RAM.
    """

    def __init__(self, model_id: str, token: str):
        self.model_id = model_id
        self.client = InferenceClient(token=token)

    def encode(self, text: str, convert_to_tensor: bool = False):
        result = self.client.feature_extraction(text, model=self.model_id)
        embedding = np.array(result)

        # Safety net: if the API returns per-token embeddings instead of
        # a single pooled sentence vector, mean-pool them ourselves so the
        # shape matches what the rest of the code expects.
        if embedding.ndim == 2:
            embedding = embedding.mean(axis=0)

        return embedding
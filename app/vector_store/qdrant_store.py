from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings

client = QdrantClient(path="./qdrant_data")


def create_collection_if_not_exists():
    collections = client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    if settings.qdrant_collection_name in collection_names:
        print("Collection already exists.")
        return

    client.create_collection(
        collection_name=settings.qdrant_collection_name,
        vectors_config=VectorParams(
            size=settings.embedding_dimension,
            distance=Distance.COSINE,
        ),
    )

    print("Collection created successfully.")
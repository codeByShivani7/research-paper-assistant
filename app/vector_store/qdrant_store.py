from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct

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


def upsert_chunks(points: list[dict]):
    create_collection_if_not_exists()

    qdrant_points = []

    for point in points:
        qdrant_points.append(
            PointStruct(
                id=point["id"],
                vector=point["vector"],
                payload=point["payload"],
            )
        )

    client.upsert(
        collection_name=settings.qdrant_collection_name,
        points=qdrant_points,
    )

    return {
        "inserted_count": len(qdrant_points)
    }

def search_chunks(query_vector: list[float], limit: int = 5) -> list[dict]:
    create_collection_if_not_exists()

    results = client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_vector,
        limit=limit,
    )

    return [
        {
            "score": result.score,
            "payload": result.payload,
        }
        for result in results.points
    ]
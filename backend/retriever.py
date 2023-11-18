import os
import json

import weaviate


client = weaviate.Client(
    url="https://philai-cluster-nhezpuma.weaviate.network", 
    auth_client_secret=weaviate.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
    additional_headers = {
        "X-Cohere-Api-Key": os.getenv("COHERE_API_KEY")
    }
)


def retrieval(query: str) -> dict:
    return (client.query.get("Project", ["summary", "title", "themeName", "country", "uuid"])
            .with_near_text({"concepts": [query]})
            .with_limit(4)
            .do())


def retrieval_with_id(uuid: str) -> dict:
    return (client.query.get("Project", ["summary", "title", "themeName", "country", "uuid", "activities"])
            .with_where({
                "path": ["uuid"],
                "operator": "Equal",
                "valueText": uuid
            })
            .with_limit(1)
            .do())


def retrieval_with_id_complete(uuid: str) -> dict:
    return (client.query.get("Project", ["summary", "title", "themeName", "country", "imageLink"])
            .with_where({
                "path": ["uuid"],
                "operator": "Equal",
                "valueText": uuid
            })
            .with_limit(1)
            .do())


def fetch_projects(uuids):
    projects = []
    for uuid in uuids:
        if not uuid:
          continue
        response = retrieval_with_id_complete(uuid)
        projects.append(response["data"]["Get"]["Project"][0])
    return projects
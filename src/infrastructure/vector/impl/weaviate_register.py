# import weaviate
# from .vector_database_plugin import VectorDatabasePlugin
#
# class WeaviatePlugin(VectorDatabasePlugin):
#     def __init__(self, url="http://localhost:8080"):
#         self.client = weaviate.Client(url=url)
#         self.classes = set()
#
#     def connect(self, class_name: str):
#         if class_name not in self.classes:
#             schema = {
#                 "classes": [{
#                     "class": class_name,
#                     "description": "Text Embeddings",
#                     "properties": [{
#                         "name": "embedding",
#                         "dataType": ["number[]"],
#                         "description": "The embedding of the text"
#                     }]
#                 }]
#             }
#             self.client.schema.create(schema)
#             self.classes.add(class_name)
#
#     def add_embedding(self, embedding, class_name: str):
#         data_object = {
#             "embedding": embedding.tolist()
#         }
#         self.client.data_object.create(data_object, class_name)
#
#     def search_embeddings(self, query_embedding, class_name: str, k=5):
#         near_vector = {
#             "concepts": query_embedding.tolist(),
#             "vector": query_embedding.tolist()
#         }
#         response = (
#             self.client.query.get(class_name, ["_additional { id distance }"])
#             .with_near_vector(near_vector)
#             .with_limit(k)
#             .do()
#         )
#         results = response["data"]["Get"][class_name]
#         distances = [item["_additional"]["distance"] for item in results]
#         ids = [item["_additional"]["id"] for item in results]
#         return {"distances": distances, "ids": ids}
#
#
#


# import weaviate
# from .vector_database_plugin import VectorDatabasePlugin
#
# class WeaviatePlugin(VectorDatabasePlugin):
#     def __init__(self, url="http://localhost:8080"):
#         self.client = weaviate.Client(url=url)
#         self.classes = set()
#
#     def connect(self, class_name: str):
#         if class_name not in self.classes:
#             schema = {
#                 "classes": [{
#                     "class": class_name,
#                     "description": "Text Embeddings",
#                     "properties": [{
#                         "name": "embedding",
#                         "dataType": ["number[]"],
#                         "description": "The embedding of the text"
#                     }]
#                 }]
#             }
#             self.client.schema.create(schema)
#             self.classes.add(class_name)
#
#     def add_embedding(self, embedding, class_name: str):
#         data_object = {
#             "embedding": embedding.tolist()
#         }
#         self.client.data_object.create(data_object, class_name)
#
#     def search_embeddings(self, query_embedding, class_name: str, k=5):
#         near_vector = {
#             "concepts": query_embedding.tolist(),
#             "vector": query_embedding.tolist()
#         }
#         response = (
#             self.client.query.get(class_name, ["_additional { id distance }"])
#             .with_near_vector(near_vector)
#             .with_limit(k)
#             .do()
#         )
#         results = response["data"]["Get"][class_name]
#         distances = [item["_additional"]["distance"] for item in results]
#         ids = [item["_additional"]["id"] for item in results]
#         return {"distances": distances, "ids": ids}




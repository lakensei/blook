from pymilvus import MilvusClient

from ...base import BaseRegister


# class MilvusRegister(BaseRegister):
#     def __init__(self, host="localhost", port="19530"):
#         self.host = host
#         self.port = port
#         self.collections = {}
#
#     def connect(self, collection_name: str):
#         if collection_name not in self.collections:
#             connections.connect("default", host=self.host, port=self.port)
#             fields = [
#                 FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#                 FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
#                 # Adjust dimension based on your model
#             ]
#             schema = CollectionSchema(fields, description="Text Embeddings")
#
#             if collection_name not in [col.name for col in Collection.list_collections()]:
#                 collection = Collection(name=collection_name, schema=schema)
#                 index_params = {"index_type": "IVF_FLAT", "params": {"nlist": 128}, "metric_type": "L2"}
#                 collection.create_index(field_name="embedding", index_params=index_params)
#                 collection.load()
#             else:
#                 collection = Collection(name=collection_name)
#
#             self.collections[collection_name] = collection
#
#     def check_collection(self, collection_name: str):
#         if collection_name not in self.collections:
#             raise ValueError(f"Unsupported collection name: {collection_name}")
#
#     def add_embedding(self, embedding, collection_name: str):
#         self.check_collection(collection_name)
#         data = [[np.array(embedding).tolist()]]
#         self.collections[collection_name].insert(data)
#         self.collections[collection_name].flush()
#
#     def search_embeddings(self, query_embedding, collection_name: str, k=5):
#         self.check_collection(collection_name)
#         search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
#         results = self.collections[collection_name].search([query_embedding], anns_field="embedding",
#                                                            param=search_params, limit=k)
#         distances = [result.distance for result in results[0]]
#         ids = [result.id for result in results[0]]
#         return {"distances": distances, "ids": ids}
#
#     """
#     from pymilvus import connections, db
#     database = db.create_database("my_database")
#
#     db.using_database("my_database")
#
#     db.list_database()
#     db.drop_database("my_database")
#
#     """


class MilvusRegister(BaseRegister):
    def __init__(self, host="localhost", port="19530"):
        self.host = host
        self.port = port
        self.clients = {}

    def connect(self, collection_name: str):
        if collection_name not in self.clients:
            client = MilvusClient(host=self.host, port=self.port)
            self.clients[collection_name] = client

            # Check if the collection exists, create it if not

            # collections = client.list_collections()
            # if collection_name not in collections:
            if not client.has_collection(collection_name):
                fields = [
                    {"name": "id", "type": "int64", "is_primary": True, "auto_id": True},
                    {"name": "embedding", "type": "float_vector", "dim": 384}  # Adjust dimension based on your model
                ]
                # fields = [
                #     FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                #     FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
                #     # Adjust dimension based on your model
                # ]
                client.create_collection(collection_name, fields)

                # Create index
                index_params = {
                    "index_type": "IVF_FLAT",
                    "params": {"nlist": 128},
                    "metric_type": "L2"
                }
                client.create_index(collection_name, field_name="embedding", index_params=index_params)

            # Load collection
            client.load_collection(collection_name)

    def check_collection(self, collection_name: str):
        if collection_name not in self.clients:
            raise ValueError(f"Unsupported collection name: {collection_name}")

    def add_embedding(self, embedding, collection_name: str):
        self.check_collection(collection_name)

        client = self.clients[collection_name]
        data = [[embedding.tolist()]]
        client.insert(collection_name, data)

    def update_embedding(self):
        ...

    def search_embeddings(self, query_embedding, collection_name: str, k=5):
        self.check_collection(collection_name)

        client = self.clients[collection_name]
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = client.search(collection_name, [query_embedding.tolist()], params=search_params, limit=k)
        distances = [result['distance'] for result in results]
        ids = [result['id'] for result in results]
        return {"distances": distances, "ids": ids}

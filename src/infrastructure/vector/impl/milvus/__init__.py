from .register import MilvusRegister


def init_register():
    from ...vector_registry import VectorRegistry
    VectorRegistry.register(
        "milvus",
        MilvusRegister
    )


__all__ = [
    "init_register",
]

#!/usr/bin/env python3
"""module docs"""


def insert_school(mongo_collection, **kwargs) -> str:
    """insert a document in a collection based on kwargs"""
    return mongo_collection.insert_one(kwargs).inserted_id

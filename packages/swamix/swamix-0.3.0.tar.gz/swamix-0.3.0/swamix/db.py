from typing import Any
import pymongo
from pymongo.collection import Collection
from contextlib import suppress
from bson import ObjectId


class _Database:
    def __init__(self, db):
        self.db = db

    def __getitem__(self, item):
        return _Collection(self.db[item])

    def __setitem__(self, key, value):
        pass


class _Client:
    def __init__(self, url, db="test", collection="test"):
        self.client = pymongo.MongoClient(url)

    def __getitem__(self, item):
        return _Database(self.client[item])


class _QueryResult:
    def __init__(self, cursor):
        self.cursor = cursor

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop
            step = key.step or 1

            cursor = self.cursor
            if start:
                cursor = cursor.skip(start)
            if stop:
                cursor = cursor.limit(stop - (start or 0))
            if step == -1:
                cursor = cursor.sort("_id", pymongo.DESCENDING)

            return list(cursor)

        return list(self.cursor)[key]

    def __iter__(self):
        return self.cursor

    def __list__(self):
        return list(self.cursor)

    def __str__(self):
        return str(list(self.cursor))


class _Collection(Collection):
    """override read write methods while inheriting all default Collection methods"""

    def __init__(self, collection: Collection, selector_mode="one"):
        super().__init__(collection.database, collection.name)
        self.collection = collection
        self.selector_mode = selector_mode
        self.last_inserted = None  # Add this attribute

    def _parse_query_string(self, query_str: str):
        # Handle different operators
        compound_operators = {">=": "$gte", "<=": "$lte", "!=": "$ne", "~=": "$regex", "*=": "$regex"}
        simple_operators = {"=": "$eq", ">": "$gt", "<": "$lt"}

        # Try compound operators first
        op = next((op for op in compound_operators if op in query_str), None)
        if op:
            field, value = [x.strip() for x in query_str.split(op, 1)]
        else:
            # Try simple operators if no compound operator found
            op = next((op for op in simple_operators if op in query_str), None)
            if not op:
                # If no operator found, treat it as an ID lookup
                with suppress(Exception):
                    return {"_id": ObjectId(query_str.strip())}
                return {"_id": query_str.strip()}

            field, value = [x.strip() for x in query_str.split(op, 1)]

        # Handle different value types
        with suppress(ValueError):
            value = int(value)
        if isinstance(value, str):
            with suppress(ValueError):
                value = float(value)

        if isinstance(value, str):
            # Remove quotes if present
            value = value.strip("'\"")

            if op == "~=":
                return {field: {"$regex": value, "$options": "i"}}
            elif op == "*=":
                return {field: {"$regex": value}}

        # Build MongoDB query for numeric/exact comparisons
        operators = {**compound_operators, **simple_operators}
        if op in operators:
            return {field: {operators[op]: value}}

    def print(self, limit=10, reversed=False):
        for item in self.collection.find().limit(limit).sort("_id", pymongo.DESCENDING if reversed else pymongo.ASCENDING):
            print(item)

    def __iadd__(self, other):
        if isinstance(other, list):
            result = self.collection.insert_many(other)
            self.last_inserted = _QueryResult(self.collection.find({"_id": {"$in": result.inserted_ids}}))
        else:
            result = self.collection.insert_one(other)
            self.last_inserted = _QueryResult(self.collection.find({"_id": result.inserted_id}))
        return self  # Return self for the += operator

    def __getitem__(self, query_str):
        if isinstance(query_str, str):
            query = self._parse_query_string(query_str)
            return _QueryResult(self.collection.find(query))
        return _QueryResult(self.collection.find(query_str))

    def __getattribute__(self, name):
        if name == "many":
            print('many mode activated')
            return _Collection(self.collection, "many")
        else:
            return object.__getattribute__(self, name)

    def __str__(self):
        return str(list(self.collection.find()))


def mongo(url="mongodb://localhost:27017/"):
    return _Client(url)


if __name__ == "__main__":
    db = mongo()
    c = db["test"]["employees"]

    # Add test data

    # Example queries with slicing
    print("\nCase insensitive match with slice:")
    results = c["name ~= john"]
    print(results[0:2])  # First 2 matches

    print("\nReverse age query:")
    print(c["age >= 30"][::-1])  # All matches in reverse order

    print("\nSkip and limit:")
    print(c["age < 65"][0:5])  # Skip 2, get next 2

    # Can still use native Collection methods
    print("\nNative count:")
    print(c.count_documents({"age": {"$gte": 30}}))

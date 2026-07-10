"""
Provides easy access to schema definitions.
"""


class SchemaManager:

    def __init__(self, schema):
        self.schema = schema

    def field(self, name):
        return self.schema["source_columns"].get(name, {})

    def valid_values(self, name):
        return self.field(name).get("valid_values", {})

    def required(self, name):
        return self.field(name).get("required", False)

    def datatype(self, name):
        return self.field(name).get("datatype")

    def minimum(self, name):
        return self.field(name).get("minimum")

    def maximum(self, name):
        return self.field(name).get("maximum")
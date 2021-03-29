import os

import jsonschema
from bson import json_util
from jsonschema import exceptions


class DataValidator(object):

    def __init__(self):
        self.courier_schema = _load_schema('courier_schema.json')
        self.order_schema = _load_schema('order_schema.json')
        self.order_assign_schema = _load_schema('order_assign_schema.json')
        self.order_complete_schema = _load_schema('order_complete_schema.json')

    def validate_courier(self, courier_data: dict) -> bool:
        try:
            jsonschema.validate(courier_data, self.courier_schema)
            return True
        except exceptions.ValidationError:
            return False

    def validate_order(self, order_data: dict) -> bool:
        try:
            jsonschema.validate(order_data, self.order_schema)
            return True
        except exceptions.ValidationError:
            return False

    def validate_order_assign(self, order_assign_data: dict) -> bool:
        try:
            jsonschema.validate(order_assign_data, self.order_assign_schema)
            return True
        except exceptions.ValidationError:
            return False

    def validate_order_complete(self, order_complete_data: dict) -> bool:
        try:
            jsonschema.validate(order_complete_data, self.order_complete_schema)
            return True
        except exceptions.ValidationError:
            return False


def _load_schema(schema_name: str) -> dict:
    with open(os.path.join(os.path.dirname(__file__), 'schemas', schema_name)) as f:
        return json_util.loads(f.read())


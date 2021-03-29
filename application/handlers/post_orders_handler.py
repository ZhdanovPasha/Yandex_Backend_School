from pymongo.database import Database
from pymongo.results import InsertManyResult
from pymongo.errors import PyMongoError
from ..data_validator import DataValidator
from werkzeug.exceptions import BadRequest
from typing import Tuple


def _write_to_db(orders_data, db: Database) -> Tuple[dict, int]:
    bad_orders = []
    if 'data' not in orders_data:
        raise BadRequest('Content-Type must contain "data" key')
    data_validator = DataValidator()
    for idx, order in enumerate(orders_data['data']):
        if not data_validator.validate_order(order) or db['orders'].find_one(order['order_id']) is not None:
            bad_orders.append(order)

    if not bad_orders:
        orders = orders_data['data'].copy()
        for order in orders:
            order['_id'] = order.pop('order_id')
            order['is_used'] = False
        db_response: InsertManyResult = db['orders'].insert_many(orders)
        if db_response.acknowledged:
            response = {'orders':
                [
                    {'id': order['_id']} for order in orders
                ]
            }
            return response, 201
        else:
            raise PyMongoError('Operation was not acknowledged')
    else:
        response = {
            'validation_error':
                {
                    'orders':
                        [{'id': order['order_id']} for order in bad_orders if 'order_id' in order]
                }
        }
        return response, 400


def post_orders(orders_data: dict, db: Database) -> Tuple[dict, int]:
    return _write_to_db(orders_data, db)
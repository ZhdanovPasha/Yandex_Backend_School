from pymongo.database import Database
from werkzeug.exceptions import BadRequest
from application.data_validator import DataValidator
from typing import Tuple


def _write_to_db(orders_complete_data: dict, db: Database) -> Tuple[dict, int]:
    data_validator = DataValidator()

    if not data_validator.validate_order_complete(orders_complete_data):
        raise BadRequest('Wrong json structure')

    courier_id = orders_complete_data['courier_id']
    courier = db['couriers'].find_one({'_id': courier_id})
    if not courier:
        raise BadRequest('Wrong courier id')

    order_id = orders_complete_data['order_id']
    if not db['orders'].find_one({'_id': order_id}):
        raise BadRequest('Wrong order id')
    if str(order_id) not in courier['orders']:
        raise BadRequest('Courier did not work with this order')

    courier['orders'].pop(str(order_id), None)
    db['couriers'].replace_one({'_id': courier_id}, courier)
    response = {
        'order_id': order_id
    }

    return response, 200


def post_orders_complete(orders_complete_data: dict, db: Database) -> Tuple[dict, int]:
    return _write_to_db(orders_complete_data, db)

from pymongo.database import Database
from typing import Tuple
from werkzeug.exceptions import BadRequest
from application.handlers.utils_handler import _can_courier_take_order


def _write_to_db(courier_id: int, patch_data: dict, db: Database) -> Tuple[dict, int]:
    courier = db['couriers'].find_one({"_id": courier_id})
    if not courier:
        raise BadRequest('Content must contain courier_id in database')
    allowed_fields = {'courier_type', 'regions', 'working_hours'}
    for key in patch_data:
        if key not in allowed_fields:
            raise BadRequest(f'Unknown key {key}')

    for key, value in patch_data.items():
        courier[key] = value
    prev_orders = courier['orders']
    courier['orders'] = {}
    for order_num, timestamp in prev_orders.items():
        order = db['orders'].find_one({'_id': int(order_num)})
        order['is_used'] = False
        if _can_courier_take_order(courier, order):
            courier['orders'][order_num] = timestamp
        else:
            db['orders'].replace_one({'_id': int(order_num)}, order)

    db['couriers'].replace_one({'_id': courier_id}, courier)
    response_keys = ['courier_type', 'regions', 'working_hours']
    response = {key: courier[key] for key in response_keys}
    response['courier_id'] = courier['_id']
    return response, 200


def patch_courier(courier_id: int, patch_data: dict, db: Database) -> Tuple[dict, int]:
    return _write_to_db(courier_id, patch_data, db)

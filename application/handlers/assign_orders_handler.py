from pymongo.database import Database
from werkzeug.exceptions import BadRequest
from application.handlers.utils_handler import _can_courier_take_order, _get_current_time
from typing import Tuple


def _write_to_db(orders_assign_data: dict, db: Database) -> Tuple[dict, int]:
    if list(orders_assign_data.keys()) != ['courier_id']:
        raise BadRequest('Incorrect json structure')
    courier = db['couriers'].find_one({"_id": orders_assign_data['courier_id']})
    if not courier:
        raise BadRequest('Courier id does not exist')
    orders = db['orders'].find()

    final_orders = []
    for order in orders:
        if _can_courier_take_order(courier, order):
            final_orders.append(order)

    if not final_orders:
        return {}, 200

    current_time = _get_current_time()
    for order in final_orders:
        order['is_used'] = True
        db['orders'].replace_one({'_id': order['_id']}, order)

    for order in final_orders:
        courier['orders'][str(order['_id'])] = current_time
    db['couriers'].replace_one({"_id": courier['_id']}, courier)
    response = {
        'orders':
            [{'id': order['_id']} for order in final_orders],
        'assign_time': current_time
    }

    return response, 200


def post_orders_assign(orders_assign_data: dict, db: Database) -> Tuple[dict, int]:
    return _write_to_db(orders_assign_data, db)


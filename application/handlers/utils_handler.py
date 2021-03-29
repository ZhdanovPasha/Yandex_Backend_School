from datetime import datetime
from typing import Tuple


def _get_current_time() -> str:
    current_time = datetime.now()
    return current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4] + "Z"


def _convert_time_to_minutes(current_time: str) -> int:
    hours, minutes = current_time.split(':')
    return int(hours) * 60 + int(minutes)


def _parse_interval(current_interval: str) -> Tuple [int, int]:
    start_time, end_time = current_interval.split('-')
    return _convert_time_to_minutes(start_time), _convert_time_to_minutes(end_time)


def _are_intersects(lhs, rhs) -> bool:
    return rhs[0] <= lhs[0] <= rhs[1] or lhs[0] <= rhs[0] <= lhs[1]


def _can_courier_take_order(courier: dict, order: dict) -> bool:
    weight_dict = {
        'foot': 10,
        'bike': 15,
        'car': 50
    }

    if order['is_used']:
        return False

    if order['weight'] > weight_dict[courier['courier_type']]:
        return False

    if order['region'] not in courier['regions']:
        return False

    in_time = False
    for order_time in order['delivery_hours']:
        for courier_time in courier['working_hours']:
            if _are_intersects(_parse_interval(order_time), _parse_interval(courier_time)):
                in_time = True
                break

    return in_time

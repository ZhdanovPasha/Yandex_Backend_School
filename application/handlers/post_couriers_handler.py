from typing import Tuple

from pymongo.database import Database
from pymongo.errors import PyMongoError
from pymongo.results import InsertManyResult
from ..data_validator import DataValidator
from werkzeug.exceptions import BadRequest


def _write_to_db(couriers_data: dict, db: Database) -> Tuple[dict, int]:
    bad_couriers = []
    data_validator = DataValidator()
    if 'data' not in couriers_data:
        raise BadRequest('Content-Type must contain "data" key')
    allowed_fields = {'foot', 'bike', 'car'}
    for idx, courier in enumerate(couriers_data['data']):
        if not data_validator.validate_courier(courier) or \
            db['couriers'].find_one(courier['courier_id']) is not None or courier['courier_type'] not in allowed_fields:
            bad_couriers.append(courier)

    if not bad_couriers:
        couriers = couriers_data['data'].copy()
        for courier in couriers:
            courier['_id'] = courier.pop('courier_id')
            courier['orders'] = dict()
        db_response: InsertManyResult = db['couriers'].insert_many(couriers)
        if db_response.acknowledged:
            response = {'couriers':
                            [
                                {'id': courier['_id']} for courier in couriers
                            ]
                        }
            return response, 201
        else:
            raise PyMongoError('Operation was not acknowledged')
    else:
        response = {
            'validation_error':
                {
                    'couriers':
                    [{'id': courier['courier_id']} for courier in bad_couriers if 'courier_id' in courier]
                }
            }
        return response, 400


def post_couriers(couriers_data: dict, db: Database) -> Tuple[dict, int]:
    return _write_to_db(couriers_data, db)
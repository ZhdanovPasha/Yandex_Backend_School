import json
import logging

from flask import Flask, request, Response
from pymongo.database import Database
from werkzeug.exceptions import BadRequest

from application.handlers.post_couriers_handler import post_couriers
from application.handlers.post_orders_handler import post_orders
from application.handlers.patch_couriers_handler import patch_courier
from application.handlers.assign_orders_handler import post_orders_assign
from application.handlers.complete_orders_handler import post_orders_complete

logger = logging.getLogger(__name__)


def make_app(db: Database) -> Flask:
    app = Flask(__name__)

    @app.route('/couriers', methods=['POST'])
    def couriers():
        if not request.is_json:
            raise BadRequest('Content-Type must beg application/json')

        couriers_data = request.get_json()
        data, status = post_couriers(couriers_data, db)
        return Response(json.dumps(data, ensure_ascii=False), status, mimetype='application/json; charset=utf-8')

    @app.route('/couriers/<int:courier_id>', methods=['PATCH'])
    def change_courier(courier_id: int):
        if not request.is_json:
            raise BadRequest('Content-Type must be application/json')

        patch_data = request.get_json()
        data, status = patch_courier(courier_id, patch_data, db)
        return Response(json.dumps(data, ensure_ascii=False), status, mimetype='application/json; charset=utf-8')

    @app.route('/orders', methods=['POST'])
    def orders():
        if not request.is_json:
            raise BadRequest('Content-Type must be application/json')

        orders_data = request.get_json()
        data, status = post_orders(orders_data, db)
        return Response(json.dumps(data, ensure_ascii=False), status, mimetype='application/json; charset=utf-8')

    @app.route('/orders/assign', methods=['POST'])
    def orders_assign():
        if not request.is_json:
            raise BadRequest('Content-Type must be application/json')

        orders_assign_data = request.get_json()
        data, status = post_orders_assign(orders_assign_data, db)
        return Response(json.dumps(data, ensure_ascii=False), status, mimetype='application/json; charset=utf-8')

    @app.route('/orders/complete', methods=['POST'])
    def orders_complete():
        if not request.is_json:
            raise BadRequest('Content-Type must be application/json')

        orders_complete_data = request.get_json()
        data, status = post_orders_complete(orders_complete_data, db)
        return Response(json.dumps(data, ensure_ascii=False), status, mimetype='application/json; charset=utf-8')

    return app

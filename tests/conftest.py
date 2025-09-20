import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.helpers import OrderHelper, CourierHelper, delete_created_courier, wait_until_condition
from data.test_data_generator import generate_courier_data, generate_order_data

@pytest.fixture
def courier_data():
    data = generate_courier_data()
    yield data
    try:
        delete_created_courier(data)
    except Exception as e:
        print(f"Ошибка при удалении курьера: {e}")

@pytest.fixture
def setup_and_teardown_courier():
    courier_helper = CourierHelper()
    create_courier_data = courier_helper.create_courier()
    yield create_courier_data
    try:
        courier_id = courier_helper.login_courier(create_courier_data["login"], create_courier_data["password"])
        courier_helper.delete_courier(courier_id)
    except Exception as e:
        print(f"Ошибка при удалении курьера: {e}")

@pytest.fixture
def setup_and_teardown_order_with_track():
    order_helper = OrderHelper()
    order_data = generate_order_data()
    response = order_helper.create_order(order_data)
    order_track = response.json()['track']

    yield order_track

    try:
        order_id = order_helper.get_order_by_track(order_track).json()["order"]["id"]
        order_helper.cancel_order(order_id)
    except Exception as e:
        print(f"Ошибка при удалении заказа: {e}")

@pytest.fixture(scope="function")
def setup_orders_for_list_tests():
    courier_helper = CourierHelper()
    order_helper = OrderHelper()
    new_courier = courier_helper.create_courier()
    courier_id = courier_helper.login_courier(new_courier["login"], new_courier["password"])
    orders = []

    try:
        for _ in range(5):
            order_data = generate_order_data()
            response = order_helper.create_order(order_data)
            track = response.json()['track']
            
            wait_until_condition(
                lambda: order_helper.get_order_by_track(track).status_code == 200,
                timeout=30
            )
            
            order_details = order_helper.get_order_by_track(track)
            order_id = order_details.json()["order"]["id"]
            orders.append({"track": track, "id": order_id})

        order_helper.accept_orders([order['id'] for order in orders[:3]], courier_id)
        order_helper.complete_orders([order['id'] for order in orders[:2]])

        yield courier_id, orders

    finally:
        for order in orders:
            try:
                order_helper.cancel_order(order['id'])
            except Exception as e:
                print(f"Ошибка при удалении заказа {order['id']}: {e}")
        courier_helper.delete_courier(courier_id)

@pytest.fixture
def courier_for_deletion():
    courier_helper = CourierHelper()
    courier_for_del = courier_helper.create_courier()
    courier_id = courier_helper.login_courier(courier_for_del["login"], courier_for_del["password"])
    
    yield courier_id
    
    try:
        courier_helper.delete_courier(courier_id)
    except Exception as e:
        print(f"Ошибка при удалении курьера: {e}")

@pytest.fixture
def order_and_courier_setup():
    courier_helper = CourierHelper()
    order_helper = OrderHelper()
    test_courier_data = courier_helper.create_courier()
    courier_id = courier_helper.login_courier(test_courier_data["login"], test_courier_data["password"])
    order_info = generate_order_data()
    
    try:
        order_response = order_helper.create_order(order_info)
        order_track = order_response.json()['track']
        
        wait_until_condition(
            lambda: order_helper.get_order_by_track(order_track).status_code == 200,
            timeout=30
        )
        
        order_data = order_helper.get_order_by_track(order_track)
        order_id = order_data.json()["order"]["id"]

        yield order_id, courier_id

    finally:
        try:
            order_helper.cancel_order(order_id)
        except Exception as e:
            print(f"Ошибка при удалении заказа: {e}")
        courier_helper.delete_courier(courier_id)

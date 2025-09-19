import os
import sys
import time

import pytest

from data.helpers import OrderHelper, CourierHelper, delete_created_courier
from data.test_data_generator import generate_courier_data, generate_order_data

# Добавляем корневую директорию проекта в PYTHONPATH.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def wait_until_condition(condition_func, timeout=30, interval=1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)
    raise TimeoutError("Condition not met within timeout")

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
    # Setup
    create_courier_data = CourierHelper.create_courier()
    yield create_courier_data
    # Teardown
    try:
        courier_id = CourierHelper.login_courier(create_courier_data["login"], create_courier_data["password"])
        CourierHelper.delete_courier(courier_id)
    except Exception as e:
        print(f"Ошибка при удалении курьера: {e}")

@pytest.fixture
def setup_and_teardown_order_with_track():
    order_helper = OrderHelper()
    order_data = generate_order_data()
    response = order_helper.create_order(order_data)
    order_track = response.json()['track']

    yield order_track

# из-за бага api заказ невозможно отменить
# if order_track:
#     order_helper.cancel_order(order_track)

@pytest.fixture(scope="function")
def setup_orders_for_list_tests():
    courier_helper = CourierHelper()
    order_helper = OrderHelper()

    # Создание курьера
    new_courier = courier_helper.create_courier()
    courier_id = courier_helper.login_courier(new_courier["login"], new_courier["password"])

    # Создание 5 заказов
    orders = []
    for _ in range(5):
        order_data = generate_order_data()
        response = order_helper.create_order(order_data)
        track = response.json()['track']
        
        # Ожидание появления заказа
        wait_until_condition(
            lambda: order_helper.get_order_by_track(track).status_code == 200,
            timeout=30
        )
        
        order_details = order_helper.get_order_by_track(track)
        order_id = order_details.json()["order"]["id"]
        orders.append({"track": track, "id": order_id})

    # Принятие курьером 3 заказов
    for order in orders[:3]:
        wait_until_condition(
            lambda: order_helper.accept_order(order['id'], courier_id).status_code == 200,
            timeout=30
        )
    
    # Завершение 2 заказов
    for order in orders[:2]:
        wait_until_condition(
            lambda: order_helper.complete_order(order['id']).status_code == 200,
            timeout=30
        )

    yield courier_id, orders

    # Teardown
    courier_helper.delete_courier(courier_id)

@pytest.fixture
def courier_for_deletion():
    # Setup
    courier_for_del = CourierHelper.create_courier()
    courier_id = CourierHelper.login_courier(courier_for_del["login"], courier_for_del["password"])
    return courier_id  # Удаление будет в тесте

@pytest.fixture
def order_and_courier_setup():
    courier_helper = CourierHelper()
    order_helper = OrderHelper()

    # Создаем курьера
    test_courier_data = courier_helper.create_courier()
    courier_id = courier_helper.login_courier(test_courier_data["login"], test_courier_data["password"])

    # Создаем заказ с ожиданием
    order_info = generate_order_data()
    order_response = order_helper.create_order(order_info)
    order_track = order_response.json()['track']
    
    wait_until_condition(
        lambda: order_helper.get_order_by_track(order_track).status_code == 200,
        timeout=30
    )
    
    order_data = order_helper.get_order_by_track(order_track)
    order_id = order_data.json()["order"]["id"]

    yield order_id, courier_id

    # Teardown
    courier_helper.delete_courier(courier_id)

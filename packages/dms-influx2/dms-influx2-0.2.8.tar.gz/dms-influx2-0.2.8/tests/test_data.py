import pytest

from dms_influx2.lib import DmsInflux2
from datetime import datetime, timedelta
from dotenv import dotenv_values
from time import sleep
from dateutil.parser import parse

from dms_influx2.utils import localize_dt

config = dotenv_values()

host = config['INFLUX_HOST']
port = config['INFLUX_PORT']
token = config['DOCKER_INFLUXDB_INIT_ADMIN_TOKEN']
org = config['DOCKER_INFLUXDB_INIT_ORG']
url = f'http://{host}:{port}'

client = DmsInflux2(url=url, token=token, org=org)

bucket = 'test_bucket_12345'
bucket_trash = f"{bucket}_trash_{datetime.now().year}"
measurement = "test"
device_id = "test.ch"
description = "some test"
start = 0
n_samples = 10000
test_data = {
    "measurement": measurement,
    "device_id": device_id,
    "description": description,
    "values": [(datetime.now() - timedelta(minutes=i), i) for i in range(start, n_samples)]
}


@pytest.fixture(scope='session')
def init():
    if not client.ping():
        pytest.exit('Unable to connect to influx database')
    if client.buckets_api().bucket_exists(bucket_name=bucket):
        client.buckets_api().delete_bucket_by_name(bucket_name=bucket)
    client.buckets_api().create_bucket(bucket_name=bucket)
    client.save_data(bucket=bucket, data=test_data)
    yield
    client.buckets_api().delete_bucket_by_name(bucket_name=bucket)


def test_health():
    health = client.ping()
    assert health


def test_create_delete_bucket(init):
    bucket_name = 'abrakadabra'
    client.buckets_api().create_bucket(bucket_name=bucket_name)
    client.buckets_api().delete_bucket_by_name(bucket_name=bucket_name)
    assert client.buckets_api().bucket_exists(bucket_name) is False


def test_list_measurements(init):
    data = client.list_measurements(bucket=bucket)
    assert measurement in data


def test_list_device_ids(init):
    data = client.list_device_ids(bucket=bucket)
    assert device_id in data


def test_list_descriptions(init):
    data = client.list_descriptions(bucket=bucket, measurement=measurement)
    assert data == [description]

    data = client.list_descriptions(bucket=bucket)
    assert data == [description]


def test_get_values_count_combined(init):
    data = client.get_values_count_combined(bucket=bucket, measurement=measurement, device_id=device_id)
    assert data == n_samples


def test_get_values_count(init):
    data = client.get_values_count(bucket=bucket, measurement=measurement, device_id=device_id)
    assert data[device_id] == n_samples


def test_get_metadata(init):
    data = client.get_metadata(bucket=bucket, measurement=measurement, device_id=device_id)
    print(data)
    assert data[0]['device_id'] == device_id
    assert data[0]['values_count'] == n_samples
    assert data[0]['timestamp'] == str(test_data['values'][0][0])
    assert data[0]['value'] == test_data['values'][0][1]


def test_get_first_value(init):
    data = client.get_one_value(bucket=bucket, measurement=measurement, last=False)
    assert data[0]['value'] == test_data['values'][-1][1]


def test_get_last_value(init):
    data = client.get_one_value(bucket=bucket, measurement=measurement, last=True)
    assert data[0]['value'] == start


def test_get_last_value_sort(init):
    # Get last value with sorting (asc or desc)
    d1 = {'measurement': 'test1', 'device_id': 'test.1', 'unit': 't',
          'values': [(datetime.now() - timedelta(hours=2), 0)]}
    d2 = {'measurement': 'test1', 'device_id': 'test.2', 'unit': 't',
          'values': [(datetime.now() - timedelta(hours=0), 0)]}
    d3 = {'measurement': 'test1', 'device_id': 'test.3', 'unit': 't',
          'values': [(datetime.now() - timedelta(hours=1), 0)]}
    client.save_data(bucket=bucket, data=[d1, d3, d2])

    # ascending sorting
    data = client.get_one_value(bucket=bucket, measurement='test1', sort='asc', last=True)
    assert data[0]['device_id'] == 'test.1'
    assert data[1]['device_id'] == 'test.3'
    assert data[2]['device_id'] == 'test.2'

    # descending sorting
    data = client.get_one_value(bucket=bucket, measurement='test1', sort='desc', last=True)
    assert data[0]['device_id'] == 'test.2'
    assert data[1]['device_id'] == 'test.3'
    assert data[2]['device_id'] == 'test.1'


def test_get_values_from_device_id(init):
    # Descending order
    data = client.get_values_from_device_id(bucket=bucket, measurement=measurement, device_id=device_id, sort='desc',
                                            time_range='all')
    assert data == list([(str(ts), val) for ts, val in test_data['values']])

    # Ascending order
    data = client.get_values_from_device_id(bucket=bucket, measurement=measurement, device_id=device_id, sort='asc',
                                            time_range='all')
    assert data == [(str(ts), val) for ts, val in reversed(test_data['values'])]

    # Test different time ranges
    values = client.get_values_from_device_id(bucket=bucket, measurement=measurement, device_id=device_id,
                                              time_range='all')
    assert len(values) == n_samples

    # Get values within 1 hour (60samples)
    values = client.get_values_from_device_id(bucket=bucket, measurement=measurement, device_id=device_id,
                                              time_range='1h')
    assert 60 >= len(values) > 58

    # Get values within 1 day (60*24)
    values = client.get_values_from_device_id(bucket=bucket, measurement=measurement, device_id=device_id,
                                              time_range='1d')
    assert 60 * 24 + 2 > len(values) > 60 * 24 - 2

    time_from = (datetime.utcnow() - timedelta(hours=10)).replace(minute=0)
    time_to = time_from + timedelta(hours=1)
    values = client.get_values_from_device_id(bucket=bucket, measurement=measurement, device_id=device_id,
                                              time_from=time_from, time_to=time_to)
    assert len(values) == 60

    time_from = (datetime.utcnow() - timedelta(hours=100)).replace(minute=0)
    time_to = time_from + timedelta(hours=5)
    values = client.get_values_from_device_id(bucket=bucket, measurement=measurement, device_id=device_id,
                                              time_from=time_from, time_to=time_to)
    assert len(values) == 60 * 5


def test_range_values(init):
    dt = datetime.utcnow()
    _measurement = 'valuerange'
    _device_id = 'valuerange.1'
    _data = {
        "measurement": _measurement,
        "device_id": _device_id,
        "values": [
            (datetime(2023, 1, 22, 12, 0, 0), 0),
            (datetime(2023, 1, 22, 13, 0, 0), 1),
            (datetime(2023, 1, 22, 14, 0, 0), 2),
            (datetime(2023, 1, 22, 15, 0, 0), 3)
        ]
    }
    client.save_data(bucket=bucket, data=_data)

    data = client.get_values_from_device_id(bucket=bucket,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all',
                                            value_type='greater',
                                            value=2)
    assert len(data) == 1
    assert data[0][1] == _data['values'][-1][1]

    data = client.get_values_from_device_id(bucket=bucket,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all',
                                            value_type='lesser',
                                            value=1)
    assert len(data) == 1
    assert data[0][1] == _data['values'][0][1]

    data = client.get_values_from_device_id(bucket=bucket,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all',
                                            value_type='range',
                                            value_within=True,
                                            value_min=1,
                                            value_max=3)
    assert len(data) == 1
    assert data[0][1] == _data['values'][2][1]

    data = client.get_values_from_device_id(bucket=bucket,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all',
                                            value_type='range',
                                            value_within=False,
                                            value_min=1,
                                            value_max=2)
    assert len(data) == 2
    assert data[0][1] == _data['values'][-1][1]
    assert data[1][1] == _data['values'][0][1]


def test_timezones(init):
    dt = datetime.utcnow()
    _measurement = 'timezone'
    _device_id = 'timezone.1'
    data = {
        "measurement": _measurement,
        "device_id": _device_id,
        "description": description,
        "values": [(dt, 1)]
    }
    client.save_data(bucket=bucket, data=data)

    cl2 = DmsInflux2(url=url, token=token, org=org)
    data = cl2.get_one_value(bucket=bucket, measurement=_measurement, device_id=_device_id, time_range='all')
    assert parse(data[0]['timestamp']) == dt

    cl2 = DmsInflux2(url=url, token=token, org=org, timezone_offset=1)
    data = cl2.get_one_value(bucket=bucket, measurement=_measurement, device_id=_device_id, time_range='all')
    assert parse(data[0]['timestamp']) == dt + timedelta(hours=1)

    cl2 = DmsInflux2(url=url, token=token, org=org, timezone_offset=-1)
    data = cl2.get_one_value(bucket=bucket, measurement=_measurement, device_id=_device_id, time_range='all')
    assert parse(data[0]['timestamp']) == dt + timedelta(hours=-1)


def test_utc_conversion(init):
    dt1 = datetime(2022, 3, 25, 12, 0, 0)
    dt2 = datetime(2022, 3, 27, 12, 0, 0)
    _measurement = 'tt'
    _device_id = 'tt.1'
    data = {
        "measurement": _measurement,
        "device_id": _device_id,
        "values": [(dt1, 1), (dt2, 2)]
    }
    client.save_data(bucket=bucket, data=data, utc_to_local=True)
    data = client.get_values_from_device_id(bucket=bucket,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all')
    assert data[0][0] == localize_dt(dt2, to_str=True)
    assert data[-1][0] == localize_dt(dt1, to_str=True)

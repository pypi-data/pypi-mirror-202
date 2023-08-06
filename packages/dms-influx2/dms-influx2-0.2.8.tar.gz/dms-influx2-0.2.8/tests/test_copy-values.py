import pytest

from dms_influx2.lib import DmsInflux2
from datetime import datetime, timedelta
from dotenv import dotenv_values
from time import sleep
from dateutil.parser import parse

config = dotenv_values()

host = config['INFLUX_HOST']
port = config['INFLUX_PORT']
token = config['DOCKER_INFLUXDB_INIT_ADMIN_TOKEN']
org = config['DOCKER_INFLUXDB_INIT_ORG']
url = f'http://{host}:{port}'

client = DmsInflux2(url=url, token=token, org=org, timezone_offset=None)

bucket = 'test_bucket_12345'
start = 0
n_samples = 5
TEST_DATA_1 = {
    "measurement": 'testcopy',
    "device_id": 'testcopy.1',
    "values": [(datetime.now().replace(microsecond=0) - timedelta(minutes=i), i)
               for i in range(start, n_samples)]
}

TEST_DATA_2 = {
    "measurement": 'testcopy2',
    "device_id": 'testcopy.2',
    "values": [(datetime.now().replace(microsecond=0) - timedelta(minutes=i), i)
               for i in range(n_samples + 1, n_samples + n_samples)]
}


def test_copy_values():
    if client.buckets_api().bucket_exists(bucket_name=bucket):
        client.buckets_api().delete_bucket_by_name(bucket_name=bucket)
    client.buckets_api().create_bucket(bucket_name=bucket)

    client.delete_api().delete_data(bucket=bucket, measurements=['testcopy', 'testcopy2'])
    client.save_data(bucket=bucket, data=TEST_DATA_1)
    client.save_data(bucket=bucket, data=TEST_DATA_2)

    client.copy_from_to(bucket_from=bucket,
                        measurement_from=TEST_DATA_2['measurement'],
                        devid_from=TEST_DATA_2['device_id'],
                        bucket_to=bucket,
                        measurement_to=TEST_DATA_1['measurement'],
                        devid_to=TEST_DATA_1['device_id'])

    data_merged = client.get_data_from_device_id(bucket=bucket,
                                                 measurement=TEST_DATA_1['measurement'],
                                                 device_id=TEST_DATA_1['device_id'])
    for i, data in  enumerate(TEST_DATA_1['values'] + TEST_DATA_2['values']):
        assert str(data[0]) == data_merged['values'][i][0]
        assert data[1] == data_merged['values'][i][1]

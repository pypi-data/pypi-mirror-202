from datetime import datetime
from dotenv import dotenv_values
import pytest
from influxdb_client.rest import ApiException

from dms_influx2.lib import DmsInflux2

config = dotenv_values()

host = config['INFLUX_HOST']
port = config['INFLUX_PORT']
token = config['DOCKER_INFLUXDB_INIT_ADMIN_TOKEN']
org = config['DOCKER_INFLUXDB_INIT_ORG']
url = f'http://{host}:{port}'
client = DmsInflux2(url=url, token=token, org=org)

bucket = 'test_bucket'

def test_ping():
    if not client.ping():
        pytest.exit('Unable to connect to influx database')


def test_bucket_exists():
    if client.buckets_api().bucket_exists(bucket):
        client.buckets_api().delete_bucket_by_name(bucket)
    client.buckets_api()._create_bucket(bucket_name=bucket)
    assert client.buckets_api().bucket_exists(bucket)


def test_delete_authorization():
    auth = client.authorizations_api().create_bucket_authorization(bucket_name=bucket, org_name=org)
    assert len(auth.id) > 5

    assert client.authorizations_api().delete_authorization(auth) is None

    with pytest.raises(ApiException):
        client.authorizations_api().find_authorization_by_id(auth_id=auth.id)




# # # TODO fix this test
# def test_create_bucket_with_token_and_delete_permissions():
#     """Test create new bucket with auth token and check for writes/reads permissions"""
#
#     new_token = client.buckets_api().create_bucket_with_auth(bucket_name=bucket).token
#
#     measurement = "test"
#
#     client2 = DmsInflux2(url=url, token=new_token, org=org)
#     data = {
#         "measurement": measurement,
#         "device_id": "test.ch",
#         "values": [(datetime.utcnow(), 0)]
#     }
#     client2.save_data(bucket=bucket, data=data)
#     client.delete_api().delete_data(bucket=bucket, measurements=[measurement])
#
#     client.buckets_api().delete_permissions(bucket_name=bucket)
#     data = {
#         "measurement": measurement,
#         "device_id": "test.ch",
#         "values": [(datetime.utcnow(), 0)]
#     }
#     with pytest.raises(Exception):
#         client2.save_data(bucket=bucket, data=data)



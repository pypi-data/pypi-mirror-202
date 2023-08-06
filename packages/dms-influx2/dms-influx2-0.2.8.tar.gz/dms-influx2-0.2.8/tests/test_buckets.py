from datetime import datetime
from dotenv import dotenv_values
import pytest

from dms_influx2.lib import DmsInflux2

config = dotenv_values()

host = config['INFLUX_HOST']
port = config['INFLUX_PORT']
token = config['DOCKER_INFLUXDB_INIT_ADMIN_TOKEN']
org = config['DOCKER_INFLUXDB_INIT_ORG']
url = f'http://{host}:{port}'
client = DmsInflux2(url=url, token=token, org=org)

bucket_test = 'test_buckets'
bucket_test_description = 'test_buckets'
bucket_test_description_readonly = 'test_buckets_readonly'
auth_bucket = 'test2'


def test_ping():
    if not client.ping():
        pytest.exit('Unable to connect to influx database')


def test_bucket_exists():
    client.authorizations_api().delete_all_bucket_authorizations()

    if client.buckets_api().bucket_exists(bucket_name=bucket_test):
        client.buckets_api().delete_bucket_by_name(bucket_name=bucket_test)

    if client.buckets_api().bucket_exists(bucket_name=auth_bucket):
        client.buckets_api().delete_bucket_by_name(bucket_name=auth_bucket)

    client.buckets_api()._create_bucket(bucket_name=bucket_test)
    assert client.buckets_api().bucket_exists(bucket_test)


def test_change_bucket_description():
    pass


def test_create_bucket_with_default_authorizations():
    client.buckets_api().delete_bucket_by_name(bucket_name=bucket_test)
    client.buckets_api().create_bucket_with_default_authorizations(bucket_test)

    auth_read_write = client.authorizations_api().find_authorizations_by_description(bucket_test)[0]
    assert auth_read_write.description == bucket_test
    assert len(auth_read_write.permissions) == 2
    assert auth_read_write.permissions[0].action == 'read'
    assert auth_read_write.permissions[0].resource.type == 'buckets'
    assert auth_read_write.permissions[1].action == 'write'
    assert auth_read_write.permissions[1].resource.type == 'buckets'

    auth_read = client.authorizations_api().find_authorizations_by_description(bucket_test_description_readonly)[0]
    assert auth_read.description == bucket_test_description_readonly
    assert len(auth_read.permissions) == 1
    assert auth_read.permissions[0].action == 'read'
    assert auth_read.permissions[0].resource.type == 'buckets'

    ### Remove this permissions and test get_or_create_bucket_authorization()
    print('auth read', auth_read)
    client.authorizations_api().delete_authorization(auth_read_write)
    client.authorizations_api().delete_authorization(auth_read)

    auth = client.authorizations_api().get_or_create_bucket_authorization(bucket_name=bucket_test, read_only=True)
    assert auth.description == bucket_test_description_readonly
    assert len(auth.permissions) == 1
    assert auth.permissions[0].action == 'read'
    assert auth.permissions[0].resource.type == 'buckets'

    auth = client.authorizations_api().get_or_create_bucket_authorization(bucket_name=bucket_test, read_only=False)
    print(auth)
    assert auth.description == bucket_test_description
    assert len(auth.permissions) == 2
    assert auth.permissions[0].action == 'read'
    assert auth.permissions[0].resource.type == 'buckets'
    assert auth.permissions[1].action == 'write'
    assert auth.permissions[1].resource.type == 'buckets'

def test_auths_dict():
    auths = client.authorizations_api().get_bucket_authorizations_dict()
    print(auths)
    assert True

def test_buckets_dict():
    pass

# # # # TODO fix this test
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


def test_delete_bucket_by_name():
    if client.buckets_api().bucket_exists(bucket_name=bucket_test):
        client.buckets_api().delete_bucket_by_name(bucket_name=bucket_test)

    if client.buckets_api().bucket_exists(bucket_name=auth_bucket):
        client.buckets_api().delete_bucket_by_name(bucket_name=auth_bucket)


    assert not client.buckets_api().bucket_exists(bucket_test)
    assert not client.buckets_api().bucket_exists(auth_bucket)

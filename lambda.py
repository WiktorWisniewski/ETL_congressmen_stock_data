import urllib3
import os
import json
import boto3
import botocore 
import botocore.session as bc
from botocore.client import Config
import csv
from datetime import datetime, timezone


def _get_key():
    dt_now = datetime.now(tz=timezone.utc)
    KEY = (
        dt_now.strftime("%m_%d_%Y")
        + "/"
    )
    return KEY


def upload_file_to_s3(bucket_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    """
    # Upload the file
    s3_client = boto3.client('s3')
    
    key = _get_key() + 'transaction_report'
    
    try:
        s3_client.upload_file('/tmp/data_file.csv', bucket_name, f'{key}.csv')
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_stock_data():
    
    http = urllib3.PoolManager()
    key = _get_key()
    
    try:
        resp = http.request("GET", f"{os.environ['API_stock']}{key}.json")
        data = json.loads(resp.data)

        # create the csv writer object
        data_file = open("/tmp/data_file.csv", "w+")
        csv_writer = csv.writer(data_file)
         
        # Counter variable used for writing 
        # headers to the CSV file
        count = 0
         
        for congressman in data:
            for transaction in congressman['transactions']:
                new_row = congressman | transaction
                new_row.pop('transactions')
                
                if count == 0:
        
                    # Writing headers of CSV file
                    header = new_row.keys()
                    csv_writer.writerow(header)
                    count += 1
         
                # Writing data of CSV file
                csv_writer.writerow(new_row.values())
         
        data_file.close()
    except urllib3.connection.ConnectionError as e:
        logging.error(e)
        return False
    return data_file




def upload_data_to_redshift():
    print('Loading function')

    # getting SecretId from Environment varibales
    secret_name=os.environ['secret_name'] 
    session = boto3.session.Session()
    region = session.region_name
    
    client = session.client(
    service_name='secretsmanager',
        region_name=region
    )
    
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    
    secret_arn=get_secret_value_response['ARN']

    secret = get_secret_value_response['SecretString']
    
    secret_json = json.loads(secret)

    print(get_secret_value_response)
    
    key = _get_key()
    
    # Initializing Botocore client
    bc_session = bc.get_session()
    
    session = boto3.Session(
            botocore_session=bc_session,
            region_name=region
        )
    
    # Initializing Redshift's client   
    config = Config(connect_timeout=5, read_timeout=5)
    client_redshift = session.client("redshift-data", config = config)
    

    query_str = f"COPY congress_data FROM 's3://{os.environ['bucket_name']}/{key}/transaction_report.csv' iam_role f{os.environ["IAM_role"]} CSV DELIMITER AS ',' DATEFORMAT 'auto' IGNOREHEADER 1 ;"
    try:
        result = client_redshift.execute_statement(WorkgroupName = os.environ['Workgroup'], Database= os.environ['database', SecretArn= secret_arn, Sql= query_str)
        print("API successfully executed")
        
    except botocore.exceptions.ConnectionError as e:
        client_redshift_1 = session.client("redshift-data", config = config)
        result = client_redshift_1.execute_statement(Database= 'dev', SecretArn= secret_arn, Sql= query_str, ClusterIdentifier= os.environ['Cluster_Identifier'])
        print("API executed after reestablishing the connection")
        return str(result)
        
    except Exception as e:
        raise Exception(e)
        
    return str(result)


def lambda_handler(event, context):
    
    get_stock_data()
    upload_file_to_s3('congressmenstockdata')
    upload_data_to_redshift()
    return {
        'statusCode': 200,
        'body': 'Success'
    }



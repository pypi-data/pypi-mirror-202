from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
import json
from botocore.errorfactory import ClientError

import time
import timeit
import logging

log = logging.getLogger(__name__)

BUCKET_SFTP='use1-netprd-infrastructure-sftp-server-users-s3'

BUCKET_TOOLS='use1-tools-infrastructure-datalake-s3'

def get_secrets(secret_url, region):
    secret_name = secret_url
    region_name = region
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def get_file_s3 (bucket, path):
    """
        Get file in bucket s3
        :param bucket: bucket s3 , path: path inside the bucket
        :return file
    """
    s3_obj =boto3.client('s3')
    s3_clientobj = s3_obj.get_object(Bucket=bucket, Key=path)
    s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
    return s3_clientdata

def put_file_s3 (bucket, path,file):
    """
        Insert file in bucket s3
        :param bucket: bucket s3 , path: path inside the bucket , file: file to insert
    """
    client = boto3.client('s3')
    client.put_object(Body=file, Bucket=bucket,Key=path,ACL='bucket-owner-full-control')

def convert_to_windows_format(bucket,path_origin ,path_destination):
    """
            Convert and put file in windows format
            :param bucket: bucket s3 , path_origin: path origin inside the bucket , path_destination: path destination
        """
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    s3_obj = boto3.client('s3')
    s3_clientobj = s3_obj.get_object(Bucket=bucket, Key=path_origin)
    s3_clientdata = s3_clientobj['Body'].read()
    file_replaced = s3_clientdata.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)
    put_file_s3(bucket,path_destination,file_replaced)

def delete_file_s3 (bucket, path):
    """
        Delete file from bucket s3
        :param bucket: bucket s3 , path: file path
    """
    s3_obj = boto3.client('s3')
    s3_obj.delete_object(Bucket=bucket, Key=path)

def get_data_athena(spark,json_secret,query):
    """
        Get spark dataframe with data from Athena (tables and views)
        :param spark: spark session, json_secret: Athena credential, query: query to execute
    """
    SECRET_ATHENA = get_secrets(
        "arn:aws:secretsmanager:us-east-1:644197204120:secret:data_athena_iamuser-rwmgvN",
        "us-east-1")
    ##Setting driver jdbc Athena
    jdbc_driver = "com.simba.athena.jdbc42.Driver"
    ##Generate URL to connect athena by JDBC SIMBA
    jdbcUrl = "jdbc:awsathena://AWSRegion=us-east-1;UID={};PWD={};workgroup=dba_admin;schema=pomelo,".format(json_secret.get('access-id'), json_secret.get('access-secret'))
    df = spark.read.format("jdbc") \
        .option("query", query) \
        .option("url", jdbcUrl) \
        .option("driver", jdbc_driver) \
        .load()
    return df

def get_data_replica_pg(spark,query,db):
    JDBC_DRIVER = "org.postgresql.Driver"
    secret_json = get_secrets(
        "arn:aws:secretsmanager:us-east-1:644197204120:secret:kubernetes/infrastructure/dms-replica-db-credentials-7yymMb",
        "us-east-1")

    jdbcUrl = "jdbc:postgresql://{}:{}/{}?user={}&password={}".format(secret_json.get("host"),
                                                                      secret_json.get("port"),
                                                                      db,
                                                                      secret_json.get("username"),
                                                                      secret_json.get("password"))
    df = spark.read.format("jdbc") \
        .option("url", jdbcUrl) \
        .option("query", query) \
        .option("driver", JDBC_DRIVER) \
        .load()

    return df

def insert_dataframe_into_sql_server(df, table, schema,json_secret,_database,mode):
    username = json_secret.get('username')
    password = json_secret.get('password')
    host = json_secret.get('host')
    port = json_secret.get('port')
    database = _database
    destination_table = table
    jdbcUrl = f"jdbc:sqlserver://{host}:1433;databaseName={database}"
    jdbcDriver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"

    df.write.format("jdbc") \
        .mode(mode) \
        .option("user", username) \
        .option("password", password) \
        .option("url", jdbcUrl) \
        .option("driver", jdbcDriver) \
        .option("dbtable", destination_table) \
        .option("createTableColumnTypes", schema) \
        .save()

def move_file_s3(bucket,origin,destination,coding):
    s3_obj = boto3.client('s3')
    try:
        s3_obj.head_object(Bucket=bucket, Key=origin)
        s3_clientobj = s3_obj.get_object(Bucket=bucket, Key=origin)
        s3_clientdata = s3_clientobj['Body'].read().decode(coding)
        s3_obj.put_object(Body=s3_clientdata, Bucket=bucket,
                      Key=destination)
        #s3_obj.delete_object(Bucket=bucket, Key=origin)
    except ClientError:
        print("Archivo {} no encontrado".format(origin))
        pass

def delete_s3_folder(bucket,key_path):
    """
            Delete folder from bucket s3
            :param bucket: bucket s3 , key_path: folder path 'bi/outbound/temp/local-1663088553000/'
        """
    s3 = boto3.resource('s3')
    bucket_name = bucket
    folder = key_path
    bucket = s3.Bucket(bucket_name)
    deletedObj = bucket.objects.filter(Prefix=folder).delete()

def send_file_to_bucket_intern(dataframe,application_id,name_file,path_destination,sep):
    """
             Send file to SFTP for internal users
                :param dataframe: bucket s3 , application_id: application of spark to make path ('bi/outbound/temp/local-1663088553000/') , name_file: name of file ,path_destination: path destionation of file,
                sep: separator of files. If we dont want a separator we pass the param 'None'
    """

    if not dataframe is None and len(dataframe) > 0:
        dataframe.to_csv(
            's3://{BUCKET_TOOLS}/bi/outbound/temp/{application_id}/{name_file}'.
            format(BUCKET_TOOLS=BUCKET_TOOLS, application_id=application_id, name_file=name_file), sep='{}'.format(sep if sep in [',',';','|'] else ';'), index=False, header=False)
        file = get_file_s3(BUCKET_TOOLS,
                                      'bi/outbound/temp/{application_id}/{name_file}'.
                                      format(application_id=application_id, name_file=name_file))
        if sep in [',',';','|']:
            file_replaced = file
        else:
            file_replaced = file.replace(';', '')

        # Disponibilizacion en SFTP

        put_file_s3(BUCKET_SFTP,
                               'bi/outbound/{path_destination}/{name_file}'.
                               format(path_destination=path_destination, name_file=name_file),
                               file_replaced)
        convert_to_windows_format(BUCKET_SFTP,
                                             'bi/outbound/{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file),
                                             'bi/outbound/{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file))

        # Eliminamos los archivos en temp
        delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

        print("FILE GENERADO CORRECTAMENTE")
    else:
        print("No se genero archivo por falta de informacion")

def send_file_to_bucket_raas(dataframe,application_id,client_id,name_file,path_destination):
    if not dataframe is None and len(dataframe) > 0:
        dataframe.to_csv(
            's3://{BUCKET_TOOLS}/bi/outbound/temp/{application_id}/{name_file}.txt'.
            format(BUCKET_TOOLS=BUCKET_TOOLS, application_id=application_id, name=name_file), sep=';', index=False, header=False)
        file = get_file_s3(BUCKET_TOOLS,
                                      'bi/outbound/temp/{application_id}/{name_file}.txt'.
                                      format(application_id=application_id, name=name_file))
        file_replaced = file.replace(';', '')

        # Disponibilizacion en SFTP

        put_file_s3(BUCKET_SFTP,
                               'bi/outbound/{path_destination}/{name_file}.txt'.
                               format(path_destination=path_destination, name_file=name_file),
                               file_replaced)
        convert_to_windows_format(BUCKET_SFTP,
                                             'bi/outbound/{path_destination}/{name_file}.txt'.
                                             format(path_destination=path_destination, name_file=name_file),
                                             'bi/outbound/{path_destination}/{name_file}.txt'.
                                             format(path_destination=path_destination, name_file=name_file))

        # Eliminamos los archivos en temp
        delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

        print("FILE GENERADO CORRECTAMENTE")
    else:
        print("No se genero archivo por falta de informacion")
        pass

def send_file_to_specific_bucket(specific_bucket,dataframe,application_id,name_file,path_destination,sep,header_value):
    """
             Send file to any bucket for internal users
                :param dataframe: bucket s3 , application_id: application of spark to make path ('bi/outbound/temp/local-1663088553000/') , name_file: name of file ,path_destination: path destionation of file,
                sep: separator of files. If we dont want a separator we pass the param 'None'
    """

    if not dataframe is None and len(dataframe) > 0:
        dataframe.to_csv(
            's3://{BUCKET_TOOLS}/bi/outbound/temp/{application_id}/{name_file}'.
            format(BUCKET_TOOLS=BUCKET_TOOLS, application_id=application_id, name_file=name_file), sep='{}'.format(sep if sep in [',',';','|'] else ';'), index=False, header=header_value)
        file = get_file_s3(BUCKET_TOOLS,
                                      'bi/outbound/temp/{application_id}/{name_file}'.
                                      format(application_id=application_id, name_file=name_file))
        if sep in [',',';','|']:
            file_replaced = file
        else:
            file_replaced = file.replace(';', '')

        # Disponibilizacion en specific bucket

        put_file_s3(specific_bucket,
                               '{path_destination}/{name_file}'.
                               format(path_destination=path_destination, name_file=name_file),
                               file_replaced)
        convert_to_windows_format(specific_bucket,
                                             '{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file),
                                             '{path_destination}/{name_file}'.
                                             format(path_destination=path_destination, name_file=name_file))

        # Eliminamos los archivos en temp
        delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

        print("FILE GENERADO CORRECTAMENTE")
    else:
        print("No se genero archivo por falta de informacion")

def start_a_crawler(crawler_name):
   session = boto3.session.Session()
   glue_client = session.client('glue')
   response = glue_client.start_crawler(Name=crawler_name)
   return response

def run_crawler(crawler: str, *, timeout_minutes: int = 120, retry_seconds: int = 5) -> None:
    """Run the specified AWS Glue crawler, waiting until completion."""
    # Ref: https://stackoverflow.com/a/66072347/
    timeout_seconds = timeout_minutes * 60
    client = boto3.client("glue")
    start_time = timeit.default_timer()
    abort_time = start_time + timeout_seconds

    def wait_until_ready() -> None:
        state_previous = None
        while True:
            response_get = client.get_crawler(Name=crawler)
            state = response_get["Crawler"]["State"]
            if state != state_previous:
                log.info(f"Crawler {crawler} is {state.lower()}.")
                state_previous = state
            if state == "READY":  # Other known states: RUNNING, STOPPING
                return
            if timeit.default_timer() > abort_time:
                raise TimeoutError(f"Failed to crawl {crawler}. The allocated time of {timeout_minutes:,} minutes has elapsed.")
            time.sleep(retry_seconds)

    wait_until_ready()
    response_start = client.start_crawler(Name=crawler)
    assert response_start["ResponseMetadata"]["HTTPStatusCode"] == 200
    log.info(f"Crawling {crawler}.")
    wait_until_ready()
    log.info(f"Crawled {crawler}.")


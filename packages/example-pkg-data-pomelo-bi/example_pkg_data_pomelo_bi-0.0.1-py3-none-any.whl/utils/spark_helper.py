import boto3
from pyspark.sql import SparkSession
from utilities import aws_helper
from pyspark.context import SparkContext

BUCKET_TOOLS = 'use1-tools-infrastructure-datalake-s3'

def get_context(app_name):
    print("Setting Spark Session")
    spark = SparkSession \
        .builder \
        .appName(app_name) \
        .getOrCreate()
    spark.sparkContext._jsc.hadoopConfiguration().set('fs.s3.canned.acl', 'BucketOwnerFullControl')
    return spark

def to_csv(df, application_id, file_name, bucket_destination, path_destination,file_extension,sep,header_value):
    """
        Export Pyspark Dataframe to file with file_name in bucket s3
        :param
            df: dataframe,
            application_id:
            application_id,
            file_name: file_name,
            bucket_destination: bucket s3 ,
            path_destination: path destination will be end '/'
        :return file
    """
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    temp_bucket = BUCKET_TOOLS
    print(f'temp_bucket: {temp_bucket}')
    temp_prefix = f'bi/outbound/temp/{application_id}/'
    print(f'temp_prefix: {temp_prefix}')
    prefix_target = f'{path_destination}{file_name}.{file_extension}'
    print(f'prefix_target: {prefix_target}')
    df.write.options(header=header_value,delimiter='{}'.format(sep if sep in [',',';','|'] else ';'),escape='\"').mode('overwrite').csv(f's3://{temp_bucket}/{temp_prefix}')

    object_s3 = s3_client.list_objects(Bucket=BUCKET_TOOLS,Prefix=temp_prefix,Delimiter='/')
    print(object_s3)
    temp_name_file = ''
    for object in object_s3.get('Contents'):
        if object.get('Key').endswith('.csv'):
            # object onboarding/part-00000-f676d0be-e9b7-4e98-a8a0-7022ccae86d5-c000.csv
            # temp_name_file=part-00000-f676d0be-e9b7-4e98-a8a0-7022ccae86d5-c000.csv
            temp_name_file = object.get('Key').split('/')[-1]
            print(f'Se detectó un file temporal en s3://{temp_bucket}/{temp_prefix}{temp_name_file}')

            s3_resource.Object(bucket_destination,prefix_target).copy_from(
                CopySource=f'{temp_bucket}/{temp_prefix}{temp_name_file}')

            aws_helper.delete_s3_folder(BUCKET_TOOLS, 'bi/outbound/temp/{application_id}/'.format(application_id=application_id))

    if (temp_name_file == ''):
        print(f"No se encontró un archivo con la exntesión {file_extension} en el path s3://{temp_bucket}/{temp_prefix}{temp_name_file}")
import boto3

def create_bucket(bucket_name):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)

def copy_file(source_bucket, source_key, target_bucket, target_key):
    s3 = boto3.resource('s3')
    s3.meta.client.copy_object(Bucket=target_bucket, Key=target_key, CopySource={'Bucket': source_bucket, 'Key': source_key})

def lambda_handler(event, context):
    source_bucket = 'source-bucket'
    source_key = 'src/design.png'
    target_bucket = 'destination-bucket'
    target_key = 'dest/dest.png'

    s3 = boto3.client('s3')
    
    # Verificar si el bucket de origen existe
    try:
        s3.head_bucket(Bucket=source_bucket)
    except:
        # Si no existe, crear el bucket e insertar imagen por defecto
        create_bucket(source_bucket)
    
    # Verificar si el bucket de destino existe
    try:
        s3.head_bucket(Bucket=target_bucket)
    except:
        # Si no existe, crear el bucket
        create_bucket(target_bucket)
    
    # Copiar el archivo de un bucket a otro
    copy_file(source_bucket, source_key, target_bucket, target_key)

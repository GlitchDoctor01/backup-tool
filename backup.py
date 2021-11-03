import configparser
from loguru import logger
import sys
import time
import botocore
import boto3
import os
import argparse

if not os.path.exists("logs"):
	os.mkdir("logs")

if not os.path.exists("tmp"):
	os.mkdir("tmp")


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--period", required=True, help="Cloud directory name (hourly, daily, etc.)")
ap.add_argument("-n", "--dbname", required=True, help="Name of the database")
args = vars(ap.parse_args())

logger.add("logs/info.log", level="INFO")
config = configparser.ConfigParser()
config.read('config.ini')
current_time = time.strftime('%Y%m%d-%H%M%S')
backup_name = str.format("{}--{}", args["dbname"], current_time)

backup_period = args["period"]

AWS_ACCESS_KEY_ID = config["s3"]["id"]
AWS_SECRET_ACCESS_KEY =  config["s3"]["secret_key"]
AWS_ENDPOINT = config["s3"]["endpoint"]

s3_client = boto3.client(
    service_name='s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url=AWS_ENDPOINT
)

os.system(
    str.format("mysqldump --no-tablespaces -h {host} -P {port} -u {user} -p{passwd} {db_name} | gzip > tmp/{backup_name}.sql.gz",
    host=config["mysql"]["host"],
    port=config["mysql"]["port"],
    user=config["mysql"]["user"],
    passwd=config["mysql"]["passwd"],
    db_name=args["dbname"],
    backup_name=backup_name))


try:
	s3_client.create_bucket(Bucket=config["s3"]["bucket_name"])
except botocore.exceptions.ClientError:
	#logger.info(str.format("Bucket {} Already Exists", config["s3"]["bucket_name"]))

with open(str.format("tmp/{}.sql.gz", backup_name), "rb") as f:
    s3_client.upload_fileobj(f, config["s3"]["bucket_name"], str.format("{}/{}.sql.gz",backup_period, backup_name))

os.remove(str.format("tmp/{}.sql.gz", backup_name))
#logger.info("Backup created")




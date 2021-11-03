# Usage 

1. Create config file by following example

```ini config.ini
config.ini

[s3]
id = AWS_ID
secret_key = AWS_SECRET
endpoint = http://example.tld
host_bucket = %(bucket)s.example.tld
bucket_name = example-database

[mysql]
user = mysql_user
passwd = secret
host = 127.0.0.1
port = 3306

```

2. Create venv from requirements.txt

```bash 
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

3. Add cronjob

```@daily cd /path/to/script-directory && venv/bin/python backup.py  -p <dir-name> -n <database-name>```

## command-line args

``` -p - name of a directory that will be created inside bucket. e.g. daily```

```-n - database name```

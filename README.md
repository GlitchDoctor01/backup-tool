# Usage 
1. Define your s3 and mysql config in config.ini
2. Create virtual environment and install requirements
3. Add a cronjob ```@daily cd /path/to/script-folder && venv/bin/python backup.py  -p <folder-name> -n <database-name>```

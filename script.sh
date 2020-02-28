#!/bin/bash
source /Users/peiwen_li/.bash_profile #or .bashrc
cd /Users/peiwen_li/Documents/GitHub/VA-boutique
venv/bin/python manage.py send_mail >>  /Users/peiwen_li/cron_mail.log 2>&1

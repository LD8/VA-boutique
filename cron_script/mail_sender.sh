#!/bin/bash
source /home/don/.bashrc
source /home/don/VA-boutique/venv/bin/activate
python /home/don/VA-boutique/manage.py send_mail >> /home/don/logs/cron_mail.log 2>&1
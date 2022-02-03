import json
from datetime import datetime


def log(log):
    now = datetime.now()
    timern = now.strftime("%d/%m/%Y %H:%M:%S")

    with open('./other/log.txt', 'a') as f:
        f.write('\n')
        f.write(f"{timern} | {log}")
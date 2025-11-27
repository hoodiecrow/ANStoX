
import re

def makedb ():
    with open('./src/dict.txt', 'r') as f:
        dbtext = f.read()
    db = {}
    for line in dbtext.splitlines():
        if line != '':
            (key, val) = re.split(r'\s+->\s+', line)
            db[key] = val
    return db

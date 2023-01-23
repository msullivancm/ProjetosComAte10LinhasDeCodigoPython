import pymysql
import pandas as pd

def con_banco():
    db = pymysql.connect(
        host='ferroport.managed-otrs.com',
        user='ferroport_ro',
        passwd='senha',
        db='otrs',
        ssl_ca='C:/OTRS/ferroport-ca-cert.pem',
        ssl_key='C:/OTRS/ferroport-client-key.pem',
        ssl_cert='C:/OTRS/ferroport-client-cert.pem'
    )
    cursor = db.cursor()
    query = '''SELECT TABLE_NAME FROM information_schema.tables'''
    cursor.execute(query)

    return cursor


dbcursor = con_banco()

print(dbcursor.content())

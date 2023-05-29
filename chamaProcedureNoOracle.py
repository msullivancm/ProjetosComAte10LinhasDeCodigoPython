import cx_Oracle

# Estabelecendo conexão com o banco de dados
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCLCDB')
conn = cx_Oracle.connect(user='seu_usuario', password='sua_senha', dsn=dsn_tns)

# Criando um cursor para executar a consulta
cur = conn.cursor()

# Chamando a stored procedure
p_id = 1
p_nome = 'João'
cur.callproc('sua_stored_procedure', [p_id, p_nome])

# Comitando as mudanças no banco de dados
conn.commit()

# Fechando o cursor e a conexão
cur.close()
conn.close()

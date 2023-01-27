import keyring
import subprocess

senhaBanco = keyring.get_password("acessoBanco", "bkp")
host = f'S02SQL01\\MSSQLSERVER3'
hostDestino = f'S02SQLHM02\S02SQLHM02'
hostDestinoRede = f'\\\\10.27.0.14'
banco = 'DADOSFRP'
caminhoBackup = f'V:\\tmp\\{banco}.BAK'
servidorBackup = f'\\\\S02SQLHM02\\Backup'
nomeBackup = 'DADOSFRP-Full with Compression'
senhaTotvs = keyring.get_password('acessoTotvs', 'totvs')
senhaTotvsWindows = keyring.get_password('acessoTotvsWindows','master\\totvs')
bancoDestino = 'DADOS_FRP12_P12133_TESTE'
caminhoBackupDestino = f'D:\\Program Files\\Microsoft SQL Server\\MSSQL15.S02SQLHM02\\MSSQL\\Backup\\{banco}.BAK'
volumeDestino = f'DADOSLLXMR_Data'
bancoDestinoData = f'E:\\Program Files\\Microsoft SQL Server\\MSSQL11.MSSQLSERVER\\MSSQL\\DATA\\{bancoDestino}.mdf'
volumeDestinoLog = f'DADOSLLXMR_log'
bancoDestinoLog = f'E:\\Program Files\\Microsoft SQL Server\\MSSQL11.MSSQLSERVER\\MSSQL\\DATA\\{bancoDestino}_log.ldf'

servicos = [".P12_FRP_P12133_TESTE_REST",".P12_FRP_P12133_TESTE_SLAVE_01",".P12_FRP_P12133_TESTE_SLAVE_02",".P12_FRP_P12133_TESTE_SLAVE_03",".P12_FRP_P12133_TESTE_SLAVE_04",".P12_FRP_P12133_TESTE_WF",".P12_FRP_P12133_TESTE_WS",".P12_FRP_P33_TESTE_LOAD_BROKER",".P12_FRP_P33_TESTE_LOAD_BROKER_WEB"]

comandoSqlcmd = f'sqlcmd -U bkp -P {senhaBanco} -S {host} -d {banco} -Q '
comandoSqlcmdMaster = f'sqlcmd -U bkp -P {senhaBanco} -S {hostDestino} -d master -Q '
comandoSqlcmdDestino = f'sqlcmd -U bkp -P {senhaBanco} -S {hostDestino} -d {bancoDestino} -Q '

criaBackup = f'"BACKUP DATABASE [{banco}] \
to disk = N\'{caminhoBackup}\' WITH NOFORMAT, INIT, NAME = N\'{nomeBackup}\', SKIP, \
NOREWIND, NOUNLOAD, COMPRESSION, STATS = 10, COPY_ONLY, MAXTRANSFERSIZE = 131072"'
print(comandoSqlcmd + criaBackup)

criaMapeamentoB = f'net use B: {servidorBackup} {senhaTotvs} /user:totvs /Persistent:No'
print(criaMapeamentoB)

moveBackupParaB = f'move {caminhoBackup} B:\\'
print(moveBackupParaB)

removeMapeamentoB = f'net use B: /delete /Y'
print(removeMapeamentoB)

for s in servicos:
    print(f'runas /savecred /user:master\\totvs \"sc {hostDestinoRede} stop {s}\"')
print("Derruba usuários logados")

colocaBancoOffline = f'"ALTER DATABASE [{bancoDestino}] SET OFFLINE WITH ROLLBACK IMMEDIATE" -t 90 -s ; -W -e'
print(comandoSqlcmdMaster + colocaBancoOffline)

print("Restaura backup")
restoreDatabaseDestino = f'"RESTORE DATABASE [{bancoDestino}] FILE = N\'{volumeDestino}\' FROM DISK = N\'{caminhoBackupDestino}\' WITH  FILE = 1, MOVE N\'{volumeDestino}\' TO N\'{bancoDestinoData}\', MOVE N\'{volumeDestinoLog}\' TO N\'{bancoDestinoLog}\', NOUNLOAD,  REPLACE,  STATS = 10"'
print(comandoSqlcmdMaster + restoreDatabaseDestino)

print("Muda o owner do banco para totvs")
mudaOwner = f'"USE [{bancoDestino}] exec sp_changedbowner totvs" -t 90 -s ; -W -e '
print(comandoSqlcmdMaster + mudaOwner)

print("Cria usuário de desenvolvimento somente leitura")
criaUsuarioDesenvolvimento = f'"USE [{bancoDestino}] CREATE USER [desenv] FOR LOGIN [desenv] ALTER ROLE [db_datareader] ADD MEMBER [desenv]" -t 90 -s ; -W -e'
print(comandoSqlcmdMaster + criaUsuarioDesenvolvimento)

print("Altera status do banco para recovery")
alteraBancoParaRecovery = f'"ALTER DATABASE [{bancoDestino}] SET RECOVERY SIMPLE WITH NO_WAIT" -t 90 -s ; -W -e'
print(comandoSqlcmdMaster + alteraBancoParaRecovery)

print("Executa shrink do log")
executaShrinkDoLog = f'"USE [{bancoDestino}] DBCC SHRINKFILE (N\'{volumeDestinoLog}\' , 0, TRUNCATEONLY)" -t 90 -s ; -W -e'
print(comandoSqlcmdMaster + executaShrinkDoLog)

print("Executa script para bancos de homologação")
print(comandoSqlcmdDestino + "TRUNCATE TABLE SCHDTSK;")
print(comandoSqlcmdDestino + "TRUNCATE TABLE SXH;")
print(comandoSqlcmdDestino + "DELETE FROM XX0 WHERE 1=1 AND R_E_C_N_O_ = '4' OR R_E_C_N_O_ = '5' OR R_E_C_N_O_ = '6' OR R_E_C_N_O_ = '7' OR R_E_C_N_O_ = '8'")
print(comandoSqlcmdDestino + "UPDATE  XX0 SET XX0_IP =  '10.27.0.14', XX0_PORTA = '50061'")
print(comandoSqlcmdDestino + "DELETE FROM XX1 WHERE XX1_CODIGO IN ('000024','000025','000026','000027','000028','000029', '000030', '000031', '000032', '000033', '000034', '000035') OR D_E_L_E_T_ = '*'")
print(comandoSqlcmdDestino + "UPDATE  SYS_USR SET USR_EMAIL = ' ' WHERE USR_MSBLQL IN  ('1','2')")

for s in servicos:
    print(f'runas /savecred /user:master\\totvs \"sc {hostDestinoRede} start {s}\"')

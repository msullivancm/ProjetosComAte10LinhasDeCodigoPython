from sqlalchemy import create_engine
import pandas as pd

db_connection_str = 'mysql+pymysql://frpro:Ferroport#2022@10.27.0.253/otrs'
db_connection = create_engine(db_connection_str)

'''db_connection_str = 'mysql+pymysql://ferroport_ro:senha@ferroport.managed-otrs.com/otrs'
db_ssl_args = {'ssl_ca': 'C:/OTRS/ferroport-ca-cert.pem',
               'ssl_key': 'C:/OTRS/ferroport-client-key.pem',
               'ssl_cert': 'C:/OTRS/ferroport-client-cert.pem'}
db_connection = create_engine(db_connection_str, connect_args=db_ssl_args)'''

query = '''SELECT
	t.TN AS 'Numero do Ticket',
	ts.name Status,
	t.TITLE AS Titulo,
	q.name AS Fila,
	t.CREATE_TIME AS Dt_Criacao_Ticket,
	t.customer_id AS username,
	CONCAT(u.first_name, ' ', u.last_name) AS Analista,
	case
			(
		select
				max(sv2.vote_value)
		from
				survey_vote sv2
		inner join survey_request sr2 on
				sv2.request_id = sr2.id
		inner join ticket t2 on
				sr2.ticket_id = t2.id
		where
				sv2.question_id = 1
			and t2.id = t.id)
		when 'Yes' then 'SIM'
		when 'No' then 'NAO'
		else 'NÃO APURADO'
	end as Resolvido,
	case
			(
		select
				max(sv2.vote_value)
		from
				survey_vote sv2
		inner join survey_request sr2 on
				sv2.request_id = sr2.id
		inner join ticket t2 on
				sr2.ticket_id = t2.id
		where
				sv2.question_id = 2
			and t2.id = t.id)
		when 1 then '1 - Muito Insatisfeito'
		when 2 then '2 - Insatisfeito'
		when 3 then '3 - Regular'
		when 4 then '4 - Satisfeito'
		when 5 then '5 - Muito Satisfeito'
		else 'Não respondido'
	end as Satisfacao,
	SEC_TO_TIME(sla.solution_time * 60) as SLA,
	(		select
			SEC_TO_TIME( 
						sum(
							TIME_TO_SEC(
										(select th02.change_time 
										from ticket_history th02 
										where th02.change_time > ticket_history.change_time 
										LIMIT 1 )
										)
							)
						)
		from
			ticket
		left join ticket_history on
			ticket.id = ticket_history.ticket_id
		left join ticket_state on
			ticket_history.state_id = ticket_state.id
		where 
			ticket.id = t.id
			and ticket_history.state_id = 13
	) as Tempo_Decorrido,
		(
	select
			case
				when max(SUBSTRING(sv2.vote_value, 12)) <> '' then max(SUBSTRING(sv2.vote_value, 12))
			else 'NÃO APURADO'
		end
	from
			survey_vote sv2
	inner join survey_request sr2 on
			sv2.request_id = sr2.id
	inner join ticket t2 on
			sr2.ticket_id = t2.id
	where
			sv2.question_id = 3
		and t2.id = t.id) as Comentario,
	datediff(now(),t.create_time) Aging 
FROM
		ticket t
Left join users u ON
		t.user_id = u.id
Left join queue q ON 
		q.id = t.queue_id
left join survey_request sr ON
		sr.ticket_id = t.id
left join sla on
		sla.id = t.sla_id
left join ticket_history th on
		th.id = t.id
left join ticket_state ts on 
	ts.id = t.ticket_state_id 
where t.create_time >= CONCAT( year(now()), '-01-01' )'''

df = pd.read_sql(query, con=db_connection)

print(df)

#Gera tabela em excel com conteudo da query
df.to_excel('otrschamados.xlsx', index=False, header=df.columns)
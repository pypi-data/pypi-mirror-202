import pingdatautil

logger = pingdatautil.Logger()
hyper = pingdatautil.HyperClass(logger=logger)
ox = pingdatautil.ODBCExport(logger=logger)

cs = (
    F"DRIVER=ODBC Driver 17 for SQL Server;"
    F"SERVER=localhost;PORT=1433;"
    F"DATABASE=TEST;UID=sa;PWD=P@ssw0rd;"
)


ox.connect(cs)
ox.with_data_date_column = "data_date"
sql_command = 'SELECT * FROM bnk48_member'
data_file = "D:\\TEMP\\bnk.txt"
ox.export_query_to_text(sql_command, data_file, separator=",")

hyper.odbc_connect(cs)
hyper_file = "D:\\TEMP\\bnk.hyper"
hyper.start()
hyper.create_file(hyper_file)
hyper.create_schema('Extract')
sql_command = 'SELECT *,cast(NULL as datetime2(0)) as data_date FROM bnk48_member WHERE 0=1'
hyper.create_table_from_sql_command('bnk48_member', sql_command)
hyper.execute_command(
    f'''COPY "Extract"."bnk48_member" FROM '{data_file}' WITH (format csv, NULL '', delimiter ',', header)''')
hyper.detach_file()
hyper.stop()

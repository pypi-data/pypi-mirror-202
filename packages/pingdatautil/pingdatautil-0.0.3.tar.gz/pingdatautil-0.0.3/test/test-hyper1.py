import pingdatautil

logger = pingdatautil.Logger()
hyper = pingdatautil.HyperClass(logger=logger)

cs = (
    F"DRIVER=ODBC Driver 17 for SQL Server;"
    F"SERVER=localhost;PORT=1433;"
    F"DATABASE=TEST;UID=sa;PWD=P@ssw0rd;"
)

hyper.odbc_connect(cs)
hyper_file = "D:\\TEMP\\demo_reader.hyper"
table_name = "DEMO_READER"
hyper.query_to_hyper(hyper_file, table_name, "SELECT * FROM DEMO_READER")

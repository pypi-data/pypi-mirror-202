import pingdatautil

logger = pingdatautil.Logger()

cs = (
    F"DRIVER=ODBC Driver 17 for SQL Server;"
    F"SERVER=localhost;PORT=1433;"
    F"DATABASE=TEST;UID=sa;PWD=P@ssw0rd;"
)

ex = pingdatautil.ODBCExport(logger=logger)
ex.connect(cs)

ex.export_query_to_text("SELECT * FROM DEMO_READER", "D:\\TEMP\\DEMO_READER.txt", separator=",")

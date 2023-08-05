import pingdatautil

logger = pingdatautil.Logger()
linenotify = pingdatautil.LineNotify(token="A", logger=logger)
en = pingdatautil.EngineHelper(logger=logger)
oh = pingdatautil.ODBCHelper(logger=logger)
cs = (
    F"DRIVER=ODBC Driver 17 for SQL Server;"
    F"SERVER=localhost;PORT=1433;"
    F"DATABASE=TEST;UID=sa;PWD=P@ssw0rd;"
)
# oh.connect(cs)
# oh.execute_full("SELECT TOP 10 * FROM bnk48_member", with_result=True)
# oh.close()
# gd = pingdatautil.GoogleDrive()
# gs = pingdatautil.GoogleSheet()

ex = pingdatautil.ODBCExport(logger=logger)
ex.show_table_command = None
ex.with_data_date_column = "data_date"
ex.connect(cs)

ex.export_query_to_text("SELECT TOP 10 * FROM DEMO_READER", "D:\\TEMP\\bnk.txt", separator="\t")

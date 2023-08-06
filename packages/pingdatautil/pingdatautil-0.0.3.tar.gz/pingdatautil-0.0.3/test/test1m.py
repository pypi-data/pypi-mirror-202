from pingdatautil import DataExport, Logger

logger = Logger()

cs = (
    F"DRIVER=ODBC Driver 17 for SQL Server;"
    F"SERVER=192.168.50.112;PORT=1433;"
    F"DATABASE=TEST;UID=sa;PWD=P@ssw0rd;"
)

ex = DataExport(logger=logger)
ex.show_table_command = None
ex.with_data_date_column = "data_date"
ex.connect(cs)

ex.export_query_to_text("SELECT * FROM BNK48_MEMBER", "/Users/godhand/bnk.txt", separator="\t")

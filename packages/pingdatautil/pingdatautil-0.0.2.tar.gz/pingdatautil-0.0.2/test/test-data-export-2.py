import os
import pingdatautil

logger = pingdatautil.Logger()

######### ODBC #########
de1 = pingdatautil.DataExport(logger=logger)

cs = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER=localhost;PORT=1433;DATABASE=TEST;UID=sa;PWD=P@ssw0rd;"

de1.connect(cs, mode="odbc")
de1.with_row_id_column = "row_id"
de1.with_data_date_column = "data_date"
sql_command_1 = "SELECT * FROM bnk48_member"

file_name_1a = "D:\\TEMP\\BNK_ODBC.html"
de1.export_query_to_html(sql_command_1, file_name_1a)

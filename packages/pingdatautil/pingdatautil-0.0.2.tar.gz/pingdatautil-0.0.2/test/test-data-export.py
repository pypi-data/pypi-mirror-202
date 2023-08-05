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
file_name_1 = "D:\\TEMP\\BNK_ODBC.txt"
de1.export_query_to_text(sql_command_1, file_name_1, separator="|")

######### JDBC #########

os.environ["JAVA_HOME"] = "C:\\Dev\\openlogic-openjdk-jre-11.0.18+10-windows-x64"

de2 = pingdatautil.DataExport(logger=logger)

cs2 = {
    "driver": "C:\\Dev\\JDBC\\mssql-jdbc-10.2.1.jre8.jar",
    "class": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
    "jdbc": "jdbc:sqlserver://localhost:1433;databaseName=TEST;encrypt=false;trustServerCertificate=true",
    "user": "sa",
    "pass": "P@ssw0rd"
}

de2.connect(cs2, mode="jdbc")
de2.dialect = "PG"
de2.with_row_id_column = "row_id"
de2.with_data_date_column = "data_date"
sql_command_2 = "SELECT * FROM bnk48_member"
file_name_2 = "D:\\TEMP\\BNK_JDBC.txt"
de2.export_query_to_text(sql_command_2, file_name_2, separator="\t")

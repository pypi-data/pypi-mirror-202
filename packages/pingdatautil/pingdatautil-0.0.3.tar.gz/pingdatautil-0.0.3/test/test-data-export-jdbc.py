import os
import pingdatautil
os.environ["JAVA_HOME"] = "C:\\Dev\\openlogic-openjdk-jre-11.0.18+10-windows-x64"

de = pingdatautil.DataExport()

cs = {
    "driver": "C:\\Dev\\JDBC\\mssql-jdbc-10.2.1.jre8.jar",
    "class": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
    "jdbc": "jdbc:sqlserver://localhost:1433;databaseName=DEMO_DATA;encrypt=false;trustServerCertificate=true",
    "user": "sa",
    "pass": "P@ssw0rd"
}

de.connect(cs, mode="jdbc")
sql_command_2 = "SELECT TOP 1000 * FROM DEMO_SALES_1M"
file_name_2 = "D:\\TEMP\\DEMO_SALES_1M.txt"
de.export_query_to_text(sql_command_2, file_name_2, separator="|", compress="gzip")



import pingdatautil
import os

os.environ["JAVA_HOME"] = "C:\\Dev\\openlogic-openjdk-jre-11.0.18+10-windows-x64"

logger = pingdatautil.Logger()
jd = pingdatautil.JDBCExport(logger=logger)

dict_cs = {
    "driver": "C:\\Dev\\JDBC\\mssql-jdbc-10.2.1.jre8.jar",
    "class": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
    "jdbc": "jdbc:sqlserver://localhost:1433;databaseName=TEST;encrypt=false;trustServerCertificate=true",
    "user": "sa",
    "pass": "P@ssw0rd"
}

jd.with_data_date_column = "data_date"
jd.connect(dict_cs)
jd.count_records("SELECT COUNT(*) FROM DEMO_READER")
jd.execute_full("SELECT TOP 10 * FROM DEMO_READER", with_result=True)

jd.export_query_to_text("SELECT TOP 10 * FROM DEMO_READER", "D:\\TEMP\\BNK_JDBC.txt", separator=",")

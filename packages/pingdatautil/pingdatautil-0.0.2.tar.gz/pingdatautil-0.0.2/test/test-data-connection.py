import os
import pingdatautil

logger = pingdatautil.Logger()

dc = pingdatautil.DataConnection(logger=logger)

cs = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER=localhost;PORT=1433;DATABASE=TEST;UID=sa;PWD=P@ssw0rd;"

dc.connect(cs, mode="odbc")
dc.execute_full("SELECT @@VERSION", with_result=True)
dc.execute_fetch("SELECT * FROM bnk48_member")

os.environ["JAVA_HOME"] = "C:\\Dev\\openlogic-openjdk-jre-11.0.18+10-windows-x64"

dc2 = pingdatautil.DataConnection(logger=logger)

cs2 = {
"driver": "C:\\Dev\\JDBC\\mssql-jdbc-10.2.1.jre8.jar",
"class": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
"jdbc": "jdbc:sqlserver://localhost:1433;databaseName=TEST;encrypt=false;trustServerCertificate=true",
"user": "sa",
"pass": "P@ssw0rd"
}

dc2.connect(cs2, mode="jdbc")
dc2.execute_full("SELECT @@VERSION", with_result=True)
dc2.execute_fetch("SELECT * FROM bnk48_member")

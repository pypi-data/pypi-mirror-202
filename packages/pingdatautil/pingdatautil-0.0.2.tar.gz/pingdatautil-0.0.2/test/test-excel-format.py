import pandas as pd
import pingdatautil

logger = pingdatautil.Logger()

dc = pingdatautil.DataConnection(logger=logger)
cs = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER=localhost;PORT=1433;DATABASE=TEST;UID=sa;PWD=P@ssw0rd;"
dc.connect(cs, mode="odbc")

ex = pingdatautil.ExcelFormatter(logger=logger)

df = pd.read_sql("SELECT * FROM BNK48_MEMBER", con=dc.conn)

file_name = "D:\\TEMP\\BNK.xlsx"
sheet_name = "BNK48"

ex.set_config({"font-family": "Tahoma", "font-size": 10})

ex.df_to_excel(df, file_name, sheet_name)

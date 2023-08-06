import pandas as pd
import pingdatautil

logger = pingdatautil.Logger()

dc = pingdatautil.DataConnection(logger=logger)
cs = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER=localhost;PORT=1433;DATABASE=DEMO_DATA;UID=sa;PWD=P@ssw0rd;"
dc.connect(cs, mode="odbc")

ex = pingdatautil.ExcelFormatter(logger=logger)

df = pd.read_sql("SELECT TOP 1000 * FROM DEMO_SALES_1M", con=dc.conn)

file_name = "D:\\TEMP\\DATA.xlsx"
sheet_name = "DATA"

ex.set_config({"font-family": "Tahoma", "font-size": 10})

ex.df_to_excel(df, file_name, sheet_name)

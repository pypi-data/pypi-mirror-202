import pingdatautil

logger = pingdatautil.Logger()
gs = pingdatautil.GoogleSheet(logger=logger)

gs.authenticate_with_client_secret_file("D:\\TEMP\\bac-eppo-data.json")
gs.connect_sheet("EPPO Viz Data 2023")
gs.upload_csv("D:\\TEMP\\DEMO_READER.txt","DEMO_READER")


import pingdatautil

logger = pingdatautil.Logger()
az = pingdatautil.AzureStorage(logger=logger)

blob_account = "https://bacsynapsestorage.blob.core.windows.net"
blob_container = "storage"
blob_sas_token = "?sp=racwdlme&st=2021-06-22T11:26:30Z&se=2021-12-30T19:26:30Z&sip=0.0.0.0-255.255.255.255&spr=https&sv=2020-02-10&sr=c&sig=%2FWVTpt6Jf4CMV%2Fv9Vp74EBNXT55TXkJObWA7SXnpZX0%3D"

client_id = "9753b7fb-a4af-4f7b-8d30-3b6298bf6dbf"
client_secret = "v~9FoR-atweqxpgA.8Rx.bNQ-026_l696a"
tenant_id = "9c21bf6f-39b9-4076-94e0-3f72bcf282a9"

az.blob_connect_by_sas(blob_account, blob_container, blob_sas_token)
az.blob_connect_by_credential(blob_account, blob_container, tenant_id, client_id, client_secret)

# az.list_local_path("D:/TEMP/SPARK-TEST/")
# az.upload_recursive("D:/TEMP/SPARK-TEST/", "test-pq")
# az.delete_list_of_path("test-pq", ["ym=201601", "ym=201602"])
'''
temp_file = "D:/TEMP/test.txt"
f = open(temp_file, "w")
f.write("hello.txt")
f.close()

az.upload(temp_file, "temp/" + os.path.basename(temp_file))
az.upload_text(temp_file, "temp/" + os.path.basename(temp_file) + ".upload")

list_blob = az.list_blob_prefix("temp/test")
print(list_blob[0:10])

az.download("temp/test.txt", "D:/TEMP/test.txt")

for blob in list_blob:
    az.delete(blob)

list_blob = az.list_blob_prefix("temp/test")
print(list_blob[0:10])
'''

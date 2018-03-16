import requests
import zipfile
import os


files_ids = {'Medical':'1CZ6fybHlP4QDflDOUMSdRXSFvzZMZsQT', 'Music':'1lluYmeM0G4mY4i-QCfpFCOPf2kSgz4zO'}

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def unzip(path_to_zip_file, directory_to_extract_to):

    with zipfile.ZipFile(path_to_zip_file,"r") as zip_ref:
        zip_ref.extractall(directory_to_extract_to)


def download(datasetName):

    try:
        file_id = files_ids[datasetName]

        targetDir = '../Data/'
        tempZipFile = '../Data/data.zip'

        download_file_from_google_drive(file_id, tempZipFile)

        unzip(tempZipFile, targetDir)
        os.remove(tempZipFile)
    except:
        return False
    return True


if __name__ == "__main__":
    #https://drive.google.com/open?id=1yyOJjctsgvmtT9iRA3wB-VfaLDlBMs8z

    # for file_id in files_ids:

        # destination = '../Data/data.zip'
    file_id = '1CZ6fybHlP4QDflDOUMSdRXSFvzZMZsQT'
    download_file_from_google_drive(file_id, tempZipFile)

    unzip(tempZipFile, targetDir)
    os.remove(tempZipFile)

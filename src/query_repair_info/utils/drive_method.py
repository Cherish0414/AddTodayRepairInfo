from ..interface.drive_authenticate import authenticate
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import datetime
import logging

logger = logging.getLogger(__name__)

def upload_or_update(file_path, file_name) -> None:
    logger.info("Uploading to Google Drive...")
    service = authenticate()

    query = f"name='{file_name}' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    media = MediaFileUpload(file_path, resumable=True)
    if files:
        file_id = files[0]['id']
        updated = service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
        logger.info(f"Overwrite upload successful: {updated['name']}")
    else:
        file_metadata = {'name': file_name}
        uploaded = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        logger.info(f"Upload success: {file_name}")

def download_file(file_name, destination_path) -> int:
    tokyo_tz = datetime.timezone(datetime.timedelta(hours=9), 'Asia/Tokyo')
    current_date = datetime.datetime.now(tokyo_tz).date().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    
    try:
        service = authenticate()
        query = f"name='{file_name}' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name, modifiedTime)").execute()
        
        files = results.get('files', [])
        if not files:
            logger.error(f"No file named {file_name} found in Google Drive.")
            raise SystemExit(1)
        
        file_id = results.get('files', [])[0].get('id')
        file_modifiedtime = results.get('files', [])[0].get('modifiedTime')
        file_modifiedtime_dt = datetime.datetime.fromisoformat(file_modifiedtime.replace('Z', '+00:00')).astimezone(tokyo_tz)
        file_modifiedtime_str = file_modifiedtime_dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        
        logger.info(f"Found file: {files[0]['name']} (ID: {file_id}), modified at {file_modifiedtime_dt}")
        
        if file_modifiedtime_str > current_date:
            logger.info(f"and current time is {current_date}, file is newer than the current time; proceeding to download.")
            
            request = service.files().get_media(fileId=file_id)
                    
            with open(destination_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    logger.info(f"Download {int(status.progress() * 100)}%.")
            logger.info(f"File downloaded to {destination_path}")
        else:
            logger.warning("File is up-to-date; no download needed.")
            return 0
    except Exception as e:
        logger.error(f'Download File Error :{e}')
        raise SystemExit(1)
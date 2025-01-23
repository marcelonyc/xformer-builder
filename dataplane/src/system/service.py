import os
from config.app_config import get_settings
from sqlalchemy import delete
from database import database, file_manager
import logging


def delete_expired_files(files_list: list) -> bool:

    for file in files_list:
        file_id = file["file_id"]
        upload_id = file["upload_id"]

        delete_query = (
            delete(file_manager)
            .where(file_manager.c.file_id == file_id)
            .where(file_manager.c.upload_id == upload_id)
        )
        try:
            database.execute_sync(delete_query)
        except Exception as e:
            logging.error("Could not delete file_manager entry")

        try:
            get_settings().filestoreprovider.delete_file(file_id, upload_id)
        except Exception as e:
            logging.error("Could not delete file")

    return True

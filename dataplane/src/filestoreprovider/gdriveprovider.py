# Stores files in Google Drive
from filestoreprovider.base import FileStoreProvider
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os
import io


class GoogleDriverProvider(FileStoreProvider):

    def put_file(
        self,
        file_id: str,
        upload_id: str,
        stream: io.StringIO,
        is_transformed: bool = True,
    ):
        """Upload a file to the specified folder and prints file ID, folder ID
        Args: Id of the folder
        Returns: ID of the file uploaded

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        creds, _ = google.auth.default()

        try:
            # create drive api client
            service = build("drive", "v3", credentials=creds)

            file_metadata = {"name": "photo.jpg", "parents": [folder_id]}
            media = MediaFileUpload(
                "download.jpeg", mimetype="image/jpeg", resumable=True
            )
            # pylint: disable=maybe-no-member
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            print(f'File ID: "{file.get("id")}".')
            return file.get("id")

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None


# if __name__ == "__main__":
#   upload_to_folder(folder_id="1s0oKEZZXjImNngxHGnY0xed6Mw-tvspu")
# [END drive_upload_to_folder]

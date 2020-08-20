from flask import Flask, send_file
from flask_restful import Resource, Api
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import os
import io
#A comment
APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)
api = Api(app)

azure_conn_string = os.getenv("AZURE_CONNECTION_STRING")
azure_container_name = os.getenv("AZURE_CONTAINER_NAME")


class BlobList(Resource):
    def get(self):
        blob_service_client = BlobServiceClient.from_connection_string(
            azure_conn_string
        )

        container_client = blob_service_client.get_container_client(
            azure_container_name
        )

        blobs_list = container_client.list_blobs()

        # Create dictionary to store blob names in.
        json = {"blobs": []}

        for blob in blobs_list:
            # Build json object of names: var t = {blobs: [{name: 'picture.jpg'}, {name: 'background.png'}]}
            json["blobs"].append(blob.name)

        return json


class DownloadBlob(Resource):
    def get(self, filename):
        """ Take in string name and download blob from azure storage. """
        blob_service_client = BlobServiceClient.from_connection_string(
            azure_conn_string
        )

        container_client = blob_service_client.get_container_client(
            azure_container_name
        )

        blob_client = container_client.get_blob_client(filename)

        file_content = blob_client.download_blob()

        return send_file(
            io.BytesIO(file_content.readall()),
            attachment_filename=filename,
            mimetype="application/octet-stream",
            as_attachment=True,
        )

        return blob_client.download_blob()


api.add_resource(BlobList, "/list")
api.add_resource(DownloadBlob, "/download/<filename>")

if __name__ == "__main__":
    app.run(debug=True)

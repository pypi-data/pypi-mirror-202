from office365.runtime.auth.authentication_context import ClientCredential
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from typing import List, Union

import configparser
import os
import sys

class MSAPI(object):
	def __init__(self, cid, csec):
		dir = os.path.dirname(os.path.realpath(__file__))
		configs = configparser.ConfigParser()
		configs.read(dir + "/config.ini")

		self.base_url = configs["MS"]["BASE_URL"]
		self.client_id = cid
		self.client_secret = csec
		self.default_path = configs["PATH"]["SHAREPOINT_DEFAULT_PATH"]
	
		credentials = ClientCredential(self.client_id, self.client_secret)
		self.ctx = ClientContext(self.base_url).with_credentials(credentials)
	
	def check_path_exists(self, path: str) -> bool:
		if not path:
			return []

		try:
			return self.ctx.web.get_folder_by_server_relative_url(f"{self.default_path}/{path}").get().execute_query().exists
		except ClientRequestException as e:
			if e.response.status_code == 404:
				return None
			else:
				raise ValueError(e.response.text)

	def create_folder(self, path: str):
		if not path:
			return []

		self.ctx.web.folders.add(f"{self.default_path}/{path}").execute_query()
	
	def get_lists(self, path: str) -> Union[List, List]:
		target_path = self.default_path + "/" + path
		list_source = self.ctx.web.get_folder_by_server_relative_url(target_path)
		folders = list_source.folders
		files = list_source.files

		self.ctx.load(folders)
		self.ctx.load(files)
		self.ctx.execute_query()

		return folders, files

	def download_file(self, file: str, local_path: str):
		with open(local_path, "wb") as f:
			file.download(f)
			self.ctx.execute_query()
	
	def upload_file(self, upload_path: str, local_path: str):
		file_name = os.path.basename(local_path)
		target_path = self.default_path + "/" + upload_path
		try:
			target_folder = self.ctx.web.get_folder_by_server_relative_url(target_path)
			
			with open(local_path, "rb") as f:
				content = f.read()
				target_folder.upload_file(file_name, content).execute_query()
		except:
			print(f"[ERROR] Invalid Upload Path => {target_path}")
			print(sys.exc_info())
	
	def print_upload_progress(self, offset):
		print("Uploaded '{0}' bytes...".format(offset))   

	def upload_file_chunk(self, upload_path: str, local_path: str):
		target_path = self.default_path + "/" + upload_path
		try:
			target_folder = self.ctx.web.get_folder_by_server_relative_url(target_path)
			response = target_folder.files.create_upload_session(
				local_path, 10000000, self.print_upload_progress
			)

			self.ctx.execute_query()
			print(f"[INFO] {response.serverRelativeUrl} Success uploaded")
		except:
			print(f"[ERROR] Invalid Upload Path => {target_path}")
			print(sys.exc_info())



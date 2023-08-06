from api import MSAPI
import sys
import argparse
import os

def upload_dir(msapi, remote_dir, loc_dir):

	for file in os.listdir(loc_dir):
		path = '%s/%s' % (loc_dir, file)

		if os.path.isdir(path):
			ndir = '%s/%s' % (remote_dir, file)
			valid = msapi.check_path_exists(ndir)
			if valid is None:
				msapi.create_folder(ndir)

			upload_dir(msapi, ndir, path)
		else:
			msapi.upload_file_chunk(remote_dir, path)
		

def upload_data(cid: str, csec: str, dir_path: str, loc_path: str):
	m = MSAPI(cid, csec)
	dirs = [d for d in dir_path.split("/") if d]
	
	for i in range(len(dirs)):
		path = "/".join(dirs[:i+1])
		valid = m.check_path_exists(path)

		if valid is None:
			m.create_folder(path)
	
	if os.path.isfile(loc_path):
		m.upload_file_chunk(dir_path, loc_path)
	else:
		upload_dir(m, dir_path, loc_path)


if __name__ == "__main__":
	# upload_data("자료실/빌드 테스트", "C:\\Users\\Administrator\\Desktop\\abc.zip")

	parser = argparse.ArgumentParser(description='share point')
	parser.add_argument("filename", help="the file to be uploaded")
	parser.add_argument("-d", "--dest", help="destination folder")
	parser.add_argument("-c", "--client-id", help="client id")
	parser.add_argument("-s", "--client-secret", help="client secret")

	args = parser.parse_args()

	upload_data(args.client_id, args.client_secret, args.dest, args.filename)

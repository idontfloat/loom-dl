import argparse
import json
import urllib.request

def fetch_loom_download_url(id):
	request = urllib.request.Request(
		url=f"https://www.loom.com/api/campaigns/sessions/{id}/transcoded-url",
		headers={},
		method="POST",
	)
	response = urllib.request.urlopen(request)
	body = response.read()
	content = json.loads(body.decode("utf-8"))
	url = content["url"]
	return url

def download_loom_video(url, filename):
	urllib.request.urlretrieve(url, filename)

def parse_arguments():
	parser = argparse.ArgumentParser(
		prog="loom-dl", description="script to download loom.com videos"
	)
	parser.add_argument(
		"url", help="Url of the video in the format https://www.loom.com/share/[ID]"
	)
	parser.add_argument("-o", "--out", help="Path to output the file to")
	arguments = parser.parse_args()
	return arguments

def extract_id(url):
	id = url.split("/")[-1]
	return id.split("?")[-2] if "?" in id else id

def main():
	arguments = parse_arguments()
	id = extract_id(arguments.url)
	url = fetch_loom_download_url(id)
	filename = arguments.out or f"{id}"
	if filename[-4:] != ".mp4":
		filename += ".mp4"
	print(f"Downloading video {id} and saving to {filename}")
	download_loom_video(url, filename)

if __name__ == "__main__":
	main()

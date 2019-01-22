#!/usr/bin/python2
#encoding:utf-8
import os
import sys
import requests
from make_colors import make_colors
from debug import debug
import wget
from urlparse import urlparse
import re
import clipboard
from datetime import datetime

class pdflayer(object):
	"""docstring for pdflayer"""
	def __init__(self, url=None, name="", download_path=None):
		super(pdflayer, self)#.__init__()
		self.url = url
		self.URL = "https://api.pdflayer.com/api/convert?access_key=5d6d3337836459972acfb0650653e4a4&inline=1&document_url={0}&document_name={1}.pdf"
		# self.URL = "https://pdflayer.com/php_helper_scripts/pdf_api.php?url={0}&secret_key=03a5c1d46810b9cb380e6df6e01cfc66"
		self.session = requests.Session()

	def formatURL(self, url=None, name=None):
		if not name:
			name = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
		debug(name=name)
		if not url:
			url = self.url
		debug(url=url)
		if url:
			self.URL = self.URL.format(url, name)
			debug(self_URL=self.URL)
		else:
			print make_colors('No Name Definition ~!', 'lightwhile', 'lightred')
		return self.URL


	def getName(self, url):
		up = urlparse(url).path
		debug(up=up)
		up = re.split("/", up)
		debug(up=up)
		for i in up:
			if str(i).strip() == '':
				up.remove(i)
		name = up[-1] + ".pdf"
		debug(name=name)
		return name

	def download(self, url, name=None, download_path=os.getcwd()):
		destination = ''
		if os.getenv('DOWNLOAD_PATH') and os.path.exists(os.getenv('DOWNLOAD_PATH')):
			download_path = os.getenv('DOWNLOAD_PATH')
		if not name:
			name = self.name
		if not name:
			name = raw_input('NAME: ')
		if not name:
			print make_colors('No Name Definition ~!', 'lightwhile', 'lightred')
			return False
		if not os.path.splitext(name)[1] == '.pdf':
			name = name + ".pdf"
		destination = os.path.join(destination, name)
		if self.url:
			url = self.url
		response = self.session.get(url, stream=True)
		try:
			from progressbar import ProgressBar, Bar, Percentage, FileTransferSpeed, ETA
			class ReFileTransferSpeed(FileTransferSpeed):
				def update(self, pbar):
				    if 45 < pbar.percentage() < 80:
				        return "Bigger Now" + FileTransferSpeed.update(self, pbar)
				    else:
				        return FileTransferSpeed.update(self, pbar)
			widgets = [ReFileTransferSpeed(), "<<<", Bar(), ">>>", Percentage(), ' ', ETA()]
			pbar = ProgressBar(widgets=widgets, max_value=100)
		except:
			pass
		CHUNK_SIZE = 32768
		with open(destination, "wb") as f:
			pbar.start()
			for chunk in response.iter_content(CHUNK_SIZE):
			    try:
			        pbar.update(1)
			    except:
			        pass
			    if chunk:  # filter out keep-alive new chunks
			        f.write(chunk)
		pbar.finish()

	def download_1(self, url, name=None, download_path=os.getcwd()):
		if not name:
			name = self.getName(url)
		if os.getenv('DOWNLOAD_PATH') and os.path.exists(os.getenv('DOWNLOAD_PATH')):
			download_path = os.getenv('DOWNLOAD_PATH')
		if download_path:
			if name:
				download_path = os.path.join(download_path, name)
		URL = self.formatURL(url, name)
		debug(URL=URL)
		clipboard.copy(URL)
		name = wget.download(URL, download_path)
		return name

	def usage(self):
		import argparse
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('URL', action='store', help='Url convert to')
		parser.add_argument('-p', '--download-path', action='store', help='Save to', default=os.getcwd())
		parser.add_argument('-n', '--name', action='store', help='Name (Optional) Save to')
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			if args.URL:
				self.download_1(args.URL, args.name, args.download_path)

if __name__ == '__main__':
	c = pdflayer()
	c.usage()
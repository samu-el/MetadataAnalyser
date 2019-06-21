#! python3
'''THE COMMANDLINE TOOL HERE'''

 
import os
import sys
from PyPDF2 import PdfFileReader
import exifread
import docx
import pprint
# from file_metadata.generic_file import GenericFile
#https://github.com/atdsaa/file-metadata with few modifications to  utilities.py
from file_metadata.generic_file import GenericFile




def get_generic_file_info(path):
	gf = GenericFile.create(path)
	return gf.analyze()

# def get_file_type(path):
# 	kind = filetype.guess(path)
# 	if kind is None:
# 		print('Cannot guess file type!')
# 		return
# 	return kind.extension


def get_docx_info(path):
	document = docx.Document(docx = path)
	core_properties = document.core_properties
	info = { 
		"created":core_properties.created,
		"last_modified_by": core_properties.last_modified_by,
		"last_printed": core_properties.last_printed,
		"modified": core_properties.modified,
		"revision": core_properties.revision,
		"title": core_properties.title,
		"category": core_properties.category,
		"comments": core_properties.comments,
		"identifier": core_properties.identifier,
		"keywords": core_properties.keywords,
		"language": core_properties.language,
		"subject": core_properties.subject,
		"version": core_properties.version,
		"keywords": core_properties.keywords,
		"content_status": core_properties.content_status
	}
	return info

def get_image_info(path):
	print(path)
	f = open(path, 'rb') 
	tags = exifread.process_file(f)	
	for tag in tags.keys():
		if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
			print("%s: %s" % (tag, tags[tag]))

	return tags

 
def get_pdf_info(path):
	with open(path, 'rb') as f:
		pdf = PdfFileReader(f)
		info = pdf.getDocumentInfo()
		info['number_of_pages'] = pdf.getNumPages()
	return info

def main():
	if len(sys.argv) < 3:
		print('USAGE: python analaser.py [-i/-p/-d/-g] [filepath]')
		print(' -i: image \n -p: pdf \n -d: docx\n -g: any generic file')
		return
	ftype = sys.argv[1]
	path = sys.argv[2]
	if ftype.lower() =='-g':
		info = get_generic_file_info(path)
	elif ftype.lower() == '-i':
		info = get_image_info(path)
	elif ftype.lower() == '-p':
		info = get_pdf_info(path)
	elif ftype.lower() == '-d':
		info = get_docx_info(path)
	pprint.pprint(info)
	if ftype != '-g':
		more_info = get_generic_file_info(path)
		print('More Data');
		pprint.pprint(more_info)

if __name__ == '__main__':
	
	main()

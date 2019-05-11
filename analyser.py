#! python3
'''THE COMMANDLINE TOOL HERE'''

 
import os
import sys
from PyPDF2 import PdfFileReader
import exifread
import docx
import pprint

#https://github.com/atdsaa/file-metadata with few modifications to  utilities.py
from file_metadata.generic_file import GenericFile




def get_generic_file_info(path):
	gf = GenericFile.create(path)
	return gf.analyze()




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
	with open(path, 'rb') as f:
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

if __name__ == '__main__':
    path = sys.argv[1]
    # get_pdf_info(path)
    # get_image_info(path)
    # get_docx_info(path)
    info = get_generic_file_info(path)
    pprint.pprint(info)
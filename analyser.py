#! python3
'''THE COMMANDLINE TOOL HERE'''

 
import os
import sys
from PyPDF2 import PdfFileReader
import exifread
import docx
# from file_metadata.generic_file import GenericFile



# def get_generic_file_info(path):
# 	gf = GenericFile.create(path)
# 	gf.analyse()




def get_docx_info(path):
	document = docx.Document(docx = path)
	core_properties = document.core_properties
	print("Created:", core_properties.created)
	print("Last Modified By:", core_properties.last_modified_by)
	print("Last Printed:", core_properties.last_printed)
	print("Modified:", core_properties.modified)
	print("Revision:", core_properties.revision)
	print("Title:", core_properties.title)
	print("Category:", core_properties.category)
	print("Comments:", core_properties.comments)
	print("Identifier:", core_properties.identifier)
	print("Keywords:", core_properties.keywords)
	print("Language:", core_properties.language)
	print("Subject:", core_properties.subject)
	print("Version:", core_properties.version)
	print("Keywords:", core_properties.keywords)
	print("Content Status:", core_properties.content_status)

def get_image_info(path):
	with open(path, 'rb') as f:
		tags = exifread.process_file(f)
		for tag in tags.keys():
			if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
				print("%s: %s" % (tag, tags[tag]))

 
def get_pdf_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    author = info.author
    creator = info.creator
    producer = info.producer
    subject = info.subject
    title = info.title
   
    print(info)
 
if __name__ == '__main__':
    path = sys.argv[1]
    # get_pdf_info(path)
    # get_image_info(path)
    get_docx_info(path)
import os
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from os import listdir
from os.path import isfile, join
from shutil import copyfile



def decrypt_pdf(input_path, output_path, password):
  with open(input_path, 'rb') as input_file, \
    open(output_path, 'wb') as output_file:
    print ("Trying to decrypt file  ...",input_path)
    reader = PdfFileReader(input_file)
    reader.decrypt(password)

    writer = PdfFileWriter()

    for i in range(reader.getNumPages()):
      writer.addPage(reader.getPage(i))

    writer.write(output_file)
    print ("Cleaning up file ...", input_path)
    os.remove(input_path)
    # Delete the source file here

def list_files(input_path):
    onlyfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    print ("List of files identified are...")
    for p in onlyfiles:
        print (p)
    return onlyfiles

# This scripts expected the encrypted files in the encrypted directory and pushes out the files to the
# Decrypted folder.
if __name__ == '__main__':
  filesname = list_files("encrypted/");
  for p in filesname:
      decrypt_pdf("encrypted/"+p, "decrypted/decrypted_"+p, 'VIK1706')

  filesname = list_files("decrypted/");
   # Now read the content from the files
  for p in filesname:
    print ("Reading filename" + p)
    if "pdf" in p:
        print ("Parsing.."+p)
        pdf_file = open('decrypted/'+p, 'rb')
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        if "Gold" in page_content:
            print ("Gold Exists in..." + p);
            print (page_content.split("Gold", 1)[1]);
            # Move this to  a different folder
            copyfile('decrypted/' + p, 'GOLDBEES/' + p)
        else:
            print ("Nah...")
    else:
        print ("Ignoring..."+p)

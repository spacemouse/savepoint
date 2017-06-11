from __future__ import ( division, absolute_import, print_function, unicode_literals )

import sys, os, tempfile, logging
import json
import errno

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def download_file(url, filename=None, desc=None):
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    #filename = os.path.basename(path)
    if not filename:
        filename = os.path.basename(path)
    if desc:
        filename = os.path.join(desc, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename

#url = "https://tgchan.org/kusaba/questarch/src/145231416198.png"
infile = input("Specify input JSON file: ")
outfile = input("Specify output JSON file: ")
destfolder = input("Specify output folder for images: ")


# first make sure that path exists for output
make_sure_path_exists(destfolder)
thenum = 1;

with open(infile, mode='r', encoding='utf-8') as fin:
    thejson = json.load(fin) #load old json
    newjson = {'pages' : [{}]} #begin writing new json
    for i in thejson['pages']:
#        print(i)
        if (thenum > 1):
            # the first one is blank, so this is to check that
            # now we import the json values
            pagenum = str(i[0]['pagenum'])
            img = i[0]['img']
            text = i[0]['text']

            sourcefilename = img.split('/')[-1] #get the filename
            filextension = sourcefilename.split('.')[-1] #get the extension
            destname = pagenum + "." + filextension
            filename = download_file(img,destname,destfolder)
            #now append to json
            newpage = [{'pagenum' : pagenum, 'img' : (destfolder+destname), 'text' : text}]
            #newjson = {'pages' : newpage }
            newjson['pages'].append(newpage)
        thenum = thenum + 1

with open(outfile, mode='w', encoding='utf-8') as fout:
    json.dump(newjson,fout, indent=4, sort_keys=True)

print("Done.")

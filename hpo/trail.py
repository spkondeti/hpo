import urllib.request,urllib.parse,mimetypes,hashlib,contextlib,os,sys,tempfile,shutil

def fetch_images(etree):
    with pushd_temp_dir():
        temp2 = etree.findall(".//img")
        for img in temp2:
            if img is not None:
                img = str(img.get('src'))
                img = "https://blog.hubspot.com/marketing/gif-websites/"+img
                img = "https://blog.hubspot.com/hs-fs/hubfs/CF7qD5A_-_Imgur.gif?width=894&height=503&name=CF7qD5A_-_Imgur.gif"
                img_read = urllib.request.urlopen(img)
                extension = mimetypes.guess_extension(img_read.info().get('Content-Type'))
                with open(make_filename(img,extension),"wb") as file:
                    file.write(img_read.read())
                    print("Done")

@contextlib.contextmanager
def pushd_temp_dir(base_dir=None, prefix="tmp.hpo."):
    if base_dir is None:
        proj_dir = sys.path[0]
        main_dir = os.path.join(proj_dir, "data")
    temp_dir_path = tempfile.mkdtemp(prefix=prefix, dir=base_dir)
    try:
        start_dir = os.getcwd()  # get current working directory
        os.chdir(temp_dir_path)  # change to the new temp directory
        try:
            yield
        finally:
            os.chdir(start_dir)
    finally:
        shutil.rmtree(temp_dir_path, ignore_errors=True)


def make_filename(url, extension):
    encoded_url = url.encode('utf8')
    return hashlib.sha1(encoded_url).hexdigest()+extension


def make_etree(html,url,charset="UTF-8",absolute_links=True):
    from lxml.html import HTMLParser, document_fromstring
    parser = HTMLParser(encoding="UTF-8")
    root = document_fromstring(html, parser=parser, base_url=url)
    return root

url = "https://blog.hubspot.com/marketing/gif-websites"
req = urllib.request.Request(url)
response = urllib.request.urlopen(req).read()   #Reading Bytes
response = response.decode("UTF-8")           #Converting Bytes to String
base_string = "<base href=%s>\n" %url
response = response.replace('<head>','<head>'+'\n'+base_string)
tree = make_etree(response,url)
fetch_images(tree)
#!/usr/local/bin/python3.4
import flask,os,urllib.request,sys, tempfile, shutil, contextlib, collections,hashlib,urllib.parse,mimetypes,cv2

app = flask.Flask(__name__)
@app.route('/')
def root_page():
    return flask.render_template('root.html')
@app.route('/view')
def view_page():
    from flask import flash
    url = flask.request.args['url']
    social_list = ['facebook','twitter','linkedin','youtube','pinterest','instagram','tumblr','flickr','reddit','snapchat','whatsapp','quora','vine','fb']
    validate = bool(urllib.parse.urlparse(str(url)).scheme)
    netloc = urllib.parse.urlparse(str(url)).netloc
    if validate and (any(x in netloc.lower() for x in social_list) is False):
        req = urllib.request.Request(url)
        req.add_header('Referer', 'http://www.python.org/')
        req.add_header('User-Agent', 'PurdueUniversityClassProject/1.0 (skondeti@purdue.edu https://goo.gl/dk8u5S)')
        # Credit: Adapted from example in Python 3.4 Documentation, urllib.request
        #         License: PSFL https://www.python.org/download/releases/3.4.1/license/
        #                  https://docs.python.org/3.4/library/urllib.request.html
        #Lines 15,16,17 are extracted from this source
        response = urllib.request.urlopen(req).read()   #Reading Bytes
        response = response.decode("UTF-8")           #Converting Bytes to String
        base_string = "<base href=%s>\n" %url
        response = response.replace('<head>','<head>'+'\n'+base_string)
        _make_etree(response,url)
        return response
    else:
        flash("Invalid/Unsupported URL Entered!!! Please Try Again.") #Flash Error Message
        return flask.render_template('root.html')

def _make_etree(html,url,charset="UTF-8",absolute_links=True):
    from lxml.html import HTMLParser, document_fromstring
    parser = HTMLParser(encoding="UTF-8")
    root = document_fromstring(html, parser=parser, base_url=url)
    x = fetch_images(root)
    #return root

def make_filename(url, extension):
    encoded_url = url.encode('utf8')
    return hashlib.sha1(encoded_url).hexdigest()+extension

@contextlib.contextmanager
def fetch_images(etree):
    with pushd_temp_dir():
        filename_to_node = collections.OrderedDict()
        temp2 = etree.findall(".//img")
        for img in temp2:
            if img is not None:
                img = str(img.get('src'))
                img_read = urllib.request.urlopen(img)
                extension = mimetypes.guess_extension(img_read.info().get('Content-Type'))
                with open(make_filename(img,extension),"wb") as file:
                    file.write(img_read.read())
        yield filename_to_node

def get_image_info(filename):
    img = cv2.imread(filename,0)
    height, width = img.shape[:2]
    dim_dict = dict()
    dim_dict["w"] = width
    dim_dict["h"] = height
    return dim_dict


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

if __name__ == '__main__':
    app.secret_key = "random_key" #Random key to run flash message system
    app.run(host="127.0.0.1", port=os.environ.get("ECE364_HTTP_PORT", 8000),use_reloader=True, use_evalex=False, debug=True, use_debugger=False)

from flask import Flask, render_template, request,make_response
from bs4 import BeautifulSoup
from urllib.request import urlopen
from headless import visit_with_cookies
import threading,magic,os
from io import BytesIO
from PIL import Image
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from lxml.html.clean import Cleaner



KEEP_ATTRIBUTES = ['src','charset']

app = Flask(__name__)
url = 'http://localhost:8001'

limiter = Limiter(get_remote_address, app=app, default_limits=["2000 per day", "500 per hour"])

def removeScriptContent(tag):
    soup = BeautifulSoup(tag,"html.parser")
    soup.script.clear()
    return soup


def cleaner(str):
    try:
        cleaner = Cleaner(page_structure=False)
        cleaner.javascript=True
        cleaner.scripts=True
        cleaner.kill_tags=["base"]
        return cleaner.clean_html(str)
    except Exception:
        return 'Error in cleaning'

def removeTags(doc):
    soup = BeautifulSoup(doc)
    for tag in soup.descendants:
        for k in list(tag.attrs.keys()):
            if k not in KEEP_ATTRIBUTES:
                tag.attrs.pop(k, None)
    tag = soup.find_all("script")
    return tag[0]

def getType(uri):
    try:
        with urlopen(uri) as request:
            data = request.read()
            type = magic.from_buffer(data, mime=True)
            return type
    except Exception:
        return "Invalid Datauri"

def check_exif(uri):
    try:
        file = BytesIO((urlopen(uri).read()))
        with Image.open(file, mode='r', formats=['JPEG']) as im:
            exif_fields = list(im.info.keys())
            if 'exif' not in exif_fields:
                return True
            else:
                return False
    except:
        return False
        

@app.route("/", methods = ['GET'])
def homepage():
    resp = make_response(render_template('index.html'))
    return resp

@app.route("/review" , methods = ['POST' , 'GET'])
@limiter.limit("1 per second")
def index():
    if request.method == 'POST':
        
        content = request.form['content']
        content = cleaner(content)
        if len(content) > 1000000:
            return make_response(render_template('thanks.html'))

        soup = BeautifulSoup(content, "html.parser")
        image_tags = soup.find_all("img")
        valid_image_srcs = {'images':[]}
        target_image_tag = {'images':[]}

        for image_tag in image_tags:
            try:
                uri = image_tag['src']
            except:
                continue
            file_ext = getType(uri)
            if file_ext in ['image/jpeg']:
                try:
                    if check_exif(uri) == False:
                        continue
                except:
                    continue
                valid_image_srcs['images'].append(uri)
            
            elif file_ext == 'image/svg+xml':
                try:
                    
                    with urlopen(uri) as response:
                        svgContent = response.read()
                        svgContent.decode()
                        soup2 = BeautifulSoup(svgContent,'html')
                        innerImageTags = soup2.find_all("script")
                        if len(innerImageTags) == 0:
                            target_image_tag["images"].append("")
                            resp =  make_response(render_template('view.html',images = valid_image_srcs, main_images = target_image_tag))
                            return resp
                        
                        innerImageTag = innerImageTags[0]
                    
                        try:
                            svguri = innerImageTag['src']
                        except:
                            target_image_tag["images"].append("")
                            resp =  make_response(render_template('view.html',images = valid_image_srcs, main_images = target_image_tag))
                            return resp
                        
                        file_ext = getType(svguri)
                        if file_ext in ['image/jpeg']:
                            if check_exif(svguri) == False:
                                target_image_tag["images"].append("")
                                resp =  make_response(render_template('view.html',images = valid_image_srcs, main_images = target_image_tag))
                                return resp
                            
                            innerImageTag = removeScriptContent(innerImageTag.__str__())
                            
                            innerImageTag = removeTags(innerImageTag.__str__())

                            try:
                                t1 = threading.Thread(target = visit_with_cookies, args = (url,innerImageTag))
                                t1.start()
                            except:
                                target_image_tag["images"].append("Admin couldn't get to you try again")
                                resp =  make_response(render_template('view.html',images = valid_image_srcs, main_images = target_image_tag))
                                return resp
                            
                            target_image_tag['images'].append(innerImageTag)
                except Exception:
                    target_image_tag["images"].append("Invalid Uri")
                    resp =  make_response(render_template('view.html',images = valid_image_srcs, main_images = target_image_tag))
                    return resp                
        
        resp =  make_response(render_template('view.html',images = valid_image_srcs, main_images = target_image_tag))
        return resp         
        
            
    else:
        resp =  make_response(render_template('index.html'))
        return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=False)

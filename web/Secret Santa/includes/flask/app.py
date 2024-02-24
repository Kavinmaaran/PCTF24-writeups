from flask import Flask, request, Response,make_response
from flask_cors import CORS
from lxml import etree
from io import StringIO
import logging
from config import FRONTEND_URL
app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":[FRONTEND_URL]}})
app.config['CORS_HEADERS'] = 'Content-Type'

with open('gift.txt', 'r') as file:
    flag = file.read()



def create_file(fileinput, content):
  try:
    with open(fileinput, 'w') as f:
      f.write(content)
      f.close()
      f = open(fileinput, 'r')
      f.close()
  except:
    logging.exception('failed to create file')


def setup():
  create_file('/gift', flag)
  

setup()



@app.route('/you_know_who', methods=['POST'])
def get_server_info_route():
    try:
        data_type=request.content_type
        if(data_type=='application/xml'):
            xml_data_from_frontend = request.data.decode('utf-8')
            xml_file = StringIO(xml_data_from_frontend)


            if ".dtd" in xml_data_from_frontend:
                if "yelp" not in xml_data_from_frontend:
                    return Response("I know you've all survived the biggest apocalypse, but you need to survive the yelpocalypse",status=400,content_type='application/xml')
                else:
                    parser = etree.XMLParser(dtd_validation=True,load_dtd=True, no_network=False,huge_tree=True,resolve_entities=False)


                    tree = etree.parse(xml_file, parser=parser)

                    
                    root = tree.getroot()
                    print(root.text)
                    if(root.text is None):
                        return Response("None",status=400,content_type='application/xml')
                    
                    return Response(root.text,status=400, content_type='application/xml')

            else:
                parser = etree.XMLParser(dtd_validation=True,load_dtd=True, no_network=False,huge_tree=True,resolve_entities=False)

             
                tree = etree.parse(xml_file, parser=parser)

                
                root = tree.getroot()
                print(root.text)
                if(root.text is None):
                    return Response("Sorry, the XML parser didn't return anything",status=400,content_type='application/xml')
                
        else:
            return Response("This data format is not supported for your gift",content_type='application/xml',status=400)
            

    except etree.Error as e:
        return Response(str(e), status=400, content_type='application/xml')
    except TypeError as e:
        return Response(str(e), status=400, content_type='application/xml')

#dev mode
if __name__ == '__main__':
    app.run(port=5000)

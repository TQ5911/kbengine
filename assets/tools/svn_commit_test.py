# -*- coding: utf-8 -*-
import json 
import requests
data = {
  "ver":14488,
  "files":["test/packer_pyctest.py","packer_pyc_back0.py","packer_pyc.bat1"],
}
url = 'http://127.0.0.1:8234/update'
  
r = requests.post(url,data=json.dumps(data))
print(r.text) 


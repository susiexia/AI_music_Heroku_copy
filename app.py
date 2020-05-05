from flask import Flask, render_template, request
#from euwerkzg import secure_filename
from werkzeug.utils import secure_filename

import URLtest_predict_pipeline
import cloudinary
import cloudinary.uploader

from app_config import cloud_api_key

app = Flask(__name__)
app.config["ALLOWED_EXTENSIONS"] = ["wav", "WAV"]


@app.route('/')
def first_upload_file():
   return render_template('upload_LH.html')



@app.route('/uploader', methods = ['POST','GET'])
# @app.route('/uploader')
def upload_file():
   
   if request.method == 'POST': 
      f = request.files['file']
      if   not "." in f.filename:
         return render_template('error.html')
      
      ext = f.filename.rsplit(".", 1)[1]

      if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
         
         #f.save(secure_filename(f.filename))
         #file_name = (f.filename)

         #result = cloudinary.uploader.unsigned_upload(f, upload_preset= 'q8vijdwg', cloud_name = 'dmqj5ypfp', resource_type='auto' )
         result = cloudinary.uploader.upload(f, api_key =cloud_api_key, api_secret = 'oE0lsB5Y-h5nJZbzlphcWgVBMhY', cloud_name = 'lulu666666', resource_type = 'video', use_filename = True, unique_filename= False)
         wavURL = result['url']

         predicted_pitch = URLtest_predict_pipeline.predict_pitch(wavURL)
         predicted_inst = URLtest_predict_pipeline.predict_instrument(wavURL)
         # for play audio part
         version = wavURL

         return render_template('dashboard.html',predicted_pitch = predicted_pitch, predicted_inst = predicted_inst, version = version)
      else: 
         #return "file type error"
         return render_template('error.html')

        

if __name__ == '__main__':
   #app.run(threaded=False)
   app.run(debug = True)
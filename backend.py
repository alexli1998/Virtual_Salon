from flask import Flask, jsonify, render_template, request
from os import path, system
from flask_ngrok import run_with_ngrok

import torch
from Face_parsing.test import parsing
from StarGAN_v2.test import make_img
from SEAN.test import reconstruct
from args.prepare import args_prepare

app = Flask(__name__)
project_path = path.abspath(path.dirname(__file__))
run_with_ngrok(app)  # Start ngrok when app is run
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

args = args_prepare()

@app.route('/')
def mainpage():
	return render_template('virtualsalon.html')


@app.route('/upload_img', methods=['GET', 'POST'])
def upload_img():
	if request.method == 'POST':
		img = request.files['file']
		# print(img.filename)
		img.save(path.join(project_path, 'static', 'received', img.filename.split('.')[0] + '.png'))
		print('an image is saved: ./static/received/' + img.filename.split('.')[0] + '.png')
		return ''
	if request.method == 'GET':
		# print(request.values.get('img'))
		img_name = request.values.get('img').split('.')[0] + '.png'
		return jsonify({'url': '/static/received/' + img_name})


@app.route('/get_recommendation', methods=['GET', 'POST'])
def get_recommendation():
  print('get_recommendation')
  if request.method == 'POST':
    print('process')
    img_name = request.values.get('img').split('.')[0] + '.png'
    system('rm -rf /content/Virtual_Salon/data/src/src/*')
    system('cp /content/Virtual_Salon/static/received/' + img_name + ' /content/Virtual_Salon/data/src/src')
    main(args)
    return ''
  if request.method == 'GET':
    return jsonify({'url': '/static/generate/gen.png'})



def main(args):
  print(args)
  torch.manual_seed(args.seed)

  if args.mode == 'dyeing':
      # Parsing > SEAN
      parsing(respth='./results/label/src' ,dspth='./data/src/src') # parsing src_image
      parsing(respth='./results/label/others', dspth='./data/dyeing') # parsing ref_image
      reconstruct(args.mode)
      
      
  elif args.mode == 'styling_ref':
      # StarGAN > Parsing > SEAN
      make_img(args) 
      parsing(respth='./results/label/src', dspth='./data/src/src') # parsing src_image
      parsing(respth='./results/label/others', dspth='./results/img') # parsing fake_image
      reconstruct(args.mode)

  elif args.mode == 'styling_rand':
      # StarGAN > Parsing > SEAN
      make_img(args)
      parsing(respth='./results/label/src', dspth='./data/src/src')
      parsing(respth='./results/label/others', dspth='./results/img') # parsing fake_image
      reconstruct(args.mode)
  
  else:
      raise NotImplementedError


if __name__ == '__main__':
	app.run()

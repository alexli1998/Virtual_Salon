from flask import Flask, jsonify, render_template, request
from os import path, system, listdir
from flask_ngrok import run_with_ngrok
from edit_bangs import *
from similarity import *
import torch
from Face_parsing.test import parsing
from StarGAN_v2.test import make_img
from SEAN.test import reconstruct
from args.prepare import args_prepare
from utils.clear import clear_tmp_file
from utils.color import choose_color

app = Flask(__name__)
project_path = path.abspath(path.dirname(__file__))
run_with_ngrok(app)  # Start ngrok when app is run
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


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


@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
  print(request.values.get('img'))
  system("nvidia-smi")
  imgpath = './static/received/' + request.values.get('img').split('.')[0] + '.png'
  recimgpath = similarity(imgpath)
  system("nvidia-smi")
  return jsonify({'url1': recimgpath[0], 'url2': recimgpath[1], 'url3': recimgpath[2]})
  # return jsonify({'url1': './static/images/01.PNG', 'url2': './static/images/02.PNG', 'url3': './static/images/03.PNG'})


@app.route('/generate', methods=['GET', 'POST'])
def generate():
  print('generate')
  if request.method == 'POST':
    print('process')
    # return ''
    color = request.values.get('color')
    ref = request.values.get('ref')
    print('color: '+ color + ', ref img:' + ref)

    ref_name = ref.split('/')[-1]
    print(ref_name)
    img_name = request.values.get('img').split('.')[0] + '.png'
    options = {0: 'color', 1: 'style', 2: 'color and style'}
    choice = 0
    args = args_prepare()
    system("nvidia-smi")
    if len(color) == 0 and len(ref) == 0:
      return ''
    if len(color) > 0:
      # if (img_name not in listdir('/content/Virtual_Salon/static/generate')):
        system('rm -rf /content/Virtual_Salon/data/src/src/*')
        system('cp /content/Virtual_Salon/static/received/' + img_name + ' /content/Virtual_Salon/data/src/src')
        clear_tmp_file()
        print("choose color: ", color)
        choose_color(color)
        args.mode = 'dyeing'
        with torch.no_grad():
          main(args)
        choice = 0
    if len(ref) > 0:
      if len(color) > 0:
        system('rm -rf /content/Virtual_Salon/data/src/src/*')
        system('rm -rf /content/Virtual_Salon/data/ref/ref/*')
        clear_tmp_file()
        system('cp /content/Virtual_Salon/static/generate/' + img_name + ' /content/Virtual_Salon/data/src/src')
        system('cp /content/Virtual_Salon/static/ref/' + ref_name + ' /content/Virtual_Salon/data/ref/ref/')
        choice = 2
      else:
        system('rm -rf /content/Virtual_Salon/data/src/src/*')
        system('rm -rf /content/Virtual_Salon/data/ref/ref/*')
        clear_tmp_file()
        system('cp /content/Virtual_Salon/static/received/' + img_name + ' /content/Virtual_Salon/data/src/src')
        system('cp /content/Virtual_Salon/static/ref/' + ref_name + ' /content/Virtual_Salon/data/ref/ref/')
        choice = 1
      args.mode = 'styling_ref'
      with torch.no_grad():
        main(args)
    print("select mode: %s" % (options[choice]))
    system("nvidia-smi")
    return ''
  if request.method == 'GET':
    img_name = request.values.get('img').split('.')[0] + '.png'
    color = request.values.get('color')
    ref = request.values.get('ref').split('.')[0] + '.png'
    torch.cuda.empty_cache()
    system("nvidia-smi")
    return jsonify({'url': '/static/generate/' + img_name})
    # return jsonify({'url': '/static/generate/gen.png'})




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


@app.route('/adjust', methods=['GET', 'POST'])
def adjust():
  # imgpath = '/static/generate/' + request.values.get('img') + '.png'
  imgpath = './static/generate/' + request.values.get('img')
  print(imgpath)
  system("nvidia-smi")
  frame_path,video_path = edit_bangs(imgpath, iterations=2)
  system("nvidia-smi")
  return get_base64(frame_path)


if __name__ == '__main__':
	app.run()

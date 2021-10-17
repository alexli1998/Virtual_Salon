from flask import Flask, jsonify, render_template, request
from os import path
from flask_ngrok import run_with_ngrok

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


@app.route('/get_recommendation', methods=['GET', 'POST'])
def get_recommendation():
  print('get_recommendation')
  if request.method == 'POST':
    print('process')
    return ''
  if request.method == 'GET':
    return jsonify({'url': '/static/images/LOGO.png'})


if __name__ == '__main__':
	app.run()

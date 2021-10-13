from flask import Flask, jsonify, render_template, request
from os import path

app = Flask(__name__)
project_path = path.abspath(path.dirname(__file__))

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
		img_name = request.values.get('img')
		return jsonify({'url': 'http://127.0.0.1:5000/static/received/' + img_name})


@app.route('/get_recommendation')
def get_recommendation():
	print('get_recommendation')
	return jsonify({'url': 'http://127.0.0.1:5000/static/images/LOGO.png'})


if __name__ == '__main__':
	app.run()

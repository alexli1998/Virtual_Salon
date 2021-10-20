# -*- coding: utf-8 -*-

from moviepy.editor import *
import cv2
import os
import subprocess
import numpy as np
import base64
import json

def make_video(images, vid_name):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(vid_name, fourcc, video_fps, (1024, 1024))
    gen = {}
    for img in images:
      video.write(img)
    video.release()
    print('finished '+ vid_name)

def get_video(DIR_PATH,file_name,latent_direction= 'bangs'):

  image_folder = '{}/interfacegan/results/{}'.format(DIR_PATH,latent_direction)
  video_fps = 12.

  out_path = '{}/video_result/'.format(DIR_PATH)

  images = [img_path for img_path in sorted(os.listdir(image_folder)) if '.jpg' in img_path]
  os.makedirs(out_path, exist_ok=True)

  prev_id = None
  img_sets = []
  for img_path in images:
    img_id = img_path.split('_')[0]
    if img_id == prev_id: #append
      img_sets[-1].append(img_path)
      
    else: #start a new img set
      img_sets.append([])
      img_sets[-1].append(img_path)
    prev_id = img_id

  print("Found %d image sets!\n" %len(img_sets))
  if image_folder[-1] != '/':
    image_folder += '/'

  print("############################")
  print("\nGenerating video %d..." %i)
  set_images = []
  vid_name = out_path + 'out_video_%s_%s.mp4' %(latent_direction,file_name)
  for img_path in img_sets[0]:
    set_images.append(cv2.imread(image_folder + img_path))

  set_images.extend(reversed(set_images))
  make_video(set_images, vid_name)

  return vid_name


def edit_bangs(file_path,DIR_PATH='./',latent_direction='bangs',morph_strength=3,nr_interpolation_steps=48,iterations=2,video=False):
  file_name = file_path.split('/')[-1]
  output=subprocess.getoutput('rm -rf {}/stylegan-encoder/aligned_images {}/stylegan-encoder/raw_images'.format(DIR_PATH,DIR_PATH))
  print(output)
  output=subprocess.getoutput('mkdir {}/stylegan-encoder/aligned_images {}/stylegan-encoder/raw_images'.format(DIR_PATH,DIR_PATH))
  print(output)
  output=subprocess.getoutput('cp {} {}/stylegan-encoder/raw_images'.format(file_path,DIR_PATH))
  print(output)

  #里面有模型路径替换
  output=subprocess.getoutput('python {}/stylegan-encoder/align_images.py {}/stylegan-encoder/raw_images/ {}/stylegan-encoder/aligned_images/ --output_size=1024'.format(DIR_PATH,DIR_PATH,DIR_PATH))
  print(output)

  #里面有模型路径替换,124行，40行,56行
  output=subprocess.getoutput('rm -rf {}/stylegan-encoder/generated_images {}/stylegan-encoder/latent_representations'.format(DIR_PATH,DIR_PATH))
  print(output)
  print("aligned_images contains %d images ready for encoding!" %len(os.listdir('{}/stylegan-encoder/aligned_images/'.format(DIR_PATH))))
  output=subprocess.getoutput('python {}/stylegan-encoder/encode_images.py --optimizer=lbfgs --face_mask=False --iterations={} --use_lpips_loss=0 --use_discriminator_loss=0 --output_video=True {}/stylegan-encoder/aligned_images/ {}/stylegan-encoder/generated_images/ {}/stylegan-encoder/latent_representations/'.format(DIR_PATH,iterations,DIR_PATH,DIR_PATH,DIR_PATH))
  print(output)

  latents = sorted(os.listdir('{}/stylegan-encoder/latent_representations'.format(DIR_PATH)))
  out_file = '{}/output_vectors.npy'.format(DIR_PATH)

  final_w_vectors = []
  w = np.load('{}/stylegan-encoder/latent_representations/'.format(DIR_PATH) + latents[0])
  final_w_vectors.append(w)
  final_w_vectors = np.array(final_w_vectors)
  np.save(out_file, final_w_vectors)
  print("1 latent vectors of shape %s saved to %s!" %(str(w.shape), out_file))

  # 里面有模型路径替换,
  output=subprocess.getoutput('rm -r {}/interfacegan/results/bangs'.format(DIR_PATH))
  print(output)
  output=subprocess.getoutput('python {}/interfacegan/edit.py -m stylegan_ffhq -b {}/interfacegan/boundaries/stylegan_ffhq_bangs/boundary_bangs_without_gender_smile.npy -s Wp -i \'{}/output_vectors.npy\' -o {}/interfacegan/results/bangs --start_distance -3.0 --end_distance 3.0 --steps=48'.format(DIR_PATH,DIR_PATH,DIR_PATH,DIR_PATH))
  print(output)

  output=subprocess.getoutput('rm -rf {}/frames_result/{}'.format(DIR_PATH,file_name))
  print(output)
  output=subprocess.getoutput('cp -r {}/interfacegan/results/bangs {}/frames_result/{}'.format(DIR_PATH,DIR_PATH,file_name))
  print(output)
  frame_path = sorted(os.listdir('{}/frames_result/{}'.format(DIR_PATH,file_name)))
  frame_path = ['{}/frames_result/{}/'.format(DIR_PATH,file_name)+i for i in frame_path if 'jpg' in i]
  
  video_path = None
  if video:
    video_path = get_video(DIR_PATH,file_name)

  return frame_path,video_path


def get_base64(frame_path):
  result_json = []
  for i,e in enumerate(frame_path):
    with open(e,"rb") as f:
      base64_data = base64.b64encode(f.read())
      result_json.append('data:image/jpg;base64,'+str(base64_data,'utf-8'))
    f.close()
  return json.dumps(result_json)

# frame_path,video_path = edit_bangs(file_path)


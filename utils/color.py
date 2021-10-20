import os

def choose_color(color):
  color_path = '/content/Virtual_Salon/data/dyeing_pool/' + color + '.png'
  dyeing_path = '/content/Virtual_Salon/data/dyeing/'
  os.system('rm -rf ' + dyeing_path + '*')
  os.system('cp ' + color_path + ' ' + dyeing_path)

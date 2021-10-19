import os

def clear_tmp_file():
  os.system('''rm -r /content/Virtual_Salon/results/results
rm -r /content/Virtual_Salon/data/src/src/.ipynb_checkpoints
rm -r /content/Virtual_Salon/data/src/.ipynb_checkpoints
rm -r ./results/img/.ipynb_checkpoints
rm -r ./data/ref/.ipynb_checkpoints
rm -r /content/Virtual_Salon/results/results
rm -rf /content/Virtual_Salon/results/img
rm -rf /content/Virtual_Salon/results/label/others
rm -rf /content/Virtual_Salon/results/label/src
rm -r /content/Virtual_Salon/data/dyeing/.ipynb_checkpoints''')
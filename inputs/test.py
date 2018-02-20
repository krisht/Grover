import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
files = [os.path.join('./', f) for f in os.listdir('./') if f.endswith('.jpeg') or f.endswith('.jpg')]
print(files)

for file in files:
	img = cv2.imread(file)
	a = np.sum(img[:,:,2])
	print(file, a/(img.shape[0] * img.shape[1]))

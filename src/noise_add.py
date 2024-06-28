import os
import cv2
import numpy as np
from tqdm import tqdm

root_dir = '/images'

def add_gaussian_noise(img, mean=0, var=0.01):
    noise = np.random.normal(mean, var**0.5, img.shape).astype(np.uint8)
    noisy_img = cv2.add(img, noise)
    return noisy_img

for root, dirs, files in os.walk(root_dir):
    for file in tqdm(files):
        if file.endswith('.png') or file.endswith('.jpg'):
            img_path = os.path.join(root, file)
            img = cv2.imread(img_path)
            
            noisy_img = add_gaussian_noise(img, var=6.0)
            
            cv2.imwrite(img_path, noisy_img)
            
            print(f"Added noise to: {img_path}")
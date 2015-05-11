import os
import PIL
import PIL.Image
fg_dir = '/home/junyic/Work/Courses/4th_year/DataSci/final/train_seismic/'

files = os.listdir(fg_dir)
num_width = 10
num_height = 10

img_size = 34
composite = np.zeros((num_width*img_size, num_height*img_size))

for i in range(num_width):
    for j in range(num_height):
        filename = files[(i-1)*num_width + j]
        small_img = PIL.Image.open(fg_dir + filename)
        small_img = small_img.resize((img_size, img_size))
        if small_img.mode != 'F':
            small_img = small_img.convert('F')
        composite[i*img_size:(i+1)*img_size, j*img_size:(j+1)*img_size] = np.array(small_img)
##
composite_img = PIL.Image.fromarray(composite)
if composite_img != 'RGB':
    composite_img = composite_img.convert('RGB')
composite_img.save('/home/junyic/Sandbox/train_samples_paired.png')
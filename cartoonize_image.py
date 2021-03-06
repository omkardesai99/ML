import os
os.chdir(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code')

import warnings
warnings.filterwarnings('ignore')

import os
import cv2
import numpy as np
import tensorflow as tf
import network
import guided_filter #for using this use :- pip install git+https://github.com/tflearn/tflearn.git
from tqdm import tqdm

from IPython.display import Image
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\test_images\image1.jpg')
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\test_images\image2.jpg')
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\test_images\image3.jpg')


def resize_crop(image):
    h, w, c = np.shape(image)
    print(h)
    print(w)
    print(c)
    if min(h, w) > 720:
        if h > w:
            h, w = int(720*h/w), 720
        else:
            h, w = 720, int(720*w/h)
    image = cv2.resize(image, (w, h),interpolation=cv2.INTER_AREA)
    h, w = (h//8)*8, (w//8)*8
    image = image[:h, :w, :]
    return image
    

def cartoonize(load_folder, save_folder, model_path):
    input_photo = tf.placeholder(tf.float32, [1, None, None, 3])
    network_out = network.unet_generator(input_photo)
    final_out = guided_filter.guided_filter(input_photo, network_out, r=1, eps=5e-3)

    all_vars = tf.trainable_variables()
    gene_vars = [var for var in all_vars if 'generator' in var.name]
    saver = tf.train.Saver(var_list=gene_vars)
    
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)

    sess.run(tf.global_variables_initializer())
    saver.restore(sess, tf.train.latest_checkpoint(model_path))
    name_list = os.listdir(load_folder)
    for name in tqdm(name_list):
        try:
            load_path = os.path.join(load_folder, name)
            save_path = os.path.join(save_folder, name)
            image = cv2.imread(load_path)
            image = cv2.resize_crop(image)
            batch_image = image.astype(np.float32)/127.5 - 1#The purpose of doing so is to normalize and scale the pixel data.
            #The activation function of the output layer of the generator is tanh, which returns a value between -1 and 1. To scale that to 0 and 255 (which are the values you expect for an image), we have to multiply it by 127.5 (so that -1 becomes -127.5, and 1 becomes 127.5), and then add 127.5 (so that -127.5 becomes 0, and 127.5 becomes 255). We then have to do the inverse of this when feeding an image into the discriminator (which will expect a value between -1 and 1).
            batch_image = np.expand_dims(batch_image, axis=0)
            #The expand_dims() function is used to expand the shape of an array. Insert a new axis that will appear at the axis position in the expanded array shape.
            output = sess.run(final_out, feed_dict={input_photo: batch_image})
            output = (np.squeeze(output)+1)*127.5
            output = np.clip(output, 0, 255).astype(np.uint8)
            cv2.imwrite(save_path, output)
        except:
            print('cartoonize {} failed'.format(load_path))


    
tf.reset_default_graph()
if __name__ == '__main__':
    model_path = 'saved_models'
    load_folder = 'test_images'
    save_folder = 'cartoonized_images'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    cartoonize(load_folder, save_folder, model_path)
    
#image1 difference
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\test_images\image4.jpg')
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\cartoonized_images\image4.jpg')

#image2 difference
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\test_images\image5.jpg')
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\cartoonized_images\image5.jpg')

#image3 difference

Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\test_images\image6.jpg')
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\cartoonized_images\image6.jpg')

#image4 difference
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\test_images\image7.jpg')
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\cartoonized_images\image7.jpg')

#image5 difference
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\test_images\image8.jpg')
Image(r'C:\Users\omkar desai\Desktop\machine learning\Machine_learnng_project\White-box-Cartoonization-master\White-box-Cartoonization-master\test_code\cartoonized_images\image8.jpg')























from flask import Flask,render_template, request, jsonify
from PIL import Image
import numpy as np
import os

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization, Activation, Add, Concatenate
from tensorflow.keras.optimizers import Adam
from vit_keras import vit


app = Flask(__name__)


# Define the upload directory
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define transitional block function
def transitional_block(x, filters):
    x = Conv2D(filters, kernel_size=(3, 3), strides=(1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)
    return x

# Define pointwise convolution block function
def pointwise_conv_block(x, filters):
    x = Conv2D(filters, kernel_size=(1, 1), strides=(1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    return x

# Define the ViT model
input_shape = (224, 224, 3)  # Example input shape
num_classes = 6  # Example number of classes
vit_model = vit.vit_b32(
    image_size=input_shape[:2],
    include_top=False,
    pretrained=True,
    pretrained_top=False,
    classes=num_classes,
    weights="imagenet21k",
)

# Freeze the layers of the ViT model
for layer in vit_model.layers:
    layer.trainable = False

# Define the modified VGG19 model
def modified_vgg19(input_tensor):
    # Block 1
    x = Conv2D(64, kernel_size=(3, 3), strides=(1, 1), padding='same')(input_tensor)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = transitional_block(x, 64)

    # Block 2
    x = transitional_block(x, 128)
    x = pointwise_conv_block(x, 128)

    # Block 3
    x = transitional_block(x, 256)
    x = pointwise_conv_block(x, 256)
    x = pointwise_conv_block(x, 256)
    x = pointwise_conv_block(x, 256)

    # Block 4
    x = transitional_block(x, 512)
    x = pointwise_conv_block(x, 512)
    x = pointwise_conv_block(x, 512)
    x = pointwise_conv_block(x, 512)
    x = pointwise_conv_block(x, 512)

    # Block 5
    x = transitional_block(x, 512)
    x = pointwise_conv_block(x, 512)
    x = pointwise_conv_block(x, 512)
    x = pointwise_conv_block(x, 512)
    x = pointwise_conv_block(x, 512)

    x = transitional_block(x, 1024)
    x = pointwise_conv_block(x, 1024)
    x = pointwise_conv_block(x, 1024)
    x = pointwise_conv_block(x, 1024)
    x = pointwise_conv_block(x, 1024)

    x = Flatten()(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    output_layer = Dense(6, activation='softmax')(x)

    return output_layer
    # Your modified VGG19 architecture here

# Register custom layers used in modified_vgg19
tf.keras.utils.get_custom_objects()['transitional_block'] = transitional_block
tf.keras.utils.get_custom_objects()['pointwise_conv_block'] = pointwise_conv_block

# Load the pre-trained model
path = "my_model.h5"

loaded_model = load_model(path, custom_objects={
    'transitional_block': transitional_block,
    'pointwise_conv_block': pointwise_conv_block,
})

# Function to preprocess the image
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# Function to check if the file has an allowed extension
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
     # Check if the 'file' key is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    # Check if file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Check if file is allowed
    if file and allowed_file(file.filename):
         # Create the upload directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(img_path)

        # Preprocess the image
        img_array = preprocess_image(img_path)
        
        #labels
        class_labels = ['e.coli', 'healthy', 'klebsila', 'pseudomonas', 'staphylococcus', 'streptococcus']

        
        
        
        # Make predictions
        predictions = loaded_model.predict(img_array)
        
        # Set confidence threshold
        confidence_threshold = 0.80  # Adjust as needed  #.55 for normal #.85 for microscope

        #  Get the predicted class label and confidence
        max_confidence = np.max(predictions)
        
        
        if max_confidence >= confidence_threshold:
            predicted_class_index = np.argmax(predictions)
            predicted_class_label = class_labels[predicted_class_index]
            return jsonify({'prediction': predicted_class_label})

        else:
            return jsonify({'prediction': "Unknown, if its an edible please wash it thoroughly before consuming."})
        
    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)

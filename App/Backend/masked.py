import numpy as np
import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Load the image file
def maked_img(image_filename, t_size):
    # Load image
    image = mp.Image.create_from_file(image_filename)

    # Create the options that will be used for ImageSegmenter
    base_options = python.BaseOptions(model_asset_path='./deeplab_v3.tflite')
    options = vision.ImageSegmenterOptions(base_options=base_options, output_category_mask=True)

    # Create the image segmenter
    with vision.ImageSegmenter.create_from_options(options) as segmenter:
        # Retrieve the category masks for the image
        segmentation_result = segmenter.segment(image)
        category_mask = segmentation_result.category_mask

        # Convert category_mask to a binary mask
        mask = (category_mask.numpy_view() > 0.2).astype(np.uint8) * 255

        # Erode the mask to make the masked area smaller
        kernel = np.ones((5, 5), np.uint8)
        eroded_mask = cv2.erode(mask, kernel, iterations = t_size)

        # Apply the inverse of the eroded mask to the image
        masked_image = cv2.bitwise_and(image.numpy_view(), image.numpy_view(), mask=~eroded_mask)

    return masked_image
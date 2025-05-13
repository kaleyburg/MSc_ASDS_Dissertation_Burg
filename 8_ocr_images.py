
#%% showing a leaflet as an example


#print(sys.executable)

#INSTALLATION OF KERAS OCR

#pip install -q keras-ocr


#uncomment below for setup
#pip install git+https://github.com/faustomorales/keras-ocr.git#egg=keras-ocr

#pip install "numpy<2.0"

#uncomment below for tensorflow setup
#pip install "tensorflow==2.15.1"

#pip install --force-reinstall -v "tensorflow==2.15.1"


import keras_ocr
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np


#CREATE PIPELINE

pipeline = keras_ocr.pipeline.Pipeline()

#READING IMAGES ONE AT A TIME

# Set the working directory
new_directory = "C:/Users/kburg/OneDrive/Documents/GitHub/MSc_ASDS_Dissertation_Burg"     
os.chdir(new_directory)
print("Current working directory:", os.getcwd())


image_filenames = ['/tex_files_withallimagesandbib/28_1.jpg', '/tex_files_withallimagesandbib/28_2.jpg']


# Construct paths to images with the working directory prepended
image_paths = [os.path.join(new_directory, img_path.lstrip('/')) for img_path in image_filenames]

# Print paths to confirm
for path in image_paths:
    print("Image path:", path)

# Read images from the constructed paths
images = [keras_ocr.tools.read(img_path) for img_path in image_paths]

# Optional: Print out the images to confirm they are loaded
print("Number of images loaded:", len(images))
# Read images from folder path to image object
images = [keras_ocr.tools.read(img_path) for img_path in image_paths]



# generate text predictions from the images
prediction_groups = pipeline.recognize(images)


# Initialize the OCR pipeline
pipeline = keras_ocr.pipeline.Pipeline()

# Process the images to get predictions
prediction_groups = pipeline.recognize(images)



#drawing things for showing


def draw_annotations_custom(image, predictions, ax=None, skip_ratio=4):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    # Convert image to grayscale and back to 3 channels
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    # Skip most predictions to reduce clutter
    predictions = predictions[::skip_ratio]

    # Set up the plot axis
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 12))

    # Draw thin bounding boxes
    for word, box in predictions:
        box = np.array(box).astype(int)
        poly = Polygon(box, closed=True, edgecolor='black', fill=False, linewidth=1)
        ax.add_patch(poly)

    ax.imshow(image)
    ax.set_xticks([])
    ax.set_yticks([])

    # Sort and separate predictions into left and right groups
    left, right = [], []
    for word, box in sorted(predictions, key=lambda p: p[1][:, 1].min()):
        (left if box[:, 0].mean() < image.shape[1] / 2 else right).append((word, box))

    def annotate_side(group, side):
        used_y_positions = set()
        for i, (text, box) in enumerate(group):
            # Determine box edge
            if side == "left":
                box_point = box[np.argmin(box[:, 0])]
                text_x = -0.1
                h_align = 'right'
            else:
                box_point = box[np.argmax(box[:, 0])]
                text_x = 1.1
                h_align = 'left'

            # Normalize box point
            xy = box_point / np.array([image.shape[1], image.shape[0]])
            xy[1] = 1 - xy[1]

            # Dynamically adjust label Y to avoid collision
            y_base = 1 - (i / len(group))
            offset = 0.03
            attempts = 0
            while round(y_base, 2) in used_y_positions and attempts < 10:
                y_base += offset
                attempts += 1
            used_y_positions.add(round(y_base, 2))

            # Annotate with a medium gray line and small text
            ax.annotate(
                text=text,
                xy=xy,
                xytext=(text_x, y_base),
                xycoords="axes fraction",
                textcoords="axes fraction",
                arrowprops={"arrowstyle": "-", "color": "#555555", "linewidth": 1.5},
                color="black",
                fontsize=10,
                horizontalalignment=h_align,
                verticalalignment='center'
            )

    annotate_side(left, "left")
    annotate_side(right, "right")
    return ax

# Create a single figure to hold all images
fig, axes = plt.subplots(len(images), 1, figsize=(12, 12 * len(images)))

# Ensure axes is iterable even if there's only one image
if len(images) == 1:
    axes = [axes]

# Iterate through images and predictions
for idx, (image, predictions) in enumerate(zip(images, prediction_groups)):
    # Draw annotations on the individual subplot
    draw_annotations_custom(image, predictions, ax=axes[idx])
    axes[idx].set_title(f"Image {idx + 1}")

    # Save each individual figure
    individual_save_path = os.path.join(new_directory, 'tex_files_withallimagesandbib', 'plots', f'ukip_example_{idx + 1}.png')
    individual_save_path = individual_save_path.replace('/', os.sep).replace('\\', os.sep)
    plt.figure()
    draw_annotations_custom(image, predictions)
    plt.savefig(individual_save_path, bbox_inches='tight', pad_inches=0.1)
    plt.close()

    # Check if the file was saved successfully
    if os.path.exists(individual_save_path):
        print(f"Individual figure saved successfully at: {individual_save_path}")
    else:
        print(f"Failed to save the individual figure at: {individual_save_path}")

# Save the combined figure
combined_save_path = os.path.join(new_directory, 'tex_files_withallimagesandbib', 'plots', 'ukip_combined_example.png')
combined_save_path = combined_save_path.replace('/', os.sep).replace('\\', os.sep)
plt.savefig(combined_save_path, bbox_inches='tight', pad_inches=0.1)
plt.tight_layout()

# Check if the combined file was saved successfully
if os.path.exists(combined_save_path):
    print(f"Combined figure saved successfully at: {combined_save_path}")
else:
    print(f"Failed to save the combined figure at: {combined_save_path}")

plt.show()

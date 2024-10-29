import os
import shutil
import pandas as pd

# Paths to input CSV, original dataset, and new test directory
CSV_PATH = "./verification_pairs.csv"
DATASET_PATH = "/fssd2/user-data/gsarridis/wacv-challenge/dcface_wacv/organized_cropped"
TEST_DIR = "./test_images"

# Load CSV
pairs_df = pd.read_csv(CSV_PATH)

# Set to store unique image paths
unique_images = set()

# Collect all unique image paths from both img1 and img2 columns
unique_images.update(pairs_df["img1"].tolist())
unique_images.update(pairs_df["img2"].tolist())

# Copy each unique image to the new test directory, maintaining subdirectory structure
for img_rel_path in unique_images:
    # Full path to the source image in the original dataset
    src_path = os.path.join(DATASET_PATH, img_rel_path)
    # Full path to the destination image in the test directory
    dest_path = os.path.join(TEST_DIR, img_rel_path)

    # Create any missing directories in the destination path
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Copy the image to the new test directory
    shutil.copy2(src_path, dest_path)

print(
    f"Test images successfully copied to {TEST_DIR} with original subdirectory structure."
)

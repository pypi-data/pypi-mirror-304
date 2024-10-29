import os
import random
import pandas as pd
from glob import glob

# Define the dataset path and output CSV file
DATASET_PATH = "/fssd2/user-data/gsarridis/wacv-challenge/dcface_wacv/organized_cropped"
OUTPUT_CSV = "./verification_pairs.csv"

# Define mappings for race and gender labels
race_mapping = {
    "White": 0,
    "Asian": 1,
    "Indian": 2,
    "Black": 3,
}  # Replace with actual race labels and corresponding numbers
gender_mapping = {
    "Male": 1,
    "Female": 0,
}  # Replace with actual gender labels and corresponding numbers

# Initialize list to collect pairs data
pairs_data = []

# Iterate over each race and gender combination in the dataset
for race_dir in os.listdir(DATASET_PATH):
    race_path = os.path.join(DATASET_PATH, race_dir)
    if "Other" in race_dir:
        continue
    if not os.path.isdir(race_path):
        continue
    race_num = race_mapping.get(race_dir, -1)  # Map race to numeric

    for gender_dir in os.listdir(race_path):
        gender_path = os.path.join(race_path, gender_dir)
        if not os.path.isdir(gender_path):
            continue
        gender_num = gender_mapping.get(gender_dir, -1)  # Map gender to numeric

        # Get all IDs for the current race-gender combination
        ids = [
            d
            for d in os.listdir(gender_path)
            if os.path.isdir(os.path.join(gender_path, d))
        ]

        # Create positive pairs (same ID)
        positive_pairs = []
        for person_id in ids:
            person_images = glob(os.path.join(gender_path, person_id, "*"))
            if len(person_images) < 2:
                continue  # Skip IDs with less than 2 images

            # Randomly select two images to form a positive pair
            pos_pair = random.sample(person_images, 2)
            # Save paths relative to the root data directory
            relative_pos_pair = [
                os.path.relpath(pos_pair[0], DATASET_PATH),
                os.path.relpath(pos_pair[1], DATASET_PATH),
                1,
                race_num,
                gender_num,
            ]
            positive_pairs.append(relative_pos_pair)

        # Create negative pairs (different IDs)
        negative_pairs = []
        for _ in range(5):  # Only 5 pairs per race-gender as required
            if len(ids) < 2:
                continue  # Skip if there are less than 2 IDs in this combination
            id1, id2 = random.sample(ids, 2)
            img1 = random.choice(glob(os.path.join(gender_path, id1, "*")))
            img2 = random.choice(glob(os.path.join(gender_path, id2, "*")))
            relative_neg_pair = [
                os.path.relpath(img1, DATASET_PATH),
                os.path.relpath(img2, DATASET_PATH),
                0,
                race_num,
                gender_num,
            ]
            negative_pairs.append(relative_neg_pair)

        # Combine positive and negative pairs and limit to 5 of each
        all_pairs = positive_pairs[:5] + negative_pairs[:5]
        pairs_data.extend(all_pairs)

# Create a DataFrame and save to CSV
pairs_df = pd.DataFrame(
    pairs_data, columns=["img1", "img2", "is_same", "race", "gender"]
)
pairs_df.to_csv(OUTPUT_CSV, index=False)
print(f"CSV with verification pairs saved to {OUTPUT_CSV}")

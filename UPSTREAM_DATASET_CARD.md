---
license: cc-by-4.0
task_categories:
- image-classification
tags:
- computer-vision
- eyeglasses
- sunglasses
- eyewear
- product-images
---

# Eyeglasses vs Sunglasses Dataset

This repository contains a large-scale image classification dataset for classifying eyewear into Eyeglasses and Sunglasses.

- **Total Images**: 21,766
- **Dataset Structure**:
  - `train/`: 17,358 images total (1,474 unique product models):
    - `eyeglasses/`: 13,485 images (1,118 unique product models)
    - `sunglasses/`: 3,873 images (356 unique product models)
  - `validation/`: 4,408 images total (369 unique product models):
    - `eyeglasses/`: 3,427 images (280 unique product models)
    - `sunglasses/`: 981 images (89 unique product models)
- **Format**: Image Classification folder structure where images are grouped by unique product model IDs (`train/eyeglasses/<product_id>/...`).
- **Splitting Strategy**: The dataset is split by unique product model IDs (80% train, 20% validation) to ensure that all images of any given model reside in the same split, preventing data leakage.
- **License**: CC BY 4.0

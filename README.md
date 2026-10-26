# Eyewear Segmentation Dataset — AI Prelabels for Human Review

## Contents
- 1,000 real product photographs: 800 eyeglasses and 200 sunglasses
- 250 product models, four views per model; product groups separated across train/val/test
- 1,000 generated binary PNG masks and 1,000 YOLO polygon text labels (class 0 = eyewear)
- `data.yaml`, source-aware `manifest.csv`, per-image `human_review_queue.csv`, and a mask-overlay montage

## Split
- train: 700 images
- val: 152 images
- test: 148 images

## Source and licence
Source: https://huggingface.co/datasets/shravya11/eyeglasses-dataset
Pinned revision: `7011dd3ac628040a8885a4b597399409643a9e04`
Upstream card licence tag: `cc-by-4.0`. The upstream card indicates CC BY 4.0; retain attribution and check current upstream terms before commercial use.

## CRITICAL ANNOTATION STATUS
The source is an image-classification/product-image dataset, not a human-annotated segmentation dataset. These masks were generated automatically with background-colour estimates, GrabCut and contour post-processing. **None are claimed human-verified.** Every image requires review by a human annotator before it is used as gold-standard training data or for evaluation claims. `human_review_queue.csv` prioritizes masks likely to be problematic, but even a standard-priority mask may be wrong.

Masks represent a filled object envelope to align with one-class YOLO polygon segmentation. Filling an envelope can fill transparent lens openings; YOLO polygon text format does not naturally represent holes inside a single polygon instance. If you need material-level segmentation (frame pixels only), use CVAT/Label Studio with a raster-mask or format that supports holes, then convert carefully.

## Recommended human review
1. Open `review_montage.jpg` and then the original image/mask pairs for every flagged row.
2. Import images plus the generated labels into CVAT or Label Studio and correct outlines at full resolution. Prioritize wire frames, clear lenses, pale frames, shadows, reflections and gaps in temples.
3. Keep the test split out of training and only evaluate against human-verified labels.
4. Record reviewer, review date, and accepted/corrected/rejected status for each image.

`GPT-6 Astra` was not invoked as a separate model endpoint in this session. This package is an AI-generated prelabel set, not an Astra-certified or human-certified set.

## Human review tool
Open `HUMAN_REVIEW_TOOL.html` in a desktop browser after extracting the ZIP, choose the extracted dataset root folder, visually inspect the green mask overlay, and record Approve / Corrected / Reject decisions using a reviewer ID. Corrected masks can be saved as PNGs. Use `apply_reviewed_masks.py` to apply the audit and masks after review, backing up the original masks before changes. This process requires an actual human to inspect each image; the included archive remains AI-prelabelled until that happens.

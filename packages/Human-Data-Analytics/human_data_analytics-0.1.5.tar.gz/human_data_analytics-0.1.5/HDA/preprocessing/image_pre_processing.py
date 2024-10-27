import os
from typing import List, Any
import pickle as pkl
import numpy as np
from tqdm import tqdm
import multiprocessing

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from image_utils import crop_image, resize_image, CLAHE, create_patches

def pre_process(image_n : str, path : str) -> np.ndarray:
    '''function that preprocesses an image given its filename'''

    image_path = os.path.join(path, image_n)
    cropped_image = crop_image(image_path)
    resized_image = resize_image(cropped_image)
    modified_image = CLAHE(resized_image)
    patches = create_patches(modified_image)

    return patches


def parallel(split:str="train"):
    '''function that preprocesses each image in the dataset and groups them by their original index in a parallel way, then
    save the result in a pickle file'''

    path = os.path.join(os.environ.get("DATA_PATH"), split, "images")
    
    #sorting the image filenames by their index
    images_filenames = sorted(os.listdir(path), key = lambda x: int(x.split('.')[0]))

    #parallel processing of images with a bar for progresses
    with tqdm(total=len(images_filenames), desc=f"Preprocessing {split} images") as pbar:
        
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = []
            for image_n in images_filenames:
                result = pool.apply_async(pre_process, args=(image_n, path), 
                                          callback=lambda _: pbar.update(1))
                results.append(result)

            # Wait for all results to finish
            for result in results:
                result.wait()  # Block until the result is ready

    # Collect results
    results = [result.get() for result in results]

    preprocessed_path = os.path.join(os.environ.get("DATA_PATH"), split, "preprocessed_images.npz")
    np.savez_compressed(preprocessed_path, *results)

if __name__ == "__main__":
    for split in ["train", "val", "test"]:
        parallel(split=split)

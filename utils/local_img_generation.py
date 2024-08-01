import os
import base64
import logging
import requests

from typing import Tuple
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

try:
    IMG_GEN_ENDPOINT_URL=os.getenv("IMG_GEN_ENDPOINT_URL")
except ValueError as e:
    logging.info(str(e))

def generate_img(
        img_model: str,
        prompt: str,
        negative_prompt: str,
        **kwargs
    ) -> Tuple[bytes, str]:
    
    """
    Takes image Stable Diffusion parameters and makes API call to sd-auto Docker endpoint.

    Returns a tuple of image bytes and generation info.
    """

    # Check for Lora
    use_detailed_hands_lora = kwargs.get('use_detailed_hands_lora', False)
    use_white_bg_lora = kwargs.get('use_white_bg_lora', False)
    use_sdxl_lightning_4step_lora = kwargs.get('use_4step_lora', False)
    use_sdxl_lightning_8step_lora = kwargs.get('use_8step_lora', False)

    if use_detailed_hands_lora:
        prompt += " <lora:detailed_hands:1>" # you can change 1, it needs to be between 0-1
        logging.info("Using 'Detailed Hands Lora'")
    if use_white_bg_lora:
        prompt += " <lora:white_1_0:1>" # you can change 1, it needs to be between 0-1
        logging.info("Using 'White Background Lora'")
    if use_sdxl_lightning_4step_lora:
        prompt += " <lora:sdxl_lightning_4step_lora:1>"
        logging.info("Using 'SDXL-Lightning 4Step Lora'")
    if use_sdxl_lightning_8step_lora:
        prompt += " <lora:sdxl_lightning_8step_lora:1>"
        logging.info("Using 'SDXL-Lightning 8Step Lora'")

    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": kwargs.get('seed', 1337),
        "sampler_name": kwargs.get('sampling_method', 'DPM++ SDE'),
        "scheduler": kwargs.get('schedule_type', 'Karras'),
        "batch_size": kwargs.get('batch_size', 1),
        "n_iter": kwargs.get('batch_count', 1), # ToDo: This may not be related to batch count
        "steps": kwargs.get('sampling_steps', 6),
        "cfg_scale": kwargs.get('cfg_scale', 1.5),
        "width": kwargs.get('width', 832),
        "height": kwargs.get('height', 1216),
        "override_settings": {
            "sd_model_checkpoint": img_model
        },
    }
    logging.info("\n"+"-"*40+f"\nPayload: {payload}\n"+"-"*40)

    response = requests.post(url=f'{IMG_GEN_ENDPOINT_URL}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    response.raise_for_status()

    image = r['images'][0]
    info:str = r['info'] # string of dictionary containing parameters and generation info
    
    image_bytes = base64.b64decode(image)

    return image_bytes, info
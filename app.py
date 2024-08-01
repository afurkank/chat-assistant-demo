import base64
import logging
import requests

from time import time
from flask import Flask, render_template, request, jsonify

from utils.prompt_constructor import get_prompt_for_image_gen
from utils.local_img_generation import generate_img
from utils.remove_bg import get_bg_removed_img
from utils.jotform_api import get_title, get_logo_url

app = Flask(__name__)

IMG_MODEL = "Juggernaut_RunDiffusionPhoto2_Lightning_4Steps"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_form', methods=['POST'])
def update_form():
    gender = request.json['gender']
    form_id = request.json['formID']

    start = time()
    avatar_img_generation_prompt = get_prompt_for_image_gen(prompt_file_path=f"prompts/{gender}_avatar_img_prompt_wo_color.txt", 
                                      form_id=form_id,
                                      model='gpt-3.5-turbo')
    end0 = time()
    logging.info("\n"+"#"*40+f"\nPrompt for avatar took {(end0 - start):.2f} seconds\n"+"#"*40)
    
    background_img_generation_prompt = get_prompt_for_image_gen(prompt_file_path="prompts/background_img_prompt.txt", 
                                      form_id=form_id,
                                      model='gpt-3.5-turbo')
    end1 = time()
    logging.info("\n"+"#"*40+f"\nPrompt for background took {(end1 - end0):.2f} seconds\n"+"#"*40)

    avatar_image_bytes, _ = generate_img(img_model=IMG_MODEL,
                 prompt=avatar_img_generation_prompt,
                 negative_prompt='')
    end2 = time()
    logging.info("\n"+"#"*40+f"\nAvatar image generation took {(end2 - end1):.2f} seconds\n"+"#"*40)
    
    bg_removed_avatar_img_bytes = get_bg_removed_img(avatar_image_bytes)
    end3 = time()
    logging.info("\n"+"#"*40+f"\nBackground removal took {(end3 - end2):.2f} seconds\n"+"#"*40)
    # 1344 * 768 = 1.032.192
    # 1728 * 576 =   995.328
    kwargs = {'width': 1728, 'height': 576}
    
    background_image_bytes, _ = generate_img(img_model=IMG_MODEL,
                 prompt=background_img_generation_prompt,
                 negative_prompt='', **kwargs)
    end4 = time()
    logging.info("\n"+"#"*40+f"\nBackground image generation took {(end4 - end3):.2f} seconds\n"+"#"*40)
    
    # Encode
    avatar_base64 = base64.b64encode(bg_removed_avatar_img_bytes).decode('utf-8')
    background_base64 = base64.b64encode(background_image_bytes).decode('utf-8')
    
    # Get title and logo URL
    title = get_title(form_id)
    logo_url = get_logo_url(form_id)

    # Fetch logo image and convert to base64
    logo_response = requests.get(logo_url)
    logo_base64 = base64.b64encode(logo_response.content).decode('utf-8')

    logging.info("\n"+"#"*40+f"\nTotal time: {(time() - start):.2f} seconds\n"+"#"*40)

    return jsonify({
        'message': f'Form {form_id} updated successfully',
        'avatar': avatar_base64,
        'background': background_base64,
        'title': title,
        'logo': logo_base64
    })

@app.route('/update_avatar', methods=['POST'])
def update_avatar():
    gender = request.json['gender']
    form_id = request.json['formID']
    # personality = request.json['personality']
    
    start = time()
    avatar_img_generation_prompt = get_prompt_for_image_gen(
        prompt_file_path=f"prompts/{gender}_avatar_img_prompt_wo_color.txt", 
        form_id=form_id,
        model='gpt-3.5-turbo')
    end0 = time()
    logging.info("\n"+"#"*40+f"\nPrompt for avatar took {(end0 - start):.2f} seconds\n"+"#"*40)

    avatar_image_bytes, _ = generate_img(img_model=IMG_MODEL,
                 prompt=avatar_img_generation_prompt,
                 negative_prompt='')
    end1 = time()
    logging.info("\n"+"#"*40+f"\nAvatar image generation took {(end1 - end0):.2f} seconds\n"+"#"*40)
    
    bg_removed_avatar_img_bytes = get_bg_removed_img(avatar_image_bytes)
    end2 = time()
    logging.info("\n"+"#"*40+f"\nBackground removal took {(end2 - end1):.2f} seconds\n"+"#"*40)

    avatar_base64 = base64.b64encode(bg_removed_avatar_img_bytes).decode('utf-8')

    logging.info("\n"+"#"*40+f"\nTotal time: {(time() - start):.2f} seconds\n"+"#"*40)

    return jsonify({
        'message': f'Avatar updated to {gender}.',
        'avatar': avatar_base64
    })

@app.route('/change_background', methods=['POST'])
def change_background():
    form_id = request.json['formID']

    start = time()
    background_img_generation_prompt = get_prompt_for_image_gen(
        prompt_file_path="prompts/background_img_prompt.txt", 
        form_id=form_id,
        model='gpt-3.5-turbo')
    end0 = time()
    logging.info("\n"+"#"*40+f"\nPrompt for background took {(end0 - start):.2f} seconds\n"+"#"*40)
    
    kwargs = {'width': 1728, 'height': 576}

    background_image_bytes, _ = generate_img(img_model=IMG_MODEL,
                 prompt=background_img_generation_prompt,
                 negative_prompt='', **kwargs)
    end1 = time()
    logging.info("\n"+"#"*40+f"\nBackground image generation took {(end1 - end0):.2f} seconds\n"+"#"*40)

    background_base64 = base64.b64encode(background_image_bytes).decode('utf-8')
    end2 = time()
    logging.info("\n"+"#"*40+f"\nEncoding avatar image bytes took {(end2 - end1):.2f} seconds\n"+"#"*40)

    logging.info("\n"+"#"*40+f"\nTotal time: {(end2 - start):.2f} seconds\n"+"#"*40)

    return jsonify({
        'message': 'Background changed successfully',
        'background': background_base64
    })

if __name__ == '__main__':
    app.run(debug=True, port=8888)
from flask import Flask, render_template, request, jsonify
import os
import base64
import requests

from utils.prompt_constructor import get_prompt_for_image_gen
from utils.local_img_generation import generate_img
from utils.remove_bg import get_bg_removed_img
from utils.jotform_api import get_title, get_logo_url

app = Flask(__name__)

IMG_MODEL = "sd_xl_turbo_1.0_fp16"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_form', methods=['POST'])
def update_form():
    gender = request.json['gender']
    form_id = request.json['formID']

    avatar_img_generation_prompt = get_prompt_for_image_gen(prompt_file_path=f"prompts/{gender}_avatar_img_prompt_wo_color.txt", 
                                      form_id=form_id,
                                      model='gpt-3.5-turbo')
    
    background_img_generation_prompt = get_prompt_for_image_gen(prompt_file_path="prompts/background_img_prompt.txt", 
                                      form_id=form_id,
                                      model='gpt-3.5-turbo')

    avatar_image_bytes, _ = generate_img(img_model=IMG_MODEL,
                 prompt=avatar_img_generation_prompt,
                 negative_prompt='')
    
    bg_removed_avatar_img_bytes = get_bg_removed_img(avatar_image_bytes)
    
    background_image_bytes, _ = generate_img(img_model=IMG_MODEL,
                 prompt=background_img_generation_prompt,
                 negative_prompt='')
    
    avatar_base64 = base64.b64encode(bg_removed_avatar_img_bytes).decode('utf-8')
    background_base64 = base64.b64encode(background_image_bytes).decode('utf-8')

    # Get title and logo URL
    title = get_title(form_id)
    logo_url = get_logo_url(form_id)

    # Fetch logo image and convert to base64
    logo_response = requests.get(logo_url)
    logo_base64 = base64.b64encode(logo_response.content).decode('utf-8')

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
    
    avatar_img_generation_prompt = get_prompt_for_image_gen(
        prompt_file_path=f"prompts/{gender}_avatar_img_prompt_wo_color.txt", 
        form_id=form_id,
        model='gpt-3.5-turbo')

    avatar_image_bytes, _ = generate_img(img_model=IMG_MODEL,
                 prompt=avatar_img_generation_prompt,
                 negative_prompt='')
    
    bg_removed_avatar_img_bytes = get_bg_removed_img(avatar_image_bytes)

    avatar_base64 = base64.b64encode(bg_removed_avatar_img_bytes).decode('utf-8')

    return jsonify({
        'message': f'Avatar updated to {gender}.',
        'avatar': avatar_base64
    })

@app.route('/change_background', methods=['POST'])
def change_background():
    form_id = request.json['formID']

    background_img_generation_prompt = get_prompt_for_image_gen(
        prompt_file_path="prompts/background_img_prompt.txt", 
        form_id=form_id,
        model='gpt-3.5-turbo')

    background_image_bytes, _ = generate_img(img_model=IMG_MODEL,
                 prompt=background_img_generation_prompt,
                 negative_prompt='')

    background_base64 = base64.b64encode(background_image_bytes).decode('utf-8')

    return jsonify({
        'message': 'Background changed successfully',
        'background': background_base64
    })

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import os
import base64

from utils.prompt_constructor import get_prompt_for_image_gen
from utils.local_img_generation import generate_img
from utils.remove_bg import get_bg_removed_img
from utils.log_image import log_image
from utils.jotform_api import get_title, get_logo_url

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_form', methods=['POST'])
def update_form():
    form_id = request.json['formId']
    
    avatar_img_generation_prompt = get_prompt_for_image_gen(prompt_file_path="prompts/avatar_img_prompt.txt", 
                                      form_id=form_id,
                                      model='gpt-3.5-turbo')
    
    background_img_generation_prompt = get_prompt_for_image_gen(prompt_file_path="prompts/background_img_prompt_wo_color.txt", 
                                      form_id=form_id,
                                      model='gpt-3.5-turbo')

    avatar_image_bytes, _ = generate_img(img_model="Juggernaut_RunDiffusionPhoto2_Lightning_4Steps",
                 prompt=avatar_img_generation_prompt,
                 negative_prompt='')
    
    background_image_bytes, _ = generate_img(img_model="Juggernaut_RunDiffusionPhoto2_Lightning_4Steps",
                 prompt=background_img_generation_prompt,
                 negative_prompt='')
    
    avatar_base64 = base64.b64encode(avatar_image_bytes).decode('utf-8')
    background_base64 = base64.b64encode(background_image_bytes).decode('utf-8')

    return jsonify({
        'message': f'Form {form_id} updated successfully',
        'avatar': avatar_base64,
        'background': background_base64
    })

@app.route('/update_avatar', methods=['POST'])
def update_avatar():
    gender = request.json['gender']
    personality = request.json['personality']
    
    prompt = f"Generate an avatar of a {gender} with a {personality} personality"
    if gender == 'mascot':
        prompt = f"Generate a mascot character with a {personality} personality"

    avatar_image_bytes, _ = generate_img(img_model="Juggernaut_RunDiffusionPhoto2_Lightning_4Steps",
                 prompt=prompt,
                 negative_prompt='')

    avatar_base64 = base64.b64encode(avatar_image_bytes).decode('utf-8')

    return jsonify({
        'message': f'Avatar updated to {gender} with {personality} personality',
        'avatar': avatar_base64
    })

@app.route('/change_background', methods=['POST'])
def change_background():
    prompt = "Generate a random background image"

    background_image_bytes, _ = generate_img(img_model="Juggernaut_RunDiffusionPhoto2_Lightning_4Steps",
                 prompt=prompt,
                 negative_prompt='')

    background_base64 = base64.b64encode(background_image_bytes).decode('utf-8')

    return jsonify({
        'message': 'Background changed successfully',
        'background': background_base64
    })

if __name__ == '__main__':
    app.run(debug=True)
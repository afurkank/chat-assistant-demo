from flask import Flask, render_template, request, jsonify
import os

from utils.prompt_constructor import get_prompt_for_image_gen
from utils.local_img_generation import generate_img
from utils.remove_bg import get_bg_removed_img
from utils.log_image import log_image
from utils.jotform_api import get_title, get_logo_url

app = Flask(__name__)

BACKGROUND_IMAGES = ['background1.jpg', 'background2.jpg', 'background3.jpg']
current_background = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change_background', methods=['POST'])
def change_background():
    global current_background
    current_background = (current_background + 1) % len(BACKGROUND_IMAGES)
    return jsonify({'new_background': BACKGROUND_IMAGES[current_background]})

@app.route('/update_form', methods=['POST'])
def update_form():
    """
    This method is called for generating avatar and background.
    Once the "Fill Form" button is clicked, the background and avatar generation process
    should start.

    After the images are generated, they will replace the old ones.

    The type of avatar (man, woman or mascot) will be used for generating 
    the avatar.
    """
    form_id = request.json['formId']
    # Here you would typically process the form filling request

    avatar_img_generation_prompt = get_prompt_for_image_gen(prompt_file_path="prompts/background_img_prompt_wo_color.txt", 
                                      form_id=form_id,
                                      model='gpt-3.5-turbo')
    
    background_img_generation_prompt = get_prompt_for_image_gen(prompt_file_path="prompts/avatar_img_prompt.txt", 
                                      form_id=form_id,
                                      model='gpt-3.5-turbo')

    avatar_image_bytes = generate_img(img_model="Juggernaut_RunDiffusionPhoto2_Lightning_4Steps",
                 prompt=avatar_img_generation_prompt,
                 negative_prompt='')
    
    background_image_bytes = generate_img(img_model="Juggernaut_RunDiffusionPhoto2_Lightning_4Steps",
                 prompt=avatar_img_generation_prompt,
                 negative_prompt='')
    
    

    return jsonify({'message': f'Form {form_id} updated successfully'})

@app.route('/update_avatar', methods=['POST'])
def update_avatar():
    gender = request.json['gender']
    personality = request.json['personality']
    # Here you would typically update the avatar based on gender and personality

    return jsonify({'message': f'Avatar updated to {gender} with {personality} personality'})

if __name__ == '__main__':
    app.run(debug=True)
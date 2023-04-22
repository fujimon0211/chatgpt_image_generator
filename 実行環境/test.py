import os
import openai
import requests
import streamlit as st
from PIL import Image
import os
import io
import sys
from dotenv import load_dotenv

openai.organization = st.secrets['ChatGPT_organization_key']
openai.api_key = st.secrets['ChatGPT_API_key']

def generate_improved_image(file_name, raw_prompt, size):
    edit_prompt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Please refer to the last generated image and regenerate a better one as described in the prompt."
            },
            {
                "role": "user",
                "content": raw_prompt
            },
        ],
    )
    prompt = edit_prompt["choices"][0]["message"]["content"]
    request = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size,
        response_format='url'
    )
    image_data_url = request['data'][0]['url']
    image_data = requests.get(image_data_url).content
    with open(file_name, "wb") as f:
        f.write(image_data)

# Existing functions
# ...

size_box = ['256x256', '512x512', '1024x1024']

st.title("ChatGPT画像生成ジェネレーター")
st.header('入力した内容に即した画像を生成します')
raw_prompt = st.text_input("生成したい画像を説明する文章を具体的に入力してください", "")
file_name = st.text_input("ファイル名を入れてください", "")
n = st.number_input('生成したい画像の数を入力してください(1~20)', 1, 20)
size = st.selectbox('生成する画像のサイズを選んでください', size_box)

if st.button('画像生成'):
    col = st.columns(n)
    image_generator(file_name, 1, raw_prompt, size)
    images_url_list, image_data, image = generate_other_images(file_name, n, size)
    counter = 0
    for i in range(1, n+1):
        with open(f'image{counter+1}.png', 'wb') as f:
            f.write(image_data[counter])
            st.image(f'image{i}.png', caption=f'サンプル{i}', use_column_width=True)
            counter += 1

    if st.button('改善した画像を生成'):
        improved_file_name = f"improved_{file_name}"
        generate_improved_image(improved_file_name, raw_prompt, size)
        st.image(improved_file_name, caption="改善した画像", use_column_width=True)

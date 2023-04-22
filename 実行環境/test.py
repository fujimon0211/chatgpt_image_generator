import os
import openai
import requests
import streamlit as st
from PIL import Image
import io
import sys
from dotenv import load_dotenv
from streamlit.report_thread import get_report_ctx
from streamlit.hashing import _CodeHasher
from streamlit.state.session_state import SessionState

# Load API key
openai.organization = st.secrets['ChatGPT_organization_key']
openai.api_key = st.secrets['ChatGPT_API_key']


def get_session():
    ctx = get_report_ctx()
    session_id = ctx.session_id
    session_info = SessionState.get(session_id=session_id)

    if not hasattr(session_info, 'improved_image_generated'):
        session_info.improved_image_generated = False

    return session_info


def image_generator(file_name, n, raw_prompt, size):
    edit_prompt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Please translate the input in Japanese into English and output it in an easily understandable form as a prompt for image generation."
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
        n=n,
        size=size,
        response_format='url'
    )
    image_data_url = request['data'][0]['url']
    image_data = requests.get(image_data_url).content
    with open(file_name, "wb") as f:
        f.write(image_data)


def generate_other_images(file_name, n, size):
    various_requests = openai.Image.create_variation(
        image=open(file_name, "rb"),
        n=n,
        size=size
    )
    images = various_requests['data']
    counter = 0
    images_url_list = []
    image_data = []
    for image in images:
        images_url_list.append(image['url'])
        image_data.append(requests.get(images_url_list[counter]).content)
        counter += 1
    return images_url_list, image_data, images


def generate_improved_image(improved_file_name, raw_prompt, size):
    improved_prompt = f"An improved and clearer image of {raw_prompt}"
    image_generator(improved_file_name, 1, improved_prompt, size)


size_box = ['256x256', '512x512', '1024x1024']
st.title("ChatGPT画像生成ジェネレーター")
st.header('入力した内容に即した画像を生成します')
raw_prompt = st.text_input("生成したい画像を説明する文章を具体的に入力してください", "")
file_name = st.text_input("ファイル名を入れてください", "")
n = st.number_input('生成したい画像の数を入力してください(1~20)', 1, 20)
size = st.selectbox('生成する画像のサイズを選んでください', size_box)

session = get_session()

if st.button('画像生成'):
    col = st.columns(n)
    image_generator(file_name, 1, raw_prompt, size)
    images_url_list, image_data, images = generate_other_images(
        file_name, n, size)
    counter = 0
    for i in range(1, n+1):
        with open(f'image{counter+1}.png', 'wb') as f:
            f.write(image_data[counter])
            st.image(f'image{i}.png', caption=f'サンプル{i}',
                     use_column_width=True)
            counter += 1

    session.improved_image_generated = False

if not session.improved_image_generated:
    if st.button('改善された画像を生成'):
        improved_file_name = f"improved_{file_name}"
        generate_improved_image(improved_file_name, raw_prompt, size)
        st.image(improved_file_name, caption='改善された画像', use_column_width=True)
        session.improved_image_generated = True
else:
    st.write("改善された画像が既に生成されました。")

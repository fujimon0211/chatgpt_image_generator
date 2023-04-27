# chatgpt_image_generator
ChatGPT Image Generator
This is a Streamlit application that uses OpenAI's ChatGPT API to generate images based on a user's input description. Users can specify the number of images they want to generate, and the size of the generated images. The application also supports downloading the generated images.

Requirements

・Python 3.6 or higher

・Streamlit

・OpenAI

・Requests

・Pillow

## Installation
1. Clone the repository:

```
git clone https://github.com/your-repo/chatgpt-image-generator.git
```

2. Change directory:

```
cd chatgpt-image-generator
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Run the Streamlit app:

```
streamlit run app.py
```

## Usage
1.Enter a detailed description of the image you want to generate in the provided text area.

2.Specify the number of images you want to generate (1 to 20).

3.Choose the size of the generated images (256x256, 512x512, or 1024x1024).

4.Click the "画像生成" button to generate the images.

5.The generated images will be displayed, and you can download them using the provided download links.

## How it works
The application first translates the user's input description from Japanese to English and uses it as a prompt for image generation. It then calls OpenAI's ChatGPT API to generate images based on the prompt. The images are generated and displayed on the web app, and users can download them using the provided download links.

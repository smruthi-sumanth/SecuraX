import re
import base64
from pathlib import Path
import os

def markdown_images(markdown):
    # example image markdown:
    # ![Test image](images/test.png "Alternate text")
    images = re.findall(r'(!\[(?P<image_title>[^\]]+)\]\((?P<image_path>[^\)"\s]+)\s*([^\)]*)\))', markdown)
    return images


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path, img_alt):
    img_format = img_path.split(".")[-1]
    img_html = f'<img src="data:image/{img_format.lower()};base64,{img_to_bytes(img_path)}" alt="{img_alt}" style="max-width: 100%;">'

    return img_html


def markdown_insert_images(markdown, dir_name=None):
    images = markdown_images(markdown)

    for image in images:
        image_markdown = image[0]
        image_alt = image[1]
        image_path = image[2]
        if dir_name:
            image_path = os.path.join(dir_name, image_path)
        markdown = markdown.replace(image_markdown, img_to_html(image_path, image_alt))
    return markdown

if __name__ == "__main__":
    markdown = """
    # Title
    This is a test markdown with an image ![Test image](images/test1.jpeg)
    This is another test markdown with an image ![Test image](images/test2.jpeg)
    """
    print(markdown_insert_images(markdown))
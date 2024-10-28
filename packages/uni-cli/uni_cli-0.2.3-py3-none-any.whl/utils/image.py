import base64


def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        # 读取图片文件并转换为base64
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")  # 转换为字符串

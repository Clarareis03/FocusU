import base64
from pathlib import Path


def get_image_as_base64(path):
    p = Path(path)
    if not p.exists():
        return ""
    with open(p, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{data}"

def uploaded_file_to_base64(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode()
        return f"data:{uploaded_file.type};base64,{base64_str}"
    return None
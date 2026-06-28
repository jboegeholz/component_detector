import photos
import ui
import io


class Camera:

    def capture(self):
        return photos.capture_image()


def image_for_preview(image):
    if image is None:
        return None

    if image.__class__.__module__ == "ui":
        return image

    data = image_to_png_data(image)
    if data is None:
        return None

    return ui.Image.from_data(data)


def image_to_png_data(image):
    if image is None:
        return None

    if hasattr(image, "to_png"):
        return image.to_png()

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()

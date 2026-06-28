import photos
import ui


class Camera:

    def capture(self):
        return photos.capture_image()


def image_for_preview(image):
    if image is None:
        return None

    if image.__class__.__module__ == "ui":
        return image

    if hasattr(image, "to_png"):
        return ui.Image.from_data(image.to_png())

    try:
        import io
    except ImportError:
        return None

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return ui.Image.from_data(buffer.getvalue())

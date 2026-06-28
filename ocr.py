import re
import threading
from ctypes import c_void_p, create_string_buffer


try:
    from objc_util import ObjCBlock, ObjCClass, ObjCInstance, ns
except ImportError:
    ObjCBlock = None
    ObjCClass = None
    ObjCInstance = None
    ns = None


class OcrError(Exception):
    pass


def recognize_text(image):
    if ObjCClass is None:
        raise OcrError("OCR benoetigt Pythonista auf iOS mit objc_util.")

    ui_image = image_to_objc_image(image)
    if ui_image is None or ui_image.CGImage() is None:
        raise OcrError("Bild konnte nicht fuer OCR vorbereitet werden.")

    Vision = ObjCClass("VNImageRequestHandler")
    Request = ObjCClass("VNRecognizeTextRequest")

    state = {
        "done": threading.Event(),
        "texts": [],
        "error": None,
    }

    def completion(request_ptr, error_ptr):
        try:
            if error_ptr:
                state["error"] = str(ObjCInstance(error_ptr))
                return

            request = ObjCInstance(request_ptr)
            results = request.results()

            for observation in results:
                candidates = observation.topCandidates_(1)
                candidate = candidates.firstObject()
                if candidate:
                    state["texts"].append(str(candidate.string()))
        finally:
            state["done"].set()

    completion_block = ObjCBlock(
        completion,
        restype=None,
        argtypes=[c_void_p, c_void_p]
    )
    state["completion_block"] = completion_block

    request = Request.alloc().initWithCompletionHandler_(completion_block)
    request.setRecognitionLevel_(0)
    request.setUsesLanguageCorrection_(False)

    handler = Vision.alloc().initWithCGImage_options_(ui_image.CGImage(), ns({}))
    success = handler.performRequests_error_(ns([request]), None)

    if not success:
        raise OcrError("OCR konnte nicht gestartet werden.")

    state["done"].wait(10)

    if not state["done"].is_set():
        raise OcrError("OCR hat zu lange gedauert.")

    if state["error"]:
        raise OcrError(state["error"])

    return "\n".join(state["texts"])


def image_to_objc_image(image):
    if hasattr(image, "CGImage"):
        return image

    try:
        if image.__class__.__module__ == "ui":
            return ObjCInstance(image)
    except ImportError:
        pass
    except TypeError:
        pass

    try:
        from camera import image_to_png_data
    except ImportError:
        return None

    png_data = image_to_png_data(image)
    if not png_data:
        return None

    raw = create_string_buffer(png_data)

    NSData = ObjCClass("NSData")
    UIImage = ObjCClass("UIImage")
    data = NSData.dataWithBytes_length_(raw, len(png_data))
    ui_image = UIImage.imageWithData_(data)
    ui_image._python_buffer = raw
    return ui_image


def find_mpn(text):
    candidates = []

    for token in re.findall(r"[A-Z0-9][A-Z0-9.\-_/]{2,}", text.upper()):
        normalized = token.strip(".-_/")

        if len(normalized) < 3:
            continue

        if any(char.isdigit() for char in normalized):
            candidates.append(normalized)

    if not candidates:
        return ""

    return max(candidates, key=len)

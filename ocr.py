import re
import threading
from ctypes import c_void_p


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

    ui_image = image_to_ui_image(image)
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


def image_to_ui_image(image):
    if hasattr(image, "CGImage"):
        return image

    try:
        import io
        from objc_util import ObjCClass
    except ImportError:
        return None

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    NSData = ObjCClass("NSData")
    UIImage = ObjCClass("UIImage")
    data = NSData.dataWithBytes_length_(buffer.getvalue(), len(buffer.getvalue()))
    return UIImage.imageWithData_(data)


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

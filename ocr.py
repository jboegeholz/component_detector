import re
from ctypes import create_string_buffer


try:
    from objc_util import ObjCClass, ns
except ImportError:
    ObjCClass = None
    ns = None


class OcrError(Exception):
    pass


def recognize_text(image):
    if ObjCClass is None:
        raise OcrError("OCR benoetigt Pythonista auf iOS mit objc_util.")

    image_data = image_to_nsdata(image)
    if image_data is None:
        raise OcrError("Bild konnte nicht fuer OCR vorbereitet werden.")

    Vision = ObjCClass("VNImageRequestHandler")
    Request = ObjCClass("VNRecognizeTextRequest")

    request = Request.alloc().init()
    request.setRecognitionLevel_(0)
    request.setUsesLanguageCorrection_(False)

    handler = Vision.alloc().initWithData_options_(image_data, ns({}))
    success = handler.performRequests_error_(ns([request]), None)

    if not success:
        raise OcrError("OCR konnte nicht gestartet werden.")

    texts = []
    results = request.results()

    for observation in results:
        candidates = observation.topCandidates_(1)
        candidate = candidates.firstObject()
        if candidate:
            texts.append(str(candidate.string()))

    return "\n".join(texts)


def image_to_nsdata(image):
    try:
        from camera import image_to_png_data
    except ImportError:
        return None

    png_data = image_to_png_data(image)
    if not png_data:
        return None

    raw = create_string_buffer(png_data)

    NSData = ObjCClass("NSData")
    data = NSData.dataWithBytes_length_(raw, len(png_data))
    data._python_buffer = raw
    return data


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

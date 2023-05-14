import hashlib
import imghdr
import os

IMG_PATH = "exchanges/images"


def get_images():
    """Return a list of all images to publish

    :rtype: str

    """
    files = []
    for _dirpath, _dirnames, filenames in os.walk(IMG_PATH):
        for filename in filenames:
            if filename[-3:] == "jpg":
                files.append("%s/%s" % (IMG_PATH, filename))
    return files


def mime_type(filename):
    """Return the mime_type of the file

    :param str filename: The path to the image file
    :rtype: str

    """
    return "image/%s" % imghdr.what(filename)


def read_image(filename):
    """Read in the file from path and return the opaque binary data

    :rtype: str

    """
    with open(filename, "rb") as handle:
        return handle.read()


def write_temp_file(obd, mime_type):
    """Write out the binary data passed in to a temporary file, using the
    mime_type to determine the file extension.

    :param str obd: The opaque binary data
    :param str mime_type: The image mime_type
    :rtype: str

    """
    h = hashlib.sha1()
    h.update(obd)
    if mime_type in ["image/jpg", "image/jpeg"]:
        filename = "%s.jpg" % (h.hexdigest())
    elif mime_type == "image/png":
        filename = "%s.png"
    else:
        raise ValueError("Unsupported mime-type: %s" % mime_type)
    filename = "/tmp/%s" % filename
    with open(filename, "wb") as handle:
        handle.write(obd)
    return filename

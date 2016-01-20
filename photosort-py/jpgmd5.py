import Image

import hashlib

im = Image.open('foo.jpg')

hashlib.md5(im.tostring()).hexdigest()

hashlib.sha512(im.tostring()).hexdigest()


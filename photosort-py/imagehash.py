import struct
import os
import hashlib

def png(fh):
    hash = hashlib.md5()
    assert fh.read(8)[1:4] == "PNG"
    while True:
        try:
            length, = struct.unpack(">i",fh.read(4))
        except struct.error:
            break
        if fh.read(4) == "IDAT":
            hash.update(fh.read(length))
            fh.read(4) # CRC
        else:
            fh.seek(length+4,os.SEEK_CUR)
    print "Hash: %r" % hash.digest()

def jpeg(fh):
    hash = hashlib.md5()
    assert fh.read(2) == "\xff\xd8"
    while True:
        marker,length = struct.unpack(">2H", fh.read(4))
        assert marker & 0xff00 == 0xff00
        if marker == 0xFFDA: # Start of stream
            hash.update(fh.read())
            break
        else:
            fh.seek(length-2, os.SEEK_CUR)
    print "Hash: %r" % hash.digest()


if __name__ == '__main__':
    png(file("sample.png"))
    jpeg(file("sample.jpg"))


"""
Uses python 3.x and the pillow package
"""
from PIL import Image
import sys


arg = sys.argv
if len(arg)>=3:
    # Path to the source
    src = arg[1]

    # Path to the destination
    dst = arg[2]

    with open(src, "rb") as file:
        data = file.read()
        file.close()
    
    img_data = []

    # Start after the header
    off = 4

    # While the block is not filled with 0s and the EOF is not reached
    while data[off:off+5]!=b'\x00\x00\x00\x00\x00' and off+5<=len(data):
        # Add (byte 1) pixels with color specified by (byte1-4) to the image data
        img_data.extend([data[off+1:off+4]]*data[off])
        
        # Check just in case if byte 4 is not 0x80
        if data[off+4]!=0x80:
            print("Not 0x80:", hex(off+4))

        # Go to the next block
        off+=5

    # WARNING! Image parts size and  positions in the global image are hard-coded, it should be determined by another file
    parts = [(256,256,0,0),
             (256,256,256,0),
             (128,256,512,0),
             (256,128,0,256),
             (256,128,256,256),
             (128,128,512,256),
             (256,64,0,384),
             (256,64,256,384),
             (128,64,512,384)]

    # WARNING! Hard-coded size
    im = Image.new(mode="RGB", size=(640,448), color=(0,0,0))
    off = 0
    for p in parts:
        im2 = Image.frombytes(mode="RGB", data=b''.join(img_data[off:off+p[0]*p[1]]), size=(p[0], p[1]))
        im.paste(im2, box=(p[2], p[3]))
        off += p[0]*p[1]

    # Save the image
    im.save(dst, "PNG")

else:
    print("Usage: "+arg[0]+" in_file out_file")


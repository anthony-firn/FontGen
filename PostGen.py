from PIL import Image
import os

def parse_image(image, end, i, char):
    im = Image.open(image)
    pix = im.load()
    length, height = im.size
    Stats[FontName[i]][char] = {}

    print(str(length) + ", " + str(height))
    minx = 0
    maxx = 1
    miny = 0
    maxy = 1
    nibbles = 0

    # get minx of the image
    for x in range(length):
        for y in range(height):
            rgb = list(pix[x,y])
            r = rgb[0]
            if r != 255:
                minx = x
                break
        else:
            continue
        break
    # get maxx of the image
    for x in range(length-1, -1, -1):
        for y in range(height):
            rgb = list(pix[x,y])
            r = rgb[0]
            if r != 255:
                maxx = x+1
                break
        else:
            continue
        break

    # get miny of the image
    for y in range(height):
        for x in range(length):
            rgb = list(pix[x,y])
            r = rgb[0]
            if r != 255:
                miny = y
                break
        else:
            continue
        break
    
    # get maxy of the image
    for y in range(height-1, -1, -1):
        for x in range(length):
            rgb = list(pix[x,y])
            r = rgb[0]
            if r != 255:
                maxy = y+1
                break
        else:
            continue
        break

    # determine odd widths
    oddPos = True
    oddSize = False
    if (maxx - minx) % 2 == 1:
        oddSize = True

    # record the size for the struct
    print(maxx-minx)
    if oddSize:
        Stats[FontName[i]][char]["width"] = maxx-minx + 1
    else:
        Stats[FontName[i]][char]["width"] = maxx-minx
    Stats[FontName[i]][char]["height"] = maxy-miny
    endy = False
    for y in range(miny, maxy):
        if y == maxy-1:
            endy = True

        endx = False
        for x in range(minx, maxx):
            if x == maxx-1:
                endx = True
            rgb = list(pix[x,y])
            r = rgb[0]
            # invert scale
            if FontInv[i] == 'y':
                r = int(r/17)
            else:
                r = int((255-r)/17)
            if oddPos:
                f.write("0x" + '{:01X}'.format(r))
                nibbles += 1
                oddPos = False
            else:
                if end and endy and endx:
                    f.write('{:01X}'.format(r))
                    nibbles += 1
                else:
                    f.write('{:01X}'.format(r) + ", ")
                    nibbles += 1
                    oddPos = True
        if oddSize:
            if end and endy and endx:
                f.write("0")
                nibbles += 1
            else:
                f.write("0, ")
                nibbles += 1
                oddPos = True

        if end and endy and endx:
            f.write("\n};\n")
        else:
            f.write("\n" + tab)

    return nibbles, miny, maxy
        

SetName = input("What is the set name: ")
if (SetName[-2] != ".h"):
    SetName = SetName + ".h"

f = open(SetName, "w")
f.write("#include \"globals.h\"\n\n")

FontNum = int(input("How many different font sets do you want: "))
FontName = []
FontPath = []
FontInv = []
Padding = {}
Stats = {}
tab = "    "

for i in range(FontNum):
    FontName.append(input("Name for font " + str(i) + ": "))
    FontPath.append(input("Resource path for font " + str(i) + ": "))
    FontInv.append(input("Invert scale? (y/n)").lower())
    if input("Do you want to add padding to any character in the set? (y/n) ").lower() == "y":
        done = False
        Padding[FontName[i]] = {}
        while not done:
            char = input("Character that needs padding: ")
            Padding[FontName[i]][char] = [int(input("Left padding: ")), int(input("Right padding: "))]
            if input("Add padding to more characters in this set? (y/n) ").lower() == "n":
                    done = True
            
for i in range(FontNum):
    directory = os.fsencode(FontPath[i])
    dicName = directory.decode("utf-8")

    f.write("const char " + FontName[i] + "[] =\n{\n")
    Stats[FontName[i]] = {}

    dirSize = 0
    for file in os.listdir(directory):
        dirSize += 1

    fileCount = 0
    for file in os.listdir(directory):
        # keep track of which file your on to determine when the end is
        fileCount += 1
        end = False
        if fileCount == dirSize:
            end = True

        filename = os.fsdecode(file)
        if filename[-4:] == ".png" or filename[-4:] == ".jpg":
            char = filename.replace(".png", "")

            if (dicName[-1] != "/"):
                image = dicName + "/" + filename
            else:
                image = dicName + filename

            f.write("\n" + tab + "// 4bit grey scale for char " + char + "\n" + tab)
            parse_image(image, end, i, char)

for i in range(FontNum):
    byteTotal = 0
    f.write("\nenhancedFontStruct " + FontName[i] + "Struct[] =\n{")
    for k in Stats[FontName[i]]:
        width = Stats[FontName[i]][k]["width"]
        height = Stats[FontName[i]][k]["height"]
        f.write("\n    {'" + k + "', &" + FontName[i] + "[" + str(int(byteTotal)) + "], ")
        f.write(str(height))
        f.write(", ")
        f.write(str(width))
        f.write(", 0},")
        byteTotal += (width*height)/2

    f.write("\n    {0, NULL, 0, 0, 0}                    // Terminator\n};\n\n")
            

#!/usr/bin/env python

# Generates Font images

from gimpfu import *

def font_gen(initstr, path, font, size, color) :
    # First do a quick sanity check on the font
    if font == 'Comic Sans MS' :
        initstr = "Comic Sans? Are you sure?"
    for char in initstr:
        # Make a new image. Size 10x10 for now -- we'll resize later.
        img = gimp.Image(1, 1, RGB)

        # Save the current foreground color:
        pdb.gimp_context_push()

        # Set the text color
        gimp.set_foreground(color)

        # Create a new text layer (-1 for the layer means create a new layer)
        layer = pdb.gimp_text_fontname(img, None, 0, 0, char, 10,
                                   True, size, PIXELS, font)

        # Resize the image to the size of the layer
        img.resize(layer.width, layer.height, 0, 0)

        # Background layer.
        # Can't add this first because we don't know the size of the text layer.
        background = gimp.Layer(img, "Background", layer.width, layer.height,
                            RGB_IMAGE, 100, NORMAL_MODE)
        background.fill(BACKGROUND_FILL)
        img.add_layer(background, 1)

        # Create a new image window
        gimp.Display(img)
        # Show the new image window
        gimp.displays_flush()

        # Restore the old foreground color:
        pdb.gimp_context_pop()

        # Save resulting image
        new_image = pdb.gimp_image_duplicate(img)
        layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
        pdb.gimp_file_save(new_image, layer, path + "/" + char + '.png', '?')
        pdb.gimp_image_delete(new_image)

register(
    "python_fu_Font_Gen",
    "Select font settings",
    "Create a new image with your text string",
    "Anthony Fortner",
    "Anthony Fortner",
    "2020",
    "Font Generator (Py)...",
    "",      # Create a new image, don't work on an existing one
    [
        (PF_STRING, "string", "Text string", 'ABCDEFGabcdefghi'),
        (PF_DIRNAME, "outputFolder", "Output directory", "/tmp"),
        (PF_FONT, "font", "Font face", "Sans"),
        (PF_SPINNER, "size", "Font size", 20, (1, 3000, 1)),
        (PF_COLOR, "color", "Text color", (0.0, 0.0, 0.0))
    ],
    [],
    font_gen, menu="<Image>/File/Create")

main()


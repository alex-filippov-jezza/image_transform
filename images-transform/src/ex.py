import io
import os
import math
import PySimpleGUI as sg
from PIL import Image, ImageOps

file_types = [("PNG (*.png)", "*.png"), ("BMP (*.bmp)", "*.bmp"),
              ("PCX (*.pcx, *.pcc)", "*.pcx" "*.pcc")
              ]


def main():
    global image
    layout = [
        [sg.Image(key="-IMAGE-"), sg.Image(key="-IMAGE_TRANSFORM-")],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
        ],
        [sg.Button("Halftone"),
         sg.Button("Halftone to B/W"),
         sg.Button("Negative")
         ],
        [sg.Input(size=(25, 1), key="-PARAMETER-"),
         sg.Button("Log Transform"),
         sg.Button("Exp Transform")
         ]

    ]
    window = sg.Window("Image Transform", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "Load Image":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

        if event == "Halftone":
            imageSemi = image.convert('L')
            imageSemi.thumbnail((400, 400))
            bio = io.BytesIO()
            imageSemi.save(bio, format="PNG")
            window["-IMAGE_TRANSFORM-"].update(data=bio.getvalue())

        if event == "Halftone to B/W":
            imageBW = image.convert('L').convert('1', dither=Image.NONE)
            bio = io.BytesIO()
            imageBW.save(bio, format="PNG")
            window["-IMAGE_TRANSFORM-"].update(data=bio.getvalue())

        if event == "Negative":
            imageNegative = ImageOps.invert(image)
            bio = io.BytesIO()
            imageNegative.save(bio, format="PNG")
            window["-IMAGE_TRANSFORM-"].update(data=bio.getvalue())

        if event == "Log Transform":
            image_log = image.convert('L')
            data = image_log.getdata()
            new_data = [int(int(values["-PARAMETER-"]) * math.log(1 + f / 256.0)) for f in data]
            image_log.putdata(new_data)
            bio = io.BytesIO()
            image_log.save(bio, format="PNG")
            window["-IMAGE_TRANSFORM-"].update(data=bio.getvalue())

        if event == "Exp Transform":
            image_exp = image.convert('L')
            data = image_exp.getdata()
            new_data = [int(int(values["-PARAMETER-"]) * (f / 256.0) ** 0.5) for f in data]
            image_exp.putdata(new_data)
            bio = io.BytesIO()
            image_exp.save(bio, format="PNG")
            window["-IMAGE_TRANSFORM-"].update(data=bio.getvalue())


    window.close()


if __name__ == "__main__":
    main()

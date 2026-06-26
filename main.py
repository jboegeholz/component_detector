# This is a sample Python script.
import io

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import ui
import photos
from PIL import ImageOps

class MainView(ui.View):

    def __init__(self):
        self.name = "Bauteil Scanner"
        self.background_color = "#1c1c1e"

        title = ui.Label()
        title.text = "Bauteil Scanner"
        title.font = ("<System-Bold>", 28)
        title.text_color = "white"
        title.alignment = ui.ALIGN_CENTER
        title.frame = (20, 60, self.width-40, 40)
        title.flex = "W"
        self.add_subview(title)

        info = ui.Label()
        info.text = "Fotografiere ein Bauteil zum Vergleichen."
        info.text_color = "#AAAAAA"
        info.alignment = ui.ALIGN_CENTER
        info.frame = (20, 105, self.width-40, 30)
        info.flex = "W"
        self.add_subview(info)

        btn = ui.Button()
        btn.title = "Foto aufnehmen"
        btn.font = ("<System-Bold>", 22)
        btn.tint_color = "white"
        btn.background_color = "#007AFF"
        btn.corner_radius = 15
        btn.frame = (40, 220, self.width-80, 60)
        btn.flex = "W"
        btn.action = self.take_photo
        self.add_subview(btn)

    def layout(self):
        self.subviews[0].frame = (20, 60, self.width-40, 40)
        self.subviews[1].frame = (20, 105, self.width-40, 30)
        self.subviews[2].frame = (40, self.height/2-30, self.width-80, 60)

    def take_photo(self, sender):
        pil = photos.capture_image()

        if pil:
            # EXIF-Rotation übernehmen
            pil = ImageOps.exif_transpose(pil)

            b = io.BytesIO()
            pil.save(b, 'JPEG')
            b.seek(0)

            img = ui.Image.from_data(b.read())

            iv = ui.ImageView()
            iv.image = img
            iv.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
            iv.flex = 'WH'

            v = ui.View(bg_color='black')
            iv.frame = v.bounds
            v.add_subview(iv)

            v.present('fullscreen')


MainView().present("fullscreen")
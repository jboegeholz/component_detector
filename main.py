# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import ui
import photos

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
        btn.title = "📷  Foto aufnehmen"
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
        image = photos.capture_image()

        if image:
            img_view = ui.ImageView()
            img_view.frame = self.bounds
            img_view.flex = "WH"
            img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
            img_view.image = image

            preview = ui.View()
            preview.name = "Vorschau"
            preview.background_color = "black"
            preview.add_subview(img_view)

            preview.present("fullscreen")


MainView().present("fullscreen")
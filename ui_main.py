import ui


class MainView(ui.View):

    def __init__(self):
        self.name = 'Bauteil Scanner'
        self.background_color = '#111111'

        self.build()

    def build(self):

        # Titel
        title = ui.Label()
        title.text = 'Bauteil Scanner'
        title.font = ('<System-Bold>', 30)
        title.text_color = 'white'
        title.alignment = ui.ALIGN_CENTER
        title.frame = (0, 50, self.width, 40)
        title.flex = 'W'

        self.add_subview(title)
        # Schließen-Button

        close_btn = ui.Button()
        close_btn.title = "✕"
        close_btn.frame = (self.width - 60, 50, 40, 40)
        close_btn.flex = 'L'
        close_btn.font = ('<System-Bold>', 22)
        close_btn.tint_color = 'white'
        close_btn.action = self.close_view

        self.add_subview(close_btn)

        self.close_btn = close_btn
        # Bildvorschau

        self.preview = ui.ImageView()
        self.preview.background_color = '#222222'
        self.preview.corner_radius = 12
        self.preview.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
        self.preview.frame = (20,120,self.width-40,250)
        self.preview.flex='W'

        self.add_subview(self.preview)

        # Button Kamera

        b = ui.Button()

        b.title = "📷 Foto aufnehmen"
        b.frame = (20,400,self.width-40,55)
        b.corner_radius = 12
        b.background_color = "#007AFF"
        b.tint_color = "white"
        b.font = ("<System-Bold>",20)
        b.flex='W'

        b.action=self.take_photo

        self.add_subview(b)

    def layout(self):

        self.preview.frame = (
            20,
            120,
            self.width - 40,
            self.height * 0.45
        )

        self.close_btn.frame = (
            self.width - 55,
            50,
            35,
            35
        )

    def take_photo(self,sender):

        print("Kamera kommt als Nächstes 😊")

    def close_view(self, sender):
        self.close()
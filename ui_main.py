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

        self.preview.frame=(20,120,self.width-40,self.height*0.45)

    def take_photo(self,sender):

        print("Kamera kommt als Nächstes 😊")
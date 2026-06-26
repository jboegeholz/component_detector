import ui
from database import Database


class MainView(ui.View):

    def __init__(self):
        self.name = 'Bauteil Scanner'
        self.background_color = '#111111'
        self.db = Database()
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
        self.preview.frame = (20, 120, self.width - 40, 250)
        self.preview.flex = 'W'

        self.add_subview(self.preview)

        self.search = ui.TextField(frame=(20, 120, self.width - 40, 40))
        self.search.placeholder = "MPN eingeben"
        self.add_subview(self.search)

        btn = ui.Button()
        btn.title = "🔍 Suchen"
        btn.frame = (20, 175, self.width - 40, 45)
        btn.background_color = "#007AFF"
        btn.tint_color = "white"
        btn.corner_radius = 10
        btn.action = self.search_part
        self.add_subview(btn)

        self.result = ui.TextView()
        self.result.editable = False
        self.result.background_color = "#222222"
        self.result.text_color = "white"
        self.result.font = ("Menlo", 18)
        self.result.frame = (20, 240, self.width - 40, 220)
        self.add_subview(self.result)

        # Button Kamera

        b = ui.Button()

        b.title = "📷 Foto aufnehmen"
        b.frame = (20, 400, self.width - 40, 55)
        b.corner_radius = 12
        b.background_color = "#007AFF"
        b.tint_color = "white"
        b.font = ("<System-Bold>", 20)
        b.flex = 'W'

        b.action = self.take_photo

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

    def take_photo(self, sender):
        print("Kamera kommt als Nächstes 😊")

    def close_view(self, sender):
        self.close()

    def search_part(self, sender):
        mpn = self.search.text.strip()

        part = self.db.find(mpn)

        if part is None:
            self.result.text = "Nicht gefunden."

            return

        self.result.text = f"""
    MPN

    {part.mpn}

    VDS

    {part.vds} V

    RDS(on)

    {part.rdson} Ω
    """

import ui
from camera import Camera, image_for_preview
from component import Component
from database import Database
from ocr import OcrError, find_mpn, recognize_text


class MainView(ui.View):

    def __init__(self):
        self.name = 'Bauteil Scanner'
        self.background_color = '#111111'
        self.db = Database()
        self.db.create()
        self.build()

    def build(self):
        # Titel
        self.title = ui.Label()
        self.title.text = 'Bauteil Scanner'
        self.title.font = ('<System-Bold>', 30)
        self.title.text_color = 'white'
        self.title.alignment = ui.ALIGN_CENTER
        self.title.frame = (0, 50, self.width, 40)
        self.title.flex = 'W'

        self.add_subview(self.title)
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
        self.preview.hidden = True

        self.add_subview(self.preview)

        self.search = ui.TextField(frame=(20, 120, self.width - 40, 40))
        self.search.placeholder = "MPN eingeben"
        self.add_subview(self.search)

        self.search_btn = ui.Button()
        self.search_btn.title = "🔍 Suchen"
        self.search_btn.frame = (20, 175, self.width - 40, 45)
        self.search_btn.background_color = "#007AFF"
        self.search_btn.tint_color = "white"
        self.search_btn.corner_radius = 10
        self.search_btn.action = self.search_part
        self.add_subview(self.search_btn)



        self.result = ui.TextView()
        self.result.editable = False
        self.result.background_color = "#222222"
        self.result.text_color = "white"
        self.result.font = ("Menlo", 26)
        self.result.alignment = ui.ALIGN_LEFT
        self.result.frame = (20, 295, self.width - 40, 180)
        self.add_subview(self.result)

        # Button Kamera

        self.photo_btn = ui.Button()

        self.photo_btn.title = "📷 Foto aufnehmen"
        self.photo_btn.frame = (20, 490, self.width - 40, 55)
        self.photo_btn.corner_radius = 12
        self.photo_btn.background_color = "#007AFF"
        self.photo_btn.tint_color = "white"
        self.photo_btn.font = ("<System-Bold>", 20)
        self.photo_btn.flex = 'W'

        self.photo_btn.action = self.take_photo

        self.add_subview(self.photo_btn)

        self.add_btn = ui.Button()
        self.add_btn.title = "MOSFET anlegen"
        self.add_btn.frame = (20, 230, self.width - 40, 45)
        self.add_btn.background_color = "#34C759"
        self.add_btn.tint_color = "white"
        self.add_btn.corner_radius = 10
        self.add_btn.action = self.show_add_mosfet
        self.add_subview(self.add_btn)

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
        self.title.frame = (0, 50, self.width, 40)
        self.search.frame = (20, 120, self.width - 40, 40)
        self.search_btn.frame = (20, 175, self.width - 40, 45)
        self.result.frame = (20, 295, self.width - 40, 180)
        self.photo_btn.frame = (20, 490, self.width - 40, 55)
        self.add_btn.frame = (20, 230, self.width - 40, 45)

    def take_photo(self, sender):
        image = Camera().capture()

        if image is None:
            return

        self.result.text = "Foto geladen."
        self.preview.image = image_for_preview(image)
        self.clear_preview()
        self.result.text = "OCR startet..."
        ui.delay(lambda: self.run_ocr(image), 0.3)

    def run_ocr(self, image):
        self.result.text = "OCR laeuft..."

        try:
            text = recognize_text(image)
        except OcrError as error:
            self.clear_preview()
            self.result.text = "OCR Fehler:\n" + str(error)
            return

        mpn = find_mpn(text)

        if not mpn:
            self.clear_preview()
            self.result.text = "Keine MPN erkannt.\n\n" + text
            return

        self.search.text = mpn
        self.clear_preview()
        self.search_part()

    def clear_preview(self):
        self.preview.image = None
        self.preview.hidden = True

    def close_view(self, sender):
        self.close()

    def show_add_mosfet(self, sender):
        AddMosfetView(self.db).present('sheet')

    def search_part(self, sender=None):
        mpn = self.search.text.strip()

        part = self.db.find(mpn)

        if part is None:
            self.result.text = "Nicht gefunden."

            return

        self.result.text = (
            f"MPN {part.mpn}\n"
            f"Hersteller {part.manufacturer}\n"
            f"VDS {part.vds} V\n"
            f"RDS(on) {part.rdson} Ω"
            f"Dauerstrom {part.continous_drain_current} A"
        )


class AddMosfetView(ui.View):

    def __init__(self, db):
        self.name = "MOSFET anlegen"
        self.frame = (0, 0, 360, 520)
        self.background_color = "#111111"
        self.db = db
        self.build()

    def build(self):
        title = ui.Label()
        title.text = "MOSFET anlegen"
        title.font = ("<System-Bold>", 26)
        title.text_color = "white"
        title.alignment = ui.ALIGN_CENTER
        title.frame = (20, 30, self.width - 40, 40)
        title.flex = "W"
        self.add_subview(title)

        self.mpn = self.add_text_field("MPN", 95)
        self.vds = self.add_text_field("VDS in V", 155)
        self.rdson = self.add_text_field("RDS(on) in Ohm", 215)

        save_btn = ui.Button()
        save_btn.title = "Speichern"
        save_btn.frame = (20, 285, self.width - 40, 48)
        save_btn.flex = "W"
        save_btn.background_color = "#34C759"
        save_btn.tint_color = "white"
        save_btn.corner_radius = 10
        save_btn.font = ("<System-Bold>", 18)
        save_btn.action = self.save
        self.add_subview(save_btn)

        cancel_btn = ui.Button()
        cancel_btn.title = "Abbrechen"
        cancel_btn.frame = (20, 345, self.width - 40, 44)
        cancel_btn.flex = "W"
        cancel_btn.tint_color = "white"
        cancel_btn.action = self.cancel
        self.add_subview(cancel_btn)

        self.message = ui.Label()
        self.message.text_color = "white"
        self.message.alignment = ui.ALIGN_CENTER
        self.message.number_of_lines = 0
        self.message.frame = (20, 405, self.width - 40, 70)
        self.message.flex = "W"
        self.add_subview(self.message)

    def add_text_field(self, placeholder, y):
        field = ui.TextField(frame=(20, y, self.width - 40, 42))
        field.flex = "W"
        field.placeholder = placeholder
        field.background_color = "white"
        field.text_color = "black"
        field.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
        self.add_subview(field)
        return field

    def save(self, sender):
        mpn = self.mpn.text.strip()

        if not mpn:
            self.show_error("MPN fehlt.")
            return

        try:
            vds = self.parse_float(self.vds.text)
            rdson = self.parse_float(self.rdson.text)
        except ValueError:
            self.show_error("VDS und RDS(on) muessen Zahlen sein.")
            return

        self.db.add(Component(mpn, vds, rdson))
        self.message.text_color = "#34C759"
        self.message.text = "MOSFET gespeichert."

    def cancel(self, sender):
        self.close()

    def show_error(self, text):
        self.message.text_color = "#FF453A"
        self.message.text = text

    def parse_float(self, text):
        return float(text.strip().replace(",", "."))

class Component:

    def __init__(self,
                 mpn="",
                 manufacturer="",
                 channel_type="",
                 vds=None,
                 rdson=None,
                 continous_drain_current=None
                 ):
        self.mpn = mpn
        self.manufacturer = manufacturer
        self.channel_type = channel_type
        self.vds = vds
        self.rdson = rdson
        self.continous_drain_current = continous_drain_current

    def __str__(self):
        return self.mpn

class Component:

    def __init__(self,
                 mpn="",
                 vds=None,
                 rdson=None,
                 ):
        self.mpn = mpn
        self.vds = vds
        self.rdson = rdson

    def __str__(self):
        return self.mpn

class Component:

    def __init__(self,
                 mpn="",
                 manufacturer="",
                 package="",
                 vds=None,
                 current=None,
                 rds_on=None,
                 logic_level=False):

        self.mpn = mpn
        self.manufacturer = manufacturer
        self.package = package
        self.vds = vds
        self.current = current
        self.rds_on = rds_on
        self.logic_level = logic_level

    def __str__(self):
        return self.mpn
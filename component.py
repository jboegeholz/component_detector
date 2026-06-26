class Component:

    def __init__(self,
                 mpn="",
                 vds=None,
                 rds_on=None,
                 ):
        self.mpn = mpn
        self.vds = vds
        self.rds_on = rds_on

    def __str__(self):
        return self.mpn

from app.admin.interfaces.Indicator import Indicator

class IoerIndicator(Indicator):
    def __init__(self,id, name, description, time_string, spatial_extends, units, methodology,colors=None,cat=None):
        self.id = id
        self.name=name
        self.description=description
        self.time_string=time_string
        self.spatial_extends=spatial_extends
        self.units=units
        self.methodology=methodology
        self.colors=colors
        self.cat=cat

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_time(self):
        return self.time_string

    def get_spatial_extends(self):
        return self.spatial_extends

    def get_units(self):
        return self.units

    def get_methodogy(self):
        return self.methodology

    def get_colors(self):
        return self.colors

    def get_cat(self):
        return self.cat

    def toJSON(self,state="create"):
        return {self.id:{
                "state": state,
                "name": self.name,
                "description": self.description,
                "times": self.time_string,
                "spatial_extends": self.spatial_extends,
                "unit": self.units,
                "methodik": self.methodology
            }}

import json


class Toolbox:
    def clean_string(self, string):
        d = {"\\": "", "\n": "",'"':"","Kurzbeschreibung":"","  ":""}
        for i, j in d.items():
            string = string.replace(i, j)
        return string.strip()

    def json_validator(self,data):
        try:
            json.loads(data)
            return True
        except ValueError as error:
            return False



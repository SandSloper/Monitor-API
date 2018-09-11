class StringConverter:
    def cleanString(self,string):
        d = {"\\": "", "\n": "",'"':"","Kurzbeschreibung":"","  ":""}
        for i, j in d.items():
            string = string.replace(i, j)
        return string.strip()
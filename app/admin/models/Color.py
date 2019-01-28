from colormap import rgb2hex, hex2rgb

class Color:
    def __init__(self,min_color,max_color,classes):
        self.min_color=min_color
        self.max_color=max_color
        self.classes=(int(classes))

    def Berechnung(self,min_color,max_color):
        klasse=[]
        if min_color<max_color:
            width=round((max_color-min_color)/(self.classes-1))
            klasse.append(min_color)
            for x in range(0,self.classes-1):
                klasse.append(min_color+(width*x))

            klasse.append(max_color)

        elif min_color>max_color:
            width = round((min_color-max_color)/(self.classes-1))
            klasse.append(min_color)
            for x in range(0,self.classes-1):
                klasse.append(min_color-(width*x))

            klasse.append(max_color)

        elif min_color==max_color:
            klasse.append(min_color)
            for x in range(0,self.classes-1):
                klasse.append(min_color)

            klasse.append(min_color)

        return klasse

    def HexToRGB(self,hex):
        if "#" not in hex:
            hex="#{}".format(hex)

        return hex2rgb(hex,normalise=False)

    def RGBToHex(self,r,g,b):
        return rgb2hex(r,g,b)

    def buildColorPalette(self):
        colors = []
        #convert color in RGB
        colmin_rgb = self.HexToRGB(self.min_color)
        colmax_rgb = self.HexToRGB(self.max_color)

        r = self.Berechnung(colmin_rgb[0],colmax_rgb[0])
        g = self.Berechnung(colmin_rgb[1],colmax_rgb[1])
        b = self.Berechnung(colmin_rgb[2],colmax_rgb[2])

        for x in range(0,len(r)):
            colors.append(self.RGBToHex(r[x],g[x],b[x]))

        return colors

    def toString(self):
        return {"min_color":self.min_color,"max_color":self.max_color,"classes":self.classes}
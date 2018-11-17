import json
from flask import Response
from app.flaechenportal import f_portal
from app.flaechenportal.parser import Parser

parser = Parser()

@f_portal.route('/', methods=['GET', 'POST'])
def parse():
    pages = [
        {"id": "arl", "url": "https://www.arl-net.de/events"},
        {"id": "bbsr", "url": "https://www.bbsr.bund.de/BBSR/DE/Aktuell/Veranstaltungen/veranstaltungen_node.html"},
        {"id": "bmu", "url": "https://www.bmu.de/service/veranstaltungen/"},
        {"id": "uba", "url": "https://www.umweltbundesamt.de/service/termine?tabc=1"},
        {"id": "nhr", "url": "https://www.nachhaltigkeitsrat.de/termine/"},
        {"id": "aktion_flaeche", "url": "https://aktion-flaeche.de/termine"}
    ]
    result = parser.parseEvents(pages)
    result = json.dumps(result,ensure_ascii=False)
    resp = Response(result,mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

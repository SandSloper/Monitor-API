#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup

from app.tools.Converter import *

class Parser:

    def ParseEvents(self,value):
        events = []
        strConverter = StringConverter()
        for o in value:
            page = requests.get(o['url'])
            id = o['id']
            soup = BeautifulSoup(page.content, 'html.parser')
            if id=="arl":
                table = soup.findAll("table", {"class": "views-table"})
                values = []
                for div in table:
                    rows = div.findAll('tr')
                    for row in rows:
                        start = row.find("span",{"class":"date-display-start"})
                        end = row.find("span",{"class":"date-display-end"})
                        name = row.find("a")
                        if start is not None:
                            date = strConverter.cleanString("{} - {}".format(start.getText(), end.getText()))
                            name_txt = strConverter.cleanString(name.getText())
                            values.append({"date":date,"name":name_txt, "url": "https://www.arl-net.de/{}".format(name.get('href'))})
                events.append({id: {"events": values}})
            elif id=="bbsr":
                table_div = soup.find("div", {"class": "singleview"})
                table = table_div.find("table")
                tBody = table.find("tbody")
                values = []
                for tr in tBody:
                    td_list = tr.find_all("td")
                    date = strConverter.cleanString(td_list[0].getText())
                    name = strConverter.cleanString(td_list[1].getText())
                    name_a = td_list[1].find('a')
                    url = name_a.get('href')
                    if name != "Kurzbeschreibung":
                        values.append({"date": date, "name": name,"url": "https://www.bbsr.bund.de/{}".format(url)})
                events.append({id: {"events": values}})
            elif id=="bmu":
                event_a = soup.findAll('div',{"class":"rf-c-item-list__body"})
                values = []
                for content in event_a:
                    info_span = content.find("span", {"class": "rf-c-typo:xs"})
                    text = content.find("a")
                    if info_span is not None:
                        name = strConverter.cleanString(text.getText())
                        url = text.get("href")
                        infos = info_span.getText()
                        infos = infos.split("|")
                        date = strConverter.cleanString(infos[0])
                        values.append({"date": date, "name": name, "url": "{}{}".format("https://www.bmu.de/service/veranstaltungen/",url)})
                events.append({id: {"events": values}})
            elif id=="uba":
                # todo
                text = soup
            elif id == "nhr":
                panel = soup.findAll("div",{"class","panel-content"})
                values = []
                for content in panel:
                    link = content.find("h4")
                    link = link.find("a")
                    name = strConverter.cleanString(link.getText())
                    link = link.get("href")
                    date = content.find("p",{"class","small-gray"})
                    date = date.getText()
                    date = date.split("|")
                    date = strConverter.cleanString(date[0])
                    values.append(
                        {"date": date, "name": name, "url": link})
                events.append({id: {"events": values}})
            elif id=="aktion_flaeche":
                panel = soup.findAll("div",{"class","node-difu_wrapper"})
                values = []
                for content in panel:
                    date = content.find("div",{"class","difu-start-ende"})
                    date = date.getText()
                    date = strConverter.cleanString(date)
                    name = content.find("h2",{"class","title"})
                    name = name.find("a")
                    link = name.get("href")
                    name = strConverter.cleanString(name.getText())
                    values.append(
                        {"date": date, "name": name, "url": link})
                events.append({id: {"events": values}})
        return events


from bs4 import BeautifulSoup
import requests
from flask import Flask, jsonify
URLsearch = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query="
URL = "https://www.transfermarkt.com"

app = Flask("TransferMarkAPI")


def getPlayerLink(player):
    res = requests.get(URLsearch + player,
                       headers={'User-Agent': 'Custom'}).text
    soup = BeautifulSoup(res, "html.parser")
    for link in soup.find_all("a"):
        if "profil/spieler" in link.get("href"):
            return link.get("href")


@app.get("/trophies/<player>")
def getPlayerTrophies(player):
    trophies = []
    link = getPlayerLink(player).replace("profil", "erfolge")
    res = requests.get(URL+link,
                       headers={"User-Agent": "Custom"}).text
    soup = BeautifulSoup(res, "html.parser").find(
        "div", {"id": "main"}).find_all("td", {"class": "hauptlink"})
    for trophy in soup:
        trophies.append(trophy.text)
    return jsonify(trophies)


@app.get("/stats/<player>")
def getPlayerStats(player):
    stats = {}
    link = getPlayerLink(player).replace("profil", "leistungsdatendetails")
    res = requests.get(URL+link,
                       headers={"User-Agent": "Custom"}).text
    soup = BeautifulSoup(res, "html.parser").find(
        "div", {"id": "main"}).find_all("td", {"class": "zentriert"})
    stats["matches"] = soup[1].text
    stats["goals"] = soup[2].text
    stats["assists"] = soup[3].text
    cards = soup[4].text.replace("\xa0", "").split("/")
    stats["Yellow Cards"] = cards[0]
    if cards[1] == "-":
        stats["Red Cards"] = cards[2]
    elif cards[2] == "-":
        stats["Red Cards"] = cards[1]
    else:
        stats["Red Cards"] = str(int(cards[1])+int(cards[2]))
    return jsonify(stats)


@app.get("/infos/<player>")
def getPlayerGenerals(player):
    link = getPlayerLink(player)
    res = requests.get(URL+link,
                       headers={"User-Agent": "Custom"}).text
    birth = BeautifulSoup(res, "html.parser").find(
        "span", {"itemprop": "birthDate"}).text.replace(" ", "").replace("\n", "")
    height = BeautifulSoup(res, "html.parser").find(
        "span", {"itemprop": "height"}).text
    nationality = BeautifulSoup(res, "html.parser").find(
        "span", {"itemprop": "nationality"}).text.strip()
    club = BeautifulSoup(res, "html.parser").find(
        "span", {"itemprop": "affiliation"}).a["title"]
    value = BeautifulSoup(res, "html.parser").find(
        "div", {"class": "tm-player-market-value-development__current-value"}).text.strip()
    position = BeautifulSoup(res, "html.parser").find_all("li")
    image = BeautifulSoup(res, "html.parser").find(
        "img", {"class": "data-header__profile-image"})["src"]
    for p in position:
        if "Position" in p.text:
            position = p.span.text.strip()
    generals = {
        "Date Of Birth": birth,
        "Height": height,
        "Nationality": nationality,
        "Club": club,
        "Value": value,
        "Position": position,
        "Image": image
    }
    return jsonify(generals)


app.run()

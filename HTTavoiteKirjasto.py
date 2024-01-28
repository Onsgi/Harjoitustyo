######################################################################
# CT60A0203 Ohjelmoinnin perusteet
# Tekijä: Otto Hongisto
# Opiskelijanumero: 001754850
# Päivämäärä: 9.12.2023
# Kurssin oppimateriaalien lisäksi työhön ovat vaikuttaneet seuraavat
# lähteet ja henkilöt, ja se näkyy tehtävässä seuraavalla tavalla:
# numby.org dokumentaatio. Opin sen kautta käyttämään komentoa array() ja concatenate()
#
# Mahdollisen vilppiselvityksen varalta vakuutan, että olen tehnyt itse
# tämän tehtävän ja vain yllä mainitut henkilöt sekä lähteet ovat
# vaikuttaneet siihen yllä mainituilla tavoilla.
######################################################################
# Harjoitustyö (tavoitetaso)
# eof

import sys
import time
import numpy as np

EROTIN = ";"

class SADEDATA:
    aikaleima = None
    aikavyohyke = None
    sademaara = None

class ANALYYSIDATA:
    paivadata = None
    sadedata = None

class KAVIJADATA():
    aikaleima = None
    sademaara = None
    mustikkamaa = None
    kauppatori = None
    Hakaniemi = None
    kavijamaara = None

def lueTiedosto(oliolista, nimiT):

    oliolista.clear()

    try:
        tiedosto = open(nimiT, "r", encoding="utf-8")

        rivi = tiedosto.readline()
        rivi = tiedosto.readline()

        rivit = 0

        while (len(rivi) > 0):
            alkiot = rivi.split(EROTIN)
            sadedata = SADEDATA()
            sadedata.aikaleima = time.strptime(alkiot[0], "%Y.%m.%d %H:%M")
            sadedata.aikavyohyke = alkiot[1]
            sadedata.sademaara = float(alkiot[2][:-1])
            oliolista.append(sadedata)
            rivit += 1
            rivi = tiedosto.readline()
    
        tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(nimiT))
        sys.exit(0)
    
    print("Tiedosto '{}' luettu.".format(nimiT))
    print("Tiedostosta lisättiin {} datariviä listaan.".format(rivit))

    return oliolista

def lueTiedostoNimi():
    nimi = input("Anna luettavan tiedoston nimi: ")
    return nimi

def analysoi(analyysilista, oliolista):

    analyysilista.clear()
    sadelista = []
    paivalista = []

    sadeSumma = 0

    mahdotonAika = "1000.10.10 10:10"
    aika2 = time.strptime(mahdotonAika, "%Y.%m.%d %H:%M")

    for i in range(len(oliolista)):
        aikaRivi = oliolista[i].aikaleima
        if (aika2.tm_mday == aikaRivi.tm_mday) and (aika2.tm_mon == aikaRivi.tm_mon):
            sadeSumma += float(oliolista[i].sademaara)
        else:
            sadelista.append(sadeSumma)
            paivalista.append(aikaRivi)
            sadeSumma = float(oliolista[i].sademaara)
        aika2 = aikaRivi
    sadelista.append(sadeSumma)
    sadelista.pop(0)

    for j in range(len(paivalista)):
        analyysidata = ANALYYSIDATA()
        analyysidata.paivadata = paivalista[j]
        analyysidata.sadedata = sadelista[j]
        analyysilista.append(analyysidata)

    print("Päivittäiset summat laskettu {} päivälle.".format(len(analyysilista)))

    sadelista.clear()
    paivalista.clear()

    return analyysilista

def dataKategoreoitavaksi(analyysilista):
    sadelista = []
    for tiedot in analyysilista:
        sadelista.append(tiedot.sadedata)
    kategoriat = maaraaKategoria(sadelista)

    sadelista.clear()
    print("Päivät kategorisoitu 4 kategoriaan.")
    return kategoriat

def maaraaKategoria(sadelista):

    kategoriat = [0, 0, 0, 0]

    for tiedot in sadelista:
        if (tiedot >= 4.5):
            kategoriat[0] += 1
        elif (4.5 > tiedot >= 1.0):
            kategoriat[1] += 1
        elif (1.0 > tiedot >= 0.3):
            kategoriat[2] += 1
        elif (0.3 > tiedot >= 0):
            kategoriat[3] += 1

    return kategoriat

def kirjoitaTiedosto(analyysilista, nimiT, kategoriat):

    try:
        tiedosto = open(nimiT, "w", encoding="utf-8")

        tiedosto.write(str("Kategoria;Päivien lukumäärä:\n"))
        for i in range(0, 4):
            tiedosto.write("Kategoria " + str(i+1) + ";" + str(kategoriat[i]) + "\n")

        tiedosto.write(str("\n"))
        tiedosto.write(str("Kaikki päivittäiset sademäärät:\n"))
        tiedosto.write(str("Pvm;mm\n"))

        for tiedot in (analyysilista):
            luettavaAika = time.strftime("%d.%m.%Y", tiedot.paivadata)
            tiedosto.write(str("{};{:.1f}\n".format(luettavaAika, tiedot.sadedata))) 

        print("Tiedosto '{}' kirjoitettu.".format(nimiT))

        tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(nimiT))
        sys.exit(0)
    return None

def kirjoitaTiedostoNimi():
    nimi = input("Anna kirjoitettavan tiedoston nimi: ")
    return nimi

def viikonpaivittainen(oliolista, analyysilista, nimiT):
    viikonpaivat = [0, 0, 0, 0, 0, 0, 0]
    for tiedot in analyysilista:
        data = tiedot.paivadata
        viikonpaivat[data.tm_wday] = viikonpaivat[data.tm_wday] + tiedot.sadedata

    kirjoitaTiedostoWday(viikonpaivat, nimiT)

    viikonpaivat.clear()

    return None

def kirjoitaTiedostoWday(viikonpaivat, nimiT):

    try:
        tiedosto = open(nimiT, "w", encoding="utf-8")

        tiedosto.write("Viikonpäivä;Sadekertymä\n")
        tiedosto.write("Maanantai;{:.1f}\n".format(viikonpaivat[0]))
        tiedosto.write("Tiistai;{:.1f}\n".format(viikonpaivat[1]))
        tiedosto.write("Keskiviikko;{:.1f}\n".format(viikonpaivat[2]))
        tiedosto.write("Torstai;{:.1f}\n".format(viikonpaivat[3]))
        tiedosto.write("Perjantai;{:.1f}\n".format(viikonpaivat[4]))
        tiedosto.write("Lauantai;{:.1f}\n".format(viikonpaivat[5]))
        tiedosto.write("Sunnuntai;{:.1f}\n".format(viikonpaivat[6]))

        print("Tiedosto '{}' kirjoitettu.".format(nimiT))

        tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(nimiT))
        sys.exit(0)

    return None



def lueYhdistaTiedosto(analyysilista, kavijalista, nimiT):

    try:
        tiedosto = open(nimiT, "r", encoding="utf-8")

        rivi = tiedosto.readline()
        rivi = tiedosto.readline()

        kavijamaara = 0

        while (len(rivi) > 0):
            alkiot = rivi.split(EROTIN)
            kavijadata = KAVIJADATA()
            kavijadata.aikaleima = time.strptime(alkiot[0], "%d.%m.%Y")
            kavijadata.mustikkamaa = int(alkiot[1])
            kavijadata.kauppatori = int(alkiot[2])
            kavijadata.Hakaniemi = int(alkiot[3][:-1])
            kavijamaara = kavijamaara + int(alkiot[1]) + int(alkiot[2]) + int(alkiot[3][:-1])
            aikaRivi = kavijadata.aikaleima
            for i in range(len(analyysilista)):
                paiva = analyysilista[i].paivadata
                if (paiva.tm_mday == aikaRivi.tm_mday) and (paiva.tm_mon == aikaRivi.tm_mon):
                    kavijadata.sademaara = analyysilista[i].sadedata
                    break
            kavijalista.append(kavijadata)
            rivi = tiedosto.readline()
    
        tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(nimiT))
        sys.exit(0)

    print("Tiedosto '{}' luettu.".format(nimiT))
    print("Tiedot yhdistetty, kävijämäärä on yhteensä {}.".format(kavijamaara))

    return kavijalista


def kirjoitaYhdistettyData(kavijalista, nimiT):

    try:
        tiedosto = open(nimiT, "w", encoding="utf-8")

        tiedosto.write("Pvm;Sademäärä;Mustikkamaa;Kauppatori;Hakaniemi\n")
        for items in kavijalista:
            tiedosto.write("{};{:.1f};{};{};{}\n".format(time.strftime("%d.%m.%Y", items.aikaleima), items.sademaara, items.mustikkamaa, items.kauppatori, items.Hakaniemi))

        tiedosto.close()

    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(nimiT))
        sys.exit(0)

    print("Tiedosto '{}' kirjoitettu.".format(nimiT))

    return None

def analysoiKKKavijamaara(kavijalista):

    summaMatriisi = np.zeros((12, 4), dtype=int)

    KKmatriisi = np.array([["Jan"], ["Feb"], ["Mar"], ["Apr"], ["May"], ["Jun"], ["Jul"], ["Aug"], ["Sep"], ["Oct"], ["Nov"], ["Dec"]])

    tapahtumatMaara = np.ones((12, 4), dtype=int)

    for i in range(len(kavijalista)):
        paiva = kavijalista[i].aikaleima
        kuukausi = paiva.tm_mon
        sadelista = [kavijalista[i].sademaara]
        kategoria = maaraaKategoria(sadelista)
        index = kategoria.index(1)
        if (summaMatriisi[int(kuukausi)-1][int(index)] != 0):
            tapahtumatMaara[int(kuukausi)-1][int(index)] = tapahtumatMaara[int(kuukausi)-1][int(index)] + 1
        summaMatriisi[int(kuukausi)-1][int(index)] = summaMatriisi[int(kuukausi)-1][int(index)] + kavijalista[i].mustikkamaa + kavijalista[i].Hakaniemi + kavijalista[i].kauppatori

    keskiarvoMatriisi = summaMatriisi / tapahtumatMaara

    yhdistettyMatriisi = np.concatenate((KKmatriisi, keskiarvoMatriisi), axis=1)

    print("Kuukausikohtaiset sademäärät analysoitu.")

    kirjoitaTiedostoKK(yhdistettyMatriisi)

    return None

def kirjoitaTiedostoKK(yhdistettyMatriisi):

    nimiT = kirjoitaTiedostoNimi()

    try:
        tiedosto = open(nimiT, "w", encoding="utf-8")

        tiedosto.write("Kuukausi;Kategoria 1;Kategoria 2;Kategoria 3;Kategoria 4\n")

        for i in range(len(yhdistettyMatriisi)):
            tiedosto.write(yhdistettyMatriisi[i][0])
            for j in range(len(yhdistettyMatriisi[0])-1):
                toFloat = float(yhdistettyMatriisi[i][j+1])
                tiedosto.write(";{:.1f}".format(toFloat))
            tiedosto.write("\n")
        tiedosto.close()
    except OSError:
        print("Tiedoston '{}' käsittelyssä virhe, lopetetaan.".format(nimiT))
        sys.exit(0)

    print("Tiedosto '{}' kirjoitettu.".format(nimiT))

    return None

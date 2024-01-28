
import HTTavoiteKirjasto

def valikko():
    print("Valitse haluamasi toiminto:")
    print("1) Lue tiedosto")
    print("2) Analysoi")
    print("3) Kirjoita tiedosto")
    print("4) Analysoi viikonpäivittäiset sademäärät")
    print("5) Lue ja yhdistä Korkeasaari tiedosto")
    print("6) Kirjoita yhdistetty data tiedostoon")
    print("7) Analysoi viikoittaiset kävijämäärät")
    print("0) Lopeta")
    
    valinta = input("Anna valintasi: ")
    try:
        valinta = int(valinta)
    except ValueError:
        print("Syötteen muuttaminen numeroksi ei onnistunut.")
    return valinta

def paaohjelma():
    valinta = valikko()

    oliolista = []
    analyysilista = []
    kavijalista = []

    while valinta != 0:
        if valinta == 1:
            nimiT = HTTavoiteKirjasto.lueTiedostoNimi()
            oliolista = HTTavoiteKirjasto.lueTiedosto(oliolista, nimiT)
            print()
            valinta = valikko()
        elif valinta == 2:
            if len(oliolista) == 0:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.")
            else:
                analyysilista = HTTavoiteKirjasto.analysoi(analyysilista, oliolista)
                kategoriat = HTTavoiteKirjasto.dataKategoreoitavaksi(analyysilista)
            print()
            valinta = valikko()
        elif valinta == 3:
            if len(analyysilista) == 0:
                print("Ei tietoja tallennettavaksi, analysoi tiedot ennen tallennusta.")
            else:
                nimiT = HTTavoiteKirjasto.kirjoitaTiedostoNimi()
                HTTavoiteKirjasto.kirjoitaTiedosto(analyysilista, nimiT, kategoriat)
            print()
            valinta = valikko()
        elif valinta == 4:
            if len(oliolista) == 0:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.")
            else:
                nimiT = HTTavoiteKirjasto.kirjoitaTiedostoNimi()
                HTTavoiteKirjasto.viikonpaivittainen(oliolista, analyysilista, nimiT)
            print()
            valinta = valikko()
        elif valinta == 5:
            if len(oliolista) == 0:
                print("Lue sademäärät ennen kävijämäärätietoja.")
            else:
                nimiT = HTTavoiteKirjasto.lueTiedostoNimi()
                kavijalista = HTTavoiteKirjasto.lueYhdistaTiedosto(analyysilista, kavijalista, nimiT)
            print()
            valinta = valikko()
        elif valinta == 6:
            if len(oliolista) == 0:
                print("Ei tietoja tallennettavaksi, analysoi tiedot ennen tallennusta.")
            else:
                nimiT = HTTavoiteKirjasto.kirjoitaTiedostoNimi()
                HTTavoiteKirjasto.kirjoitaYhdistettyData(kavijalista, nimiT)
            print()
            valinta = valikko()
        elif valinta == 7:
            if len(oliolista) == 0:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.")
            else:
                HTTavoiteKirjasto.analysoiKKKavijamaara(kavijalista)
            print()
            valinta = valikko()
        else:
            print("Tuntematon valinta, yritä uudestaan.")
            print()
            valinta = valikko()

    oliolista.clear()
    analyysilista.clear()
    kavijalista.clear()

    print("Lopetetaan.")
    print()
    print("Kiitos ohjelman käytöstä.")
    return None

paaohjelma()

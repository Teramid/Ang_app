def dwonload_verb_list():
    from urllib.request import urlopen
    from bs4 import BeautifulSoup

    """_summary_
    Aplikacja do tworzenia bazy danych do nauki angielskiego
    """

    html = "https://www.ang.pl/gramatyka/czasowniki-verbs/czasowniki-nieregularne"
    req = urlopen(html)

    soup = BeautifulSoup(req.read(), "html5lib")

    words = soup.find_all(class_=["ang", "pol"])
    word_list = []
    for x in words:
        word_list.append(x.get_text())
        try:
            word_list.remove("przykłady »\n\t\t\twzory odmian »")
        except:
            pass

    verb_irr = []
    for nr, word in enumerate(word_list):
        if word[0] == "p" and word[1] == "l" and word[2] == "a" and word[3] == "y":
            list = [x for x in word]
            word = "".join(x for x in list[4:])
            word_list[nr] = word
        if (nr + 1) % 4 == 0:
            verb_irr.append(
                [word_list[nr - 3], word_list[nr - 2], word_list[nr - 1], word_list[nr]]
            )

    for verb in verb_irr:
        print(verb)

    print(len(verb_irr))

    f = open("baza.txt", "w")
    for nr, verb in enumerate(verb_irr):
        nameFile = ""
        numberFile = nr + 1
        if numberFile < 10:
            nameFile = "00" + str(numberFile) + ".txt"
        elif numberFile >= 0 and numberFile < 100:
            nameFile = "0" + str(numberFile) + ".txt"
        else:
            nameFile = str(numberFile) + ".txt"
        nameFile = "baza/" + nameFile
        f = open(nameFile, "w")
        f.write("\n".join(x for x in verb))

    f.close()


from os import listdir

files = listdir("baza")
Files_Number = len(files)

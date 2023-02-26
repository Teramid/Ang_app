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
from os import system
from random import randint

files = listdir("baza")
Files_Number = len(files)
dict = {}
for nr, x in enumerate(files):
    file_name = "baza/" + x
    f = open(file_name, "r")
    f = f.readlines()
    dict.update(
        {nr: [f[0].rstrip(), f[1].rstrip(), f[2].rstrip(), f[3], file_name[5:]]}
    )


dictNumber = {}
for i in range(1, Files_Number + 1):
    dictNumber.update({i: 1})

full_Answer = 0
while True:
    system("cls")
    if full_Answer == Files_Number:
        print("Po nauce czas na piwo :)")
        break
    else:
        choose_File = int(randint(1, Files_Number))
        if dictNumber.get(choose_File) == 0:
            continue
        else:
            print("Ilosć pytań w bazie:", str(Files_Number))
            print("Przyswojone pytania: ", full_Answer, "/", Files_Number)
            print("Pytanie:", dict[choose_File][4])
            print("pozostałych powtórzeń pytania:", dictNumber.get(choose_File))
            print("")
            print("Czasownik:", dict[choose_File][3])
            Iform = input("I Forma: ")
            if Iform == dict[choose_File][0]:
                print("Correct")
            else:
                print("Uncorrect, should be: ", dict[choose_File][0])
            IIform = input("II Forma: ")
            if IIform == dict[choose_File][1]:
                print("Correct")
            else:
                print("Uncorrect, should be: ", dict[choose_File][1])
            IIIform = input("III Forma: ")
            if IIIform == dict[choose_File][2]:
                print("Correct")
            else:
                print("Uncorrect, should be: ", dict[choose_File][2])
            x = dictNumber.get(choose_File)
            try:
                wait_press = input("Enter, aby kontynuować...")
            except:
                pass
            if (
                Iform == dict[choose_File][0]
                and IIform == dict[choose_File][1]
                and IIIform == dict[choose_File][2]
            ):
                x -= 1
            else:
                x += 2
            dictNumber.update({choose_File: x})
            if x == 0:
                full_Answer += 1
            else:
                pass

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


import os
from random import randint


def download_verb_list():
    from urllib.request import urlopen
    from bs4 import BeautifulSoup

    """_summary_
    Funkcja tworząca baze czasowników nieregularnych
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
        if not os.path.exists("baza"):
            os.makedirs("baza")
        else:
            pass
        f = open(nameFile, "w")
        f.write("\n".join(x for x in verb))
    print("Pobrano", len(verb_irr), "czasowników")
    Enter_press = input("Wciśnij enter aby kontynuować")
    f.close()


def verb_unregular_qa():
    if os.path.exists("baza") and os.path.isdir("baza"):
        pass
    else:
        print("Baza pytań nie istnieje\nJeśli chcesz pobrać wciśnij Enter")
        enter_press = input()
        download_verb_list()

    files = os.listdir("baza")
    Files_Number = len(files)
    dict = {}
    for nr, x in enumerate(files):
        file_name = "baza/" + x
        f = open(file_name, "r")
        f = f.readlines()
        dict.update(
            {nr + 1: [f[0].rstrip(), f[1].rstrip(), f[2].rstrip(), f[3], file_name[5:]]}
        )

    dictNumber = {}
    for i in range(1, Files_Number + 1):
        dictNumber.update({i: 1})
    form_name = [
        "Bezokolicznik (infinitive): ",
        "II forma (past tense): ",
        "III forma (past participle): ",
    ]
    full_Answer = 0
    while True:
        os.system("cls")
        if full_Answer == Files_Number:
            print("Po nauce czas na piwo :)")
            wait_press = input("Enter, aby wyjść...")
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
                correct_Answer = 0
                # print(len(dict[choose_File]))
                # print(dict[choose_File])
                for i in range(len(dict[choose_File]) - 2):
                    if input(form_name[i]) in dict[choose_File][i].split():
                        print("Correct")
                        correct_Answer += 1
                    else:
                        print("Uncorrect, should be: ", dict[choose_File][i])
                wait_press = input("\nEnter, aby przejść do następnego...")
                x = dictNumber.get(choose_File)
                if correct_Answer >= 3:
                    x -= 1
                else:
                    x += 2
                dictNumber.update({choose_File: x})
                if x == 0:
                    full_Answer += 1
                else:
                    pass


from kivy.config import Config
from kivy.core.window import Window

Window.size = (450, 800)
Config.set("graphics", "resizable", False)


class Main(FloatLayout):
    pass


class MainApp(App):
    def build(self):
        return Main()


if __name__ == "__main__":
    MainApp().run()

from settings import *


class GameState:
    def __init__(self):
        self.obecny_stan = STAN_MENU
        self.lang = 'pl'

        self.jajka_w_zapytaniu = 4
        self.poziom_przejedzenia = 0

        self.ostatnia_figurka = -1
        self.licznik_powtorek = 0

        self.czas_do_powrotu_z_biedronki = 0
        self.aktualna_figurka = -1

        self.klikniecia_w_zabawke = []
        self.czas_konca_animacji = 0

        self.rundy_tutoriala = 0
        self.wiadomosc_sklep = ""
        self.nowe_jajka = 4

        self.polka = [[-1 for _ in range(5)] for _ in range(5)]

    def czy_wygrana(self):
        for wiersz in self.polka:
            for slot in wiersz:
                if slot == -1:
                    return False
        return True
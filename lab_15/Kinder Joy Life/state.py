class GameState:
    def __init__(self):
        from settings import STAN_MENU

        self.obecny_stan = STAN_MENU
        self.jajka_w_zapytaniu = 4
        self.poziom_przejedzenia = 0
        self.licznik_alex = 0
        self.czas_do_powrotu_z_biedronki = 0
        self.aktualna_figurka = -1

        self.polka = [
            [-1, -1, -1],
            [-1, -1, -1]
        ]

    def czy_wygrana(self):
        for wiersz in self.polka:
            for slot in wiersz:
                if slot == -1:
                    return False
        return True
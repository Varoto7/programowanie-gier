import pyray as pr
import random
import time

from settings import *
from state import GameState


def main():
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Kinder Joy Minecraft Simulator")
    pr.set_target_fps(FPS)

    gra = GameState()

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        mysz = pr.get_mouse_position()

        if gra.obecny_stan == STAN_MENU:
            pr.draw_text("Kinder Joy Minecraft Simulator", 150, 200, 30, pr.BLACK)
            przycisk_start = pr.Rectangle(300, 300, 200, 50)
            pr.draw_rectangle_rec(przycisk_start, pr.LIGHTGRAY)
            pr.draw_text("START", 360, 315, 20, pr.BLACK)

            if pr.check_collision_point_rec(mysz, przycisk_start) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA

        elif gra.obecny_stan == STAN_OTWIERANIE_JAJKA:
            pr.draw_text(f"Jajka do otwarcia: {gra.jajka_w_zapytaniu}", 20, 20, 20, pr.BLACK)
            pr.draw_text(f"Przejedzenie: {gra.poziom_przejedzenia}/100", 20, 50, 20,
                         pr.RED if gra.poziom_przejedzenia > 70 else pr.BLACK)
            pr.draw_text(f"Zlote Alexy pod rzad: {gra.licznik_alex}", 20, 80, 20, pr.GOLD)

            pr.draw_text("Twoja kolekcja:", 500, 20, 20, pr.DARKBLUE)
            for i in range(2):
                for j in range(3):
                    slot_rect = pr.Rectangle(500 + j * 80, 60 + i * 80, 70, 70)
                    pr.draw_rectangle_rec(slot_rect, pr.LIGHTGRAY)
                    pr.draw_rectangle_lines_ex(slot_rect, 2, pr.BLACK)
                    figurka = gra.polka[i][j]
                    if figurka != -1:
                        pr.draw_text(NAZWY_FIGUREK[figurka][:4], int(slot_rect.x) + 10, int(slot_rect.y) + 25, 15,
                                     pr.DARKGREEN)

            if gra.jajka_w_zapytaniu > 0:
                przycisk_otworz = pr.Rectangle(300, 250, 200, 80)
                pr.draw_rectangle_rec(przycisk_otworz, pr.ORANGE)
                pr.draw_text("OTWORZ JAJKO", 320, 280, 20, pr.WHITE)

                if pr.check_collision_point_rec(mysz, przycisk_otworz) and pr.is_mouse_button_pressed(
                        pr.MOUSE_BUTTON_LEFT):
                    gra.jajka_w_zapytaniu -= 1
                    gra.obecny_stan = STAN_DECYZJA_CZEKOLADA
            else:
                przycisk_sklep = pr.Rectangle(250, 250, 300, 80)
                pr.draw_rectangle_rec(przycisk_sklep, pr.BLUE)
                pr.draw_text("UZUPELNIJ ZAPASY", 260, 280, 18, pr.WHITE)

                if pr.check_collision_point_rec(mysz, przycisk_sklep) and pr.is_mouse_button_pressed(
                        pr.MOUSE_BUTTON_LEFT):
                    gra.czas_do_powrotu_z_biedronki = time.time() + 5
                    gra.obecny_stan = STAN_BIEDRONKA

        elif gra.obecny_stan == STAN_DECYZJA_CZEKOLADA:
            pr.draw_text("Otworzyles jajko! Co robisz z czekolada?", 150, 150, 25, pr.BLACK)
            przycisk_zjedz = pr.Rectangle(200, 300, 150, 50)
            przycisk_wyrzuc = pr.Rectangle(450, 300, 150, 50)

            pr.draw_rectangle_rec(przycisk_zjedz, pr.BROWN)
            pr.draw_text("ZJEDZ (+20%)", 215, 315, 18, pr.WHITE)
            pr.draw_rectangle_rec(przycisk_wyrzuc, pr.DARKGRAY)
            pr.draw_text("WYRZUC DO KOSZA", 455, 315, 15, pr.WHITE)

            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                if pr.check_collision_point_rec(mysz, przycisk_zjedz):
                    gra.poziom_przejedzenia += 20
                    if gra.poziom_przejedzenia >= 100:
                        gra.obecny_stan = STAN_PRZEGRANA_BRZUCH
                    else:
                        gra.obecny_stan = STAN_DECYZJA_ZABAWKA
                elif pr.check_collision_point_rec(mysz, przycisk_wyrzuc):
                    gra.obecny_stan = STAN_DECYZJA_ZABAWKA


        elif gra.obecny_stan == STAN_DECYZJA_ZABAWKA:
            if gra.aktualna_figurka == -1:
                gra.aktualna_figurka = random.choices(range(7), weights=SZANSE_LOSOWANIA)[0]
                if gra.aktualna_figurka == 6:
                    gra.licznik_alex += 1
                    if gra.licznik_alex >= 3:
                        gra.obecny_stan = STAN_PRZEGRANA_ALEX
                else:
                    gra.licznik_alex = 0

            if gra.obecny_stan == STAN_PRZEGRANA_ALEX:
                continue

            pr.draw_text(f"Wylosowales: {NAZWY_FIGUREK[gra.aktualna_figurka]}!", 250, 100, 25,
                         pr.GOLD if gra.aktualna_figurka == 6 else pr.BLACK)
            pr.draw_text("Kliknij na puste miejsce na polce, aby ja odlozyc", 150, 150, 20, pr.DARKGRAY)

            przycisk_zniszcz = pr.Rectangle(300, 450, 200, 50)
            pr.draw_rectangle_rec(przycisk_zniszcz, pr.RED)
            pr.draw_text("ZNISZCZ ZE ZLOSCI", 310, 465, 18, pr.WHITE)

            for i in range(2):
                for j in range(3):
                    slot_rect = pr.Rectangle(280 + j * 80, 250 + i * 80, 70, 70)
                    pr.draw_rectangle_rec(slot_rect, pr.LIGHTGRAY)
                    pr.draw_rectangle_lines_ex(slot_rect, 2, pr.BLACK)

                    figurka = gra.polka[i][j]
                    if figurka != -1:
                        pr.draw_text(NAZWY_FIGUREK[figurka][:4], int(slot_rect.x) + 10, int(slot_rect.y) + 25, 15,
                                     pr.DARKGREEN)
                    else:
                        if pr.check_collision_point_rec(mysz, slot_rect) and pr.is_mouse_button_pressed(
                                pr.MOUSE_BUTTON_LEFT):
                            if gra.aktualna_figurka != 6:
                                gra.polka[i][j] = gra.aktualna_figurka
                            gra.aktualna_figurka = -1
                            if gra.czy_wygrana():
                                gra.obecny_stan = STAN_WYGRANA
                            else:
                                gra.obecny_stan = STAN_OTWIERANIE_JAJKA

            if pr.check_collision_point_rec(mysz, przycisk_zniszcz) and pr.is_mouse_button_pressed(
                    pr.MOUSE_BUTTON_LEFT):
                gra.aktualna_figurka = -1
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA

        elif gra.obecny_stan == STAN_BIEDRONKA:
            pozostalo = int(gra.czas_do_powrotu_z_biedronki - time.time())
            pr.draw_text("Podroz do Biedronki...", 250, 250, 30, pr.DARKBLUE)
            pr.draw_text(f"Powrot za: {pozostalo} s", 320, 300, 20, pr.BLACK)

            if pozostalo <= 0:
                gra.jajka_w_zapytaniu = 4
                if gra.poziom_przejedzenia > 0:
                    gra.poziom_przejedzenia -= 10
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA


        elif gra.obecny_stan == STAN_WYGRANA:
            pr.draw_text("ZWYCIESTWO!", 300, 250, 40, pr.GREEN)
            pr.draw_text("Polska zostala zapelniona!", 250, 300, 25, pr.BLACK)

        elif gra.obecny_stan == STAN_PRZEGRANA_BRZUCH:
            pr.draw_text("GAME OVER", 300, 250, 40, pr.RED)
            pr.draw_text("Bol brzucha z przejedzenia!", 250, 300, 25, pr.BLACK)

        elif gra.obecny_stan == STAN_PRZEGRANA_ALEX:
            pr.draw_text("GAME OVER", 300, 250, 40, pr.RED)
            pr.draw_text("3 Zlote Alexy pod rzad... Wscieklosc!", 180, 300, 25, pr.BLACK)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
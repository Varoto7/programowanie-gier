import pyray as pr
import random
import time

from settings import *
from state import GameState
from graphics import *


def main():
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Kinder Joy Simulator Minecraft Edition")
    pr.set_target_fps(FPS)
    gra = GameState()

    while not pr.window_should_close():
        pr.begin_drawing()
        draw_clouds(time.time())
        mysz = pr.get_mouse_position()
        lang = gra.lang


        if gra.obecny_stan == STAN_MENU:
            pr.draw_rectangle(150, 100, 500, 150, pr.Color(255, 255, 255, 200))

            tytul_w = pr.measure_text(T[lang]['title'], 30)
            sub_w = pr.measure_text(T[lang]['subtitle'], 25)
            pr.draw_text(T[lang]['title'], 400 - tytul_w // 2, 120, 30, pr.RED)
            pr.draw_text(T[lang]['subtitle'], 400 - sub_w // 2, 160, 25, pr.DARKGRAY)

            btn_pl = pr.Rectangle(240, 280, 140, 40)
            btn_en = pr.Rectangle(420, 280, 140, 40)

            pr.draw_rectangle_rec(btn_pl, pr.GREEN if lang == 'pl' else pr.LIGHTGRAY)
            pr.draw_text("POLSKI", 270, 290, 20, pr.WHITE if lang == 'pl' else pr.DARKGRAY)

            pr.draw_rectangle_rec(btn_en, pr.GREEN if lang == 'en' else pr.LIGHTGRAY)
            pr.draw_text("ENGLISH", 445, 290, 20, pr.WHITE if lang == 'en' else pr.DARKGRAY)

            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                if pr.check_collision_point_rec(mysz, btn_pl): gra.lang = 'pl'
                if pr.check_collision_point_rec(mysz, btn_en): gra.lang = 'en'


            przycisk_start = pr.Rectangle(300, 380, 200, 50)
            pr.draw_rectangle_rec(przycisk_start, pr.BLUE)
            start_w = pr.measure_text(T[lang]['start'], 20)
            pr.draw_text(T[lang]['start'], 400 - start_w // 2, 395, 20, pr.WHITE)

            if pr.check_collision_point_rec(mysz, przycisk_start) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA


        def rysuj_szafke():
            pr.draw_rectangle(400, 250, 380, 330, pr.BROWN)
            for i in range(5):
                for j in range(5):
                    slot_rect = pr.Rectangle(415 + j * 70, 265 + i * 62, 60, 55)
                    pr.draw_rectangle_rec(slot_rect, pr.Color(139, 69, 19, 255))
                    pr.draw_rectangle_lines_ex(slot_rect, 2, pr.BLACK)

                    figurka = gra.polka[i][j]
                    if figurka != -1:
                        draw_minecraft_figure(int(slot_rect.x) + 15, int(slot_rect.y) + 5, figurka, scale=3)
                    else:
                        if gra.obecny_stan == STAN_DECYZJA_ZABAWKA and pr.check_collision_point_rec(mysz,
                                                                                                    slot_rect) and pr.is_mouse_button_pressed(
                                pr.MOUSE_BUTTON_LEFT):
                            return (i, j)
            return None


        if gra.obecny_stan == STAN_OTWIERANIE_JAJKA:
            pr.draw_text(T[lang]['collection'], 410, 220, 20, pr.WHITE)
            rysuj_szafke()

            pr.draw_text(f"{T[lang]['eggs_left']} {gra.jajka_w_zapytaniu}", 20, 20, 20, pr.BLACK)

            if gra.jajka_w_zapytaniu > 0:
                draw_kinder_egg(200, 250, 150, 200, "zamkniete")
                przycisk_otworz = pr.Rectangle(125, 150, 150, 200)

                txt_open = T[lang]['click_open']
                pr.draw_text(txt_open, 200 - pr.measure_text(txt_open, 20) // 2, 400, 20, pr.DARKGRAY)

                if pr.check_collision_point_rec(mysz, przycisk_otworz) and pr.is_mouse_button_pressed(
                        pr.MOUSE_BUTTON_LEFT):
                    gra.jajka_w_zapytaniu -= 1
                    gra.obecny_stan = STAN_DECYZJA_CZEKOLADA
            else:
                przycisk_sklep = pr.Rectangle(50, 250, 300, 80)
                pr.draw_rectangle_rec(przycisk_sklep, pr.BLUE)

                txt_sklep = T[lang]['go_shop']
                pr.draw_text(txt_sklep, 200 - pr.measure_text(txt_sklep, 18) // 2, 280, 18, pr.WHITE)

                if pr.check_collision_point_rec(mysz, przycisk_sklep) and pr.is_mouse_button_pressed(
                        pr.MOUSE_BUTTON_LEFT):
                    gra.czas_do_powrotu_z_biedronki = time.time() + 5
                    gra.obecny_stan = STAN_BIEDRONKA


        elif gra.obecny_stan == STAN_DECYZJA_CZEKOLADA:
            txt_co = T[lang]['what_to_do']
            pr.draw_text(txt_co, 400 - pr.measure_text(txt_co, 25) // 2, 100, 25, pr.BLACK)

            draw_kinder_egg(400, 230, 120, 160, "czekolada")

            przycisk_zjedz = pr.Rectangle(200, 350, 150, 50)
            przycisk_wyrzuc = pr.Rectangle(450, 350, 150, 50)

            pr.draw_rectangle_rec(przycisk_zjedz, pr.BROWN)
            pr.draw_text(T[lang]['eat'], 275 - pr.measure_text(T[lang]['eat'], 18) // 2, 365, 18, pr.WHITE)

            pr.draw_rectangle_rec(przycisk_wyrzuc, pr.DARKGRAY)
            pr.draw_text(T[lang]['trash_action'], 525 - pr.measure_text(T[lang]['trash_action'], 15) // 2, 365, 15,
                         pr.WHITE)

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
                gra.aktualna_figurka = random.choices(range(len(NAZWY_FIGUREK)), weights=SZANSE_LOSOWANIA)[0]
                if gra.aktualna_figurka == gra.ostatnia_figurka:
                    gra.licznik_powtorek += 1
                else:
                    gra.licznik_powtorek = 1
                    gra.ostatnia_figurka = gra.aktualna_figurka

                if gra.licznik_powtorek >= 3:
                    gra.obecny_stan = STAN_PRZEGRANA_POWTORKI
                    continue

            draw_kinder_egg(150, 150, 80, 100, "zabawka")
            draw_minecraft_figure(200, 100, gra.aktualna_figurka, scale=8)

            nazwa_figury = NAZWY_FIGUREK[gra.aktualna_figurka]
            szerokosc_tekstu = pr.measure_text(nazwa_figury, 20)
            pr.draw_rectangle(230 - szerokosc_tekstu // 2, 50, szerokosc_tekstu + 20, 30, pr.Color(240, 240, 240, 255))
            pr.draw_rectangle_lines(230 - szerokosc_tekstu // 2, 50, szerokosc_tekstu + 20, 30, pr.BLACK)
            pr.draw_text(nazwa_figury, 240 - szerokosc_tekstu // 2, 55, 20, pr.BLACK)

            hitbox_zabawki = pr.Rectangle(200, 100, 100, 160)
            if pr.check_collision_point_rec(mysz, hitbox_zabawki) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                obecny_czas = time.time()
                gra.klikniecia_w_zabawke = [t for t in gra.klikniecia_w_zabawke if obecny_czas - t < 1.0]
                gra.klikniecia_w_zabawke.append(obecny_czas)
                if len(gra.klikniecia_w_zabawke) >= 3:
                    gra.obecny_stan = STAN_ANIMACJA_ZNISZCZENIA
                    gra.czas_konca_animacji = obecny_czas + 5.0
                    gra.rundy_tutoriala += 1

            klikniety_slot = rysuj_szafke()
            if klikniety_slot is not None:
                i, j = klikniety_slot
                gra.polka[i][j] = gra.aktualna_figurka
                gra.aktualna_figurka = -1
                gra.rundy_tutoriala += 1
                if gra.czy_wygrana():
                    gra.obecny_stan = STAN_WYGRANA
                else:
                    gra.obecny_stan = STAN_OTWIERANIE_JAJKA

            draw_trash_can(150, 450, T[lang]['trash'])
            kosz_rect = pr.Rectangle(150, 450, 60, 80)

            if pr.check_collision_point_rec(mysz, kosz_rect) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                gra.aktualna_figurka = -1
                gra.rundy_tutoriala += 1
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA

            if gra.rundy_tutoriala < 3:
                txt1 = T[lang]['tutorial_1']
                txt2 = T[lang]['tutorial_2']
                pr.draw_text(txt1, 180 - pr.measure_text(txt1, 18) // 2, 300, 18, pr.DARKGRAY)
                pr.draw_text(txt2, 180 - pr.measure_text(txt2, 15) // 2, 330, 15, pr.RED)


        elif gra.obecny_stan == STAN_ANIMACJA_ZNISZCZENIA:
            draw_explosion_effect(400, 200, 60)
            txt_smash = T[lang]['smashed']
            txt_skip = T[lang]['skip']
            pr.draw_text(txt_smash, 400 - pr.measure_text(txt_smash, 30) // 2, 300, 30, pr.RED)
            pr.draw_text(txt_skip, 400 - pr.measure_text(txt_skip, 15) // 2, 340, 15, pr.DARKGRAY)

            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT): gra.czas_konca_animacji = 0

            if time.time() > gra.czas_konca_animacji:
                gra.aktualna_figurka = -1
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA


        elif gra.obecny_stan == STAN_BIEDRONKA:
            pozostalo = gra.czas_do_powrotu_z_biedronki - time.time()
            txt_travel = T[lang]['traveling']
            pr.draw_text(txt_travel, 400 - pr.measure_text(txt_travel, 30) // 2, 100, 30, pr.DARKBLUE)

            draw_biedronka_anim(pozostalo, T[lang]['shop_name'])

            if pozostalo <= 0:
                if random.random() < 0.33:
                    id_zdarzenia = random.randint(1, 4)
                    if id_zdarzenia == 1:
                        gra.nowe_jajka = 8
                        gra.wiadomosc_sklep = T[lang]['event_1']
                    elif id_zdarzenia == 2:
                        gra.nowe_jajka = 2
                        gra.wiadomosc_sklep = T[lang]['event_2']
                    elif id_zdarzenia == 3:
                        gra.nowe_jajka = 0
                        gra.wiadomosc_sklep = T[lang]['event_3']
                    elif id_zdarzenia == 4:
                        gra.nowe_jajka = 0
                        gra.wiadomosc_sklep = T[lang]['event_4']
                    gra.obecny_stan = STAN_ZDARZENIE_SKLEP
                else:
                    gra.jajka_w_zapytaniu = 4
                    if gra.poziom_przejedzenia > 0: gra.poziom_przejedzenia -= 10
                    gra.obecny_stan = STAN_OTWIERANIE_JAJKA


        elif gra.obecny_stan == STAN_ZDARZENIE_SKLEP:
            pr.draw_rectangle(150, 200, 500, 200, pr.Color(255, 255, 255, 230))

            szer = pr.measure_text(gra.wiadomosc_sklep, 20)
            pr.draw_text(gra.wiadomosc_sklep, 400 - szer // 2, 250, 20, pr.BLACK)

            przycisk_ok = pr.Rectangle(300, 320, 200, 50)
            pr.draw_rectangle_rec(przycisk_ok, pr.BLUE)

            szer_ok = pr.measure_text(T[lang]['understood'], 20)
            pr.draw_text(T[lang]['understood'], 400 - szer_ok // 2, 335, 20, pr.WHITE)

            if pr.check_collision_point_rec(mysz, przycisk_ok) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                gra.jajka_w_zapytaniu = gra.nowe_jajka
                if gra.poziom_przejedzenia > 0: gra.poziom_przejedzenia -= 10
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA


        elif gra.obecny_stan == STAN_WYGRANA:
            pr.draw_rectangle(150, 200, 500, 150, pr.Color(255, 255, 255, 220))
            pr.draw_text(T[lang]['victory'], 400 - pr.measure_text(T[lang]['victory'], 40) // 2, 220, 40, pr.GREEN)
            pr.draw_text(T[lang]['shelf_full'], 400 - pr.measure_text(T[lang]['shelf_full'], 20) // 2, 270, 20,
                         pr.BLACK)

            pr.draw_text(T[lang]['screenshot'], 400 - pr.measure_text(T[lang]['screenshot'], 15) // 2, 310, 15,
                         pr.DARKBLUE)

        elif gra.obecny_stan == STAN_PRZEGRANA_BRZUCH:
            pr.draw_rectangle(150, 200, 500, 150, pr.Color(255, 255, 255, 220))
            pr.draw_text(T[lang]['game_over'], 400 - pr.measure_text(T[lang]['game_over'], 40) // 2, 230, 40, pr.RED)
            pr.draw_text(T[lang]['belly'], 400 - pr.measure_text(T[lang]['belly'], 25) // 2, 290, 25, pr.BLACK)

        elif gra.obecny_stan == STAN_PRZEGRANA_POWTORKI:
            pr.draw_rectangle(50, 200, 700, 150, pr.Color(255, 255, 255, 230))
            pr.draw_text(T[lang]['game_over'], 400 - pr.measure_text(T[lang]['game_over'], 40) // 2, 230, 40, pr.RED)
            pr.draw_text(T[lang]['dupes'], 400 - pr.measure_text(T[lang]['dupes'], 30) // 2, 290, 30, pr.BLACK)

        pr.end_drawing()
    pr.close_window()


if __name__ == "__main__":
    main()
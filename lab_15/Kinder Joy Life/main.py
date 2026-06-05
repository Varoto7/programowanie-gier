import pyray as pr
import random
import time

from settings import *
from state import GameState
from graphics import *


def main():
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Kinder Joy Simulator Minecraft Edition")
    pr.set_target_fps(FPS)

    pr.init_audio_device()
    try:
        muzyka = pr.load_music_stream("362755_Minecraft_Forest_3.mp3")
        pr.play_music_stream(muzyka)
    except Exception:
        pass

    gra = GameState()

    while not pr.window_should_close():
        try:
            pr.update_music_stream(muzyka)
        except Exception:
            pass

        pr.begin_drawing()
        draw_sky(time.time())
        mysz = pr.get_mouse_position()
        lang = gra.lang

        btn_mute = pr.Rectangle(740, 20, 40, 40)
        draw_mute_button(740, 20, not gra.muzyka_gra)

        if pr.check_collision_point_rec(mysz, btn_mute) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
            gra.muzyka_gra = not gra.muzyka_gra
            try:
                pr.set_music_volume(muzyka, 1.0 if gra.muzyka_gra else 0.0)
            except Exception:
                pass

        if gra.obecny_stan == STAN_MENU:
            pr.draw_rectangle(150, 100, 500, 150, pr.Color(255, 255, 255, 200))

            tytul_w = pr.measure_text(T[lang]['title'], 36)
            sub_w = pr.measure_text(T[lang]['subtitle'], 28)
            pr.draw_text(T[lang]['title'], 400 - tytul_w // 2, 120, 36, pr.RED)
            pr.draw_text(T[lang]['subtitle'], 400 - sub_w // 2, 165, 28, pr.DARKGRAY)

            btn_pl = pr.Rectangle(240, 280, 140, 40)
            btn_en = pr.Rectangle(420, 280, 140, 40)

            pr.draw_rectangle_rec(btn_pl, pr.GREEN if lang == 'pl' else pr.LIGHTGRAY)
            pr.draw_text("POLSKI", 265, 290, 24, pr.WHITE if lang == 'pl' else pr.DARKGRAY)

            pr.draw_rectangle_rec(btn_en, pr.GREEN if lang == 'en' else pr.LIGHTGRAY)
            pr.draw_text("ENGLISH", 440, 290, 24, pr.WHITE if lang == 'en' else pr.DARKGRAY)

            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                if pr.check_collision_point_rec(mysz, btn_pl): gra.lang = 'pl'
                if pr.check_collision_point_rec(mysz, btn_en): gra.lang = 'en'

            przycisk_start = pr.Rectangle(300, 380, 200, 50)
            pr.draw_rectangle_rec(przycisk_start, pr.BLUE)
            start_w = pr.measure_text(T[lang]['start'], 24)
            pr.draw_text(T[lang]['start'], 400 - start_w // 2, 393, 24, pr.WHITE)

            if pr.check_collision_point_rec(mysz, przycisk_start) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA

        def obsluz_interakcje_szafki(srodek_x, srodek_y, tryb_interaktywny=True):
            pr.draw_rectangle(srodek_x - 190, srodek_y - 165, 380, 330, pr.BROWN)
            klikniety = None

            for i in range(5):
                for j in range(5):
                    slot_rect = pr.Rectangle((srodek_x - 175) + j * 70, (srodek_y - 150) + i * 62, 60, 55)
                    pr.draw_rectangle_rec(slot_rect, pr.Color(139, 69, 19, 255))

                    if gra.wybrany_slot == (i, j):
                        pr.draw_rectangle_lines_ex(slot_rect, 3, pr.YELLOW)
                    else:
                        pr.draw_rectangle_lines_ex(slot_rect, 2, pr.BLACK)

                    figurka = gra.polka[i][j]
                    if figurka != -1:
                        draw_minecraft_figure(int(slot_rect.x) + 15, int(slot_rect.y) + 5, figurka, scale=3)

                    if tryb_interaktywny and pr.check_collision_point_rec(mysz,
                                                                          slot_rect) and pr.is_mouse_button_pressed(
                            pr.MOUSE_BUTTON_LEFT):
                        klikniety = (i, j)

            if klikniety is not None:
                i, j = klikniety
                obecny_czas = time.time()

                if (i, j) not in gra.klikniecia_w_polke:
                    gra.klikniecia_w_polke[(i, j)] = []
                gra.klikniecia_w_polke[(i, j)] = [t for t in gra.klikniecia_w_polke[(i, j)] if obecny_czas - t < 1.0]
                gra.klikniecia_w_polke[(i, j)].append(obecny_czas)

                if len(gra.klikniecia_w_polke[(i, j)]) >= 3 and gra.polka[i][j] != -1:
                    gra.polka[i][j] = -1
                    gra.klikniecia_w_polke[(i, j)] = []
                    gra.wybrany_slot = None
                    gra.stan_przed_animacja = gra.obecny_stan
                    gra.obecny_stan = STAN_ANIMACJA_ZNISZCZENIA
                    gra.czas_konca_animacji = obecny_czas + 1.5
                else:
                    if gra.wybrany_slot is None:
                        if gra.polka[i][
                            j] == -1 and gra.obecny_stan == STAN_DECYZJA_ZABAWKA and gra.aktualna_figurka != -1:
                            gra.polka[i][j] = gra.aktualna_figurka
                            gra.aktualna_figurka = -1
                            gra.rundy_tutoriala += 1
                            if gra.czy_wygrana() and not gra.kontynuuje_po_wygranej:
                                gra.obecny_stan = STAN_WYGRANA
                            else:
                                gra.obecny_stan = STAN_OTWIERANIE_JAJKA
                        elif gra.polka[i][j] != -1:
                            gra.wybrany_slot = (i, j)
                    else:
                        wi, wj = gra.wybrany_slot
                        temp = gra.polka[i][j]
                        gra.polka[i][j] = gra.polka[wi][wj]
                        gra.polka[wi][wj] = temp
                        gra.wybrany_slot = None

        if gra.obecny_stan == STAN_OTWIERANIE_JAJKA:
            pr.draw_text(T[lang]['collection'], 410, 50, 24, pr.WHITE)
            obsluz_interakcje_szafki(590, 250)

            pr.draw_text(f"{T[lang]['eggs_left']} {gra.jajka_w_zapytaniu}", 20, 20, 24, pr.BLACK)

            if gra.jajka_w_zapytaniu > 0:
                draw_kinder_egg(200, 250, 150, 200, "zamkniete")
                przycisk_otworz = pr.Rectangle(125, 150, 150, 200)

                txt_open = T[lang]['click_open']
                pr.draw_text(txt_open, 200 - pr.measure_text(txt_open, 22) // 2, 400, 22, pr.WHITE)

                if pr.check_collision_point_rec(mysz, przycisk_otworz) and pr.is_mouse_button_pressed(
                        pr.MOUSE_BUTTON_LEFT):
                    gra.jajka_w_zapytaniu -= 1
                    gra.obecny_stan = STAN_DECYZJA_CZEKOLADA
            else:
                przycisk_sklep = pr.Rectangle(50, 250, 300, 80)
                pr.draw_rectangle_rec(przycisk_sklep, pr.BLUE)
                txt_sklep = T[lang]['go_shop']
                pr.draw_text(txt_sklep, 200 - pr.measure_text(txt_sklep, 22) // 2, 280, 22, pr.WHITE)

                if pr.check_collision_point_rec(mysz, przycisk_sklep) and pr.is_mouse_button_pressed(
                        pr.MOUSE_BUTTON_LEFT):
                    gra.czas_do_powrotu_z_biedronki = time.time() + 5
                    gra.obecny_stan = STAN_BIEDRONKA

        elif gra.obecny_stan == STAN_DECYZJA_CZEKOLADA:
            txt_co = T[lang]['what_to_do']
            pr.draw_text(txt_co, 400 - pr.measure_text(txt_co, 28) // 2, 100, 28, pr.WHITE)

            draw_kinder_egg(400, 230, 120, 160, "czekolada")

            przycisk_zjedz = pr.Rectangle(200, 350, 150, 50)
            przycisk_wyrzuc = pr.Rectangle(450, 350, 150, 50)

            pr.draw_rectangle_rec(przycisk_zjedz, pr.BROWN)
            pr.draw_text(T[lang]['eat'], 275 - pr.measure_text(T[lang]['eat'], 22) // 2, 365, 22, pr.WHITE)

            pr.draw_rectangle_rec(przycisk_wyrzuc, pr.DARKGRAY)
            pr.draw_text(T[lang]['trash_action'], 525 - pr.measure_text(T[lang]['trash_action'], 20) // 2, 365, 20,
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
            szerokosc_tekstu = pr.measure_text(nazwa_figury, 24)
            pr.draw_rectangle(230 - szerokosc_tekstu // 2, 50, szerokosc_tekstu + 20, 35, pr.Color(240, 240, 240, 255))
            pr.draw_rectangle_lines(230 - szerokosc_tekstu // 2, 50, szerokosc_tekstu + 20, 35, pr.BLACK)
            pr.draw_text(nazwa_figury, 240 - szerokosc_tekstu // 2, 56, 24, pr.BLACK)

            hitbox_zabawki = pr.Rectangle(200, 100, 100, 160)
            if pr.check_collision_point_rec(mysz, hitbox_zabawki) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                obecny_czas = time.time()
                gra.klikniecia_w_zabawke = [t for t in gra.klikniecia_w_zabawke if obecny_czas - t < 1.0]
                gra.klikniecia_w_zabawke.append(obecny_czas)
                if len(gra.klikniecia_w_zabawke) >= 3:
                    gra.stan_przed_animacja = STAN_OTWIERANIE_JAJKA
                    gra.obecny_stan = STAN_ANIMACJA_ZNISZCZENIA
                    gra.czas_konca_animacji = obecny_czas + 5.0
                    gra.rundy_tutoriala += 1

            obsluz_interakcje_szafki(590, 250)

            draw_trash_can(150, 450, T[lang]['trash'])
            kosz_rect = pr.Rectangle(150, 450, 60, 80)

            if pr.check_collision_point_rec(mysz, kosz_rect) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                gra.aktualna_figurka = -1
                gra.rundy_tutoriala += 1
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA

            if gra.rundy_tutoriala < 3:
                txt1 = T[lang]['tutorial_1']
                txt2 = T[lang]['tutorial_2']
                txt3 = T[lang]['tutorial_3']
                pr.draw_text(txt1, 200 - pr.measure_text(txt1, 22) // 2, 280, 22, pr.WHITE)
                pr.draw_text(txt2, 200 - pr.measure_text(txt2, 18) // 2, 310, 18, pr.RED)
                pr.draw_text(txt3, 200 - pr.measure_text(txt3, 18) // 2, 330, 18, pr.RED)

        elif gra.obecny_stan == STAN_ANIMACJA_ZNISZCZENIA:
            draw_explosion_effect(400, 200, 60)
            txt_smash = T[lang]['smashed']
            txt_skip = T[lang]['skip']
            pr.draw_text(txt_smash, 400 - pr.measure_text(txt_smash, 36) // 2, 300, 36, pr.RED)
            pr.draw_text(txt_skip, 400 - pr.measure_text(txt_skip, 20) // 2, 340, 20, pr.WHITE)

            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT): gra.czas_konca_animacji = 0

            if time.time() > gra.czas_konca_animacji:
                gra.aktualna_figurka = -1
                gra.obecny_stan = gra.stan_przed_animacja

        elif gra.obecny_stan == STAN_BIEDRONKA:
            pozostalo = gra.czas_do_powrotu_z_biedronki - time.time()
            txt_travel = T[lang]['traveling']
            pr.draw_text(txt_travel, 400 - pr.measure_text(txt_travel, 36) // 2, 100, 36, pr.WHITE)

            draw_biedronka_anim(pozostalo, T[lang]['shop_name'])

            if pozostalo <= 0:
                if random.random() < 0.33:
                    id_zdarzenia = random.randint(1, 4)
                    while id_zdarzenia == gra.ostatnie_zdarzenie:
                        id_zdarzenia = random.randint(1, 4)

                    gra.ostatnie_zdarzenie = id_zdarzenia

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

            szer = pr.measure_text(gra.wiadomosc_sklep, 24)
            pr.draw_text(gra.wiadomosc_sklep, 400 - szer // 2, 250, 24, pr.BLACK)

            przycisk_ok = pr.Rectangle(300, 320, 200, 50)
            pr.draw_rectangle_rec(przycisk_ok, pr.BLUE)

            szer_ok = pr.measure_text(T[lang]['understood'], 24)
            pr.draw_text(T[lang]['understood'], 400 - szer_ok // 2, 333, 24, pr.WHITE)

            if pr.check_collision_point_rec(mysz, przycisk_ok) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                gra.jajka_w_zapytaniu = gra.nowe_jajka
                if gra.poziom_przejedzenia > 0: gra.poziom_przejedzenia -= 10
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA

        elif gra.obecny_stan == STAN_WYGRANA:
            obsluz_interakcje_szafki(400, 260, tryb_interaktywny=False)

            pr.draw_rectangle(150, 15, 500, 80, pr.Color(255, 255, 255, 220))
            pr.draw_text(T[lang]['victory'], 400 - pr.measure_text(T[lang]['victory'], 46) // 2, 20, 46, pr.GREEN)

            txt_shelf = T[lang]['shelf_full']
            pr.draw_text(txt_shelf, 400 - pr.measure_text(txt_shelf, 24) // 2, 65, 24, pr.BLACK)

            btn_kontynuuj = pr.Rectangle(250, 520, 300, 50)
            pr.draw_rectangle_rec(btn_kontynuuj, pr.BLUE)
            szer_k = pr.measure_text(T[lang]['continue_playing'], 24)
            pr.draw_text(T[lang]['continue_playing'], 400 - szer_k // 2, 533, 24, pr.WHITE)

            if pr.check_collision_point_rec(mysz, btn_kontynuuj) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                gra.kontynuuje_po_wygranej = True
                gra.obecny_stan = STAN_OTWIERANIE_JAJKA

        elif gra.obecny_stan == STAN_PRZEGRANA_BRZUCH or gra.obecny_stan == STAN_PRZEGRANA_POWTORKI:
            pr.draw_rectangle(100, 150, 600, 250, pr.Color(255, 255, 255, 220))
            pr.draw_text(T[lang]['game_over'], 400 - pr.measure_text(T[lang]['game_over'], 46) // 2, 170, 46, pr.RED)

            powod = T[lang]['belly'] if gra.obecny_stan == STAN_PRZEGRANA_BRZUCH else T[lang]['dupes']
            pr.draw_text(powod, 400 - pr.measure_text(powod, 28) // 2, 230, 28, pr.BLACK)

            btn_restart = pr.Rectangle(150, 300, 220, 50)
            btn_kolekcja = pr.Rectangle(430, 300, 220, 50)

            pr.draw_rectangle_rec(btn_restart, pr.GREEN)
            pr.draw_rectangle_rec(btn_kolekcja, pr.BLUE)

            pr.draw_text(T[lang]['play_again'], 260 - pr.measure_text(T[lang]['play_again'], 20) // 2, 315, 20,
                         pr.WHITE)
            pr.draw_text(T[lang]['view_collection'], 540 - pr.measure_text(T[lang]['view_collection'], 20) // 2, 315,
                         20, pr.WHITE)

            if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                if pr.check_collision_point_rec(mysz, btn_restart):
                    gra = GameState();
                    gra.lang = lang
                elif pr.check_collision_point_rec(mysz, btn_kolekcja):
                    gra.obecny_stan = STAN_WIDOK_KOLEKCJI

        elif gra.obecny_stan == STAN_WIDOK_KOLEKCJI:
            pr.draw_text(T[lang]['collection'], 400 - pr.measure_text(T[lang]['collection'], 36) // 2, 20, 36, pr.WHITE)
            obsluz_interakcje_szafki(400, 260, tryb_interaktywny=False)

            btn_restart = pr.Rectangle(250, 520, 300, 50)
            pr.draw_rectangle_rec(btn_restart, pr.GREEN)
            szer_r = pr.measure_text(T[lang]['play_again'], 24)
            pr.draw_text(T[lang]['play_again'], 400 - szer_r // 2, 533, 24, pr.WHITE)

            if pr.check_collision_point_rec(mysz, btn_restart) and pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
                gra = GameState();
                gra.lang = lang

        pr.end_drawing()

    try:
        pr.unload_music_stream(muzyka)
    except Exception:
        pass
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
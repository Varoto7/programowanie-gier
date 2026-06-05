import pyray as pr


def draw_clouds(czas):
    pr.clear_background(pr.Color(135, 206, 235, 255))
    for i in range(5):
        x = (czas * 20 + i * 200) % 1000 - 100
        y = 30 + (i % 3) * 80
        pr.draw_rectangle(int(x), int(y), 100, 40, pr.WHITE)
        pr.draw_rectangle(int(x + 20), int(y - 20), 60, 40, pr.WHITE)


def draw_biedronka_anim(czas_pozostaly, nazwa_sklepu):
    x_ludzika = 800 - (czas_pozostaly * 160)
    pr.draw_rectangle(600, 200, 250, 400, pr.YELLOW)
    pr.draw_rectangle(600, 400, 250, 100, pr.RED)
    pr.draw_text(nazwa_sklepu, 620, 250, 20, pr.BLACK)
    draw_minecraft_figure(int(x_ludzika), 350, 0, scale=8)


def draw_trash_can(x, y, napis_kosz):
    pr.draw_rectangle(int(x), int(y), 60, 80, pr.DARKGRAY)
    pr.draw_rectangle(int(x - 5), int(y - 10), 70, 10, pr.GRAY)
    pr.draw_rectangle(int(x + 25), int(y - 20), 10, 10, pr.GRAY)
    szer = pr.measure_text(napis_kosz, 15)
    pr.draw_text(napis_kosz, int(x + 30 - szer // 2), int(y + 35), 15, pr.WHITE)


def draw_explosion_effect(x, y, promien):
    pr.draw_circle(int(x), int(y), int(promien), pr.RED)
    pr.draw_circle(int(x), int(y), int(promien * 0.7), pr.ORANGE)
    pr.draw_circle(int(x), int(y), int(promien * 0.4), pr.YELLOW)


def draw_kinder_egg(x, y, width, height, stan="zamkniete"):
    if stan == "zamkniete":
        pr.draw_ellipse(int(x), int(y + height / 6), int(width / 2), int(height / 3), pr.RED)
        pr.draw_ellipse(int(x), int(y - height / 6), int(width / 2), int(height / 3), pr.WHITE)
        pr.draw_text("KINDER", int(x - 25), int(y - 8), 12, pr.BLACK)
        pr.draw_text("JOY", int(x - 12), int(y + 8), 15, pr.RED)
    elif stan == "czekolada":
        pr.draw_ellipse(int(x), int(y), int(width / 2), int(height / 2), pr.WHITE)
        pr.draw_ellipse(int(x), int(y), int(width / 2 - 4), int(height / 2 - 4), pr.BROWN)
        pr.draw_circle(int(x - 10), int(y), 8, pr.DARKGRAY)
        pr.draw_circle(int(x + 10), int(y + 10), 8, pr.DARKGRAY)
    elif stan == "zabawka":
        pr.draw_ellipse(int(x), int(y), int(width / 2), int(height / 2), pr.WHITE)
        pr.draw_rectangle(int(x - 20), int(y - 15), 40, 30, pr.GOLD)
        pr.draw_text("?", int(x - 5), int(y - 10), 20, pr.BLACK)


def draw_minecraft_figure(x, y, fig_id, scale=4):
    SKIN = pr.Color(255, 205, 170, 255)
    BLUE = pr.BLUE
    CYAN = pr.SKYBLUE
    GREEN = pr.GREEN
    DARK_GREEN = pr.DARKGREEN
    GOLD = pr.GOLD
    BLACK = pr.BLACK
    GRAY = pr.GRAY
    PINK = pr.Color(255, 109, 194, 255)
    PURPLE = pr.PURPLE
    WHITE = pr.WHITE

    def draw_humanoid(glowa, koszula, spodnie, wlosy=None, zbroja=False):
        pr.draw_rectangle(int(x + scale * 2), int(y), int(scale * 4), int(scale * 4), glowa)
        if wlosy: pr.draw_rectangle(int(x + scale * 2), int(y), int(scale * 4), int(scale), wlosy)
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 4), int(scale * 4), int(scale * 4), koszula)
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 8), int(scale * 4), int(scale * 4), spodnie)
        if zbroja:
            pr.draw_rectangle(int(x + scale * 1.5), int(y - scale * 0.5), int(scale * 5), int(scale * 2), koszula)
            pr.draw_rectangle(int(x + scale * 1.5), int(y + scale * 4), int(scale), int(scale * 3), koszula)

    if fig_id == 0:
        draw_humanoid(SKIN, CYAN, BLUE, pr.BROWN)
    elif fig_id == 1:
        draw_humanoid(SKIN, CYAN, CYAN, pr.BROWN, True)
    elif fig_id == 2:
        draw_humanoid(SKIN, GREEN, pr.BROWN, pr.ORANGE)
    elif fig_id == 3:
        draw_humanoid(SKIN, GOLD, GOLD, pr.ORANGE, True)
    elif fig_id == 4:
        pr.draw_rectangle(int(x + scale * 2), int(y), int(scale * 4), int(scale * 4), GREEN)
        pr.draw_rectangle(int(x + scale * 3), int(y + scale * 2), int(scale * 2), int(scale * 2), BLACK)
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 4), int(scale * 4), int(scale * 6), GREEN)
        pr.draw_rectangle(int(x + scale), int(y + scale * 10), int(scale * 2), int(scale * 2), DARK_GREEN)
        pr.draw_rectangle(int(x + scale * 5), int(y + scale * 10), int(scale * 2), int(scale * 2), DARK_GREEN)
    elif fig_id == 5:
        draw_minecraft_figure(x, y, 4, scale)
        pr.draw_rectangle_lines(int(x + scale), int(y - scale), int(scale * 6), int(scale * 14), CYAN)
    elif fig_id == 6:
        pr.draw_rectangle(int(x + scale * 3), int(y), int(scale * 2), int(scale * 2), BLACK)
        pr.draw_rectangle(int(x + scale * 3), int(y + scale // 2), int(scale), int(scale // 2), PURPLE)
        pr.draw_rectangle(int(x + scale * 3), int(y + scale * 2), int(scale * 2), int(scale * 5), BLACK)
        pr.draw_rectangle(int(x + scale * 3), int(y + scale * 7), int(scale), int(scale * 6), BLACK)
    elif fig_id == 7:
        draw_humanoid(GREEN, CYAN, BLUE)
    elif fig_id == 8:
        draw_humanoid(GRAY, GRAY, GRAY)
    elif fig_id == 9:
        pr.draw_rectangle(int(x + scale * 3), int(y), int(scale * 3), int(scale * 2), BLACK)
        pr.draw_rectangle(int(x + scale * 4), int(y + scale), int(scale), int(scale // 2), PURPLE)
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 2), int(scale * 4), int(scale * 4), BLACK)
        pr.draw_rectangle(int(x - scale), int(y + scale * 2), int(scale * 3), int(scale * 3), GRAY)
        pr.draw_rectangle(int(x + scale * 6), int(y + scale * 2), int(scale * 3), int(scale * 3), GRAY)
    elif fig_id == 10:
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 4), int(scale * 6), int(scale * 4), PINK)
        pr.draw_rectangle(int(x), int(y + scale * 2), int(scale * 3), int(scale * 3), PINK)
        pr.draw_rectangle(int(x + scale * 3), int(y + scale * 8), int(scale), int(scale * 2), PINK)
    elif fig_id == 11:
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 3), int(scale * 6), int(scale * 5), WHITE)
        pr.draw_rectangle(int(x), int(y + scale * 2), int(scale * 3), int(scale * 3), SKIN)
        pr.draw_rectangle(int(x + scale * 3), int(y + scale * 8), int(scale), int(scale * 2), SKIN)
    elif fig_id == 12:
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 6), int(scale * 4), int(scale * 3), DARK_GREEN)
        pr.draw_rectangle(int(x + scale * 1.5), int(y + scale * 5), int(scale), int(scale), GOLD)
        pr.draw_rectangle(int(x + scale * 5.5), int(y + scale * 5), int(scale), int(scale), GOLD)
    elif fig_id == 13:
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 7), int(scale * 4), int(scale * 2), PINK)
        pr.draw_rectangle(int(x + scale), int(y + scale * 6), int(scale * 2), int(scale * 2), PINK)
        pr.draw_rectangle(int(x + scale * 5), int(y + scale * 6), int(scale * 2), int(scale * 2), PINK)
    elif fig_id == 14:
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 4), int(scale * 4), int(scale * 4), PURPLE)
        pr.draw_rectangle(int(x + scale * 3), int(y + scale * 5), int(scale * 2), int(scale), BLACK)
        pr.draw_rectangle(int(x + scale * 3.5), int(y + scale * 5.5), int(scale // 2), int(scale // 2), WHITE)
    elif fig_id == 15:
        pr.draw_rectangle(int(x + scale * 2), int(y + scale * 2), int(scale * 4), int(scale * 2), CYAN)
        pr.draw_rectangle(int(x + scale * 3), int(y + scale * 2.5), int(scale * 2), int(scale), BLACK)
        pr.draw_rectangle(int(x + scale), int(y + scale * 5), int(scale * 6), int(scale * 2), CYAN)
        pr.draw_rectangle(int(x + scale * 3), int(y + scale * 8), int(scale * 2), int(scale * 2), CYAN)
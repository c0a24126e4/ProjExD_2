import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect):#-> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横、縦）
    画面内ならTrue、画面がいならFalse
    """
    yoko, tate = True, True 
    #横方向判定
    if rct.left < 0 or WIDTH < rct.right: #画面外だったら
        yoko = False
    #縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom: #画面内だったら 
        tate = False
    return (yoko, tate)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_img_left = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_img_up = pg.transform.rotozoom(pg.image.load("fig/6.png"), 0, 0.9)
    kk_img_right = pg.transform.rotozoom(pg.image.load("fig/2.png"), 0, 0.9)
    kk_img_down = pg.transform.flip(kk_img_up, False, True)
    kk_img_gameover = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    # 爆弾の拡大画像リストを作成
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    # 加速度リストを作成
    bb_accs = [a for a in range(1, 11)]

    # 爆弾の初期画像を設定
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5


    clock = pg.time.Clock()
    tmr = 0


    kk_base_img = pg.image.load("fig/3.png")  # 基本は左向き画像
    kk_gyaku_img = pg.transform.flip(kk_base_img,True,False)
    kk_imgs = {
    (0, 0): pg.transform.rotozoom(kk_base_img, 0, 0.9),  # 静止
    (0, -5): pg.transform.rotozoom(kk_base_img, -90, 0.9),  # 上
    (0, +5): pg.transform.rotozoom(kk_base_img, 90, 0.9),  # 下
    (-5, 0): pg.transform.rotozoom(kk_base_img, 0, 0.9),  # 左（デフォルト）
    (+5, 0): pg.transform.rotozoom(kk_gyaku_img, 0, 0.9),  # 右

    (-5, -5): pg.transform.rotozoom(kk_base_img, -45, 0.9),  # 左上
    (-5, +5): pg.transform.rotozoom(kk_base_img, 45, 0.9),  # 左下
    (+5, -5): pg.transform.rotozoom(kk_gyaku_img, 45, 0.9),  # 右上
    (+5, +5): pg.transform.rotozoom(kk_gyaku_img, -45, 0.9),  # 右下
}



    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            blackout = pg.Surface((WIDTH, HEIGHT))
            blackout.set_alpha(150) #半透明にする
            blackout.fill((0, 0, 0)) #surfaceを一色に塗りつぶす
            screen.blit(blackout, (0, 0))
            screen.blit(kk_img_gameover, kk_rct)
            # game over テキスト
            fonto = pg.font.Font(None,80)
            txt = fonto.render("Game Over", True, (255,255,255))
            txt_rect = txt.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(txt,txt_rect)
            # こうかとん（泣いてる）画像を左右に表示
            icon_img = pg.transform.rotozoom(kk_img_gameover, 0, 1)
            icon_w = icon_img.get_width()
            icon_h = icon_img.get_height()

            # テキストの左右にアイコンを配置
            screen.blit(icon_img, (txt_rect.left - icon_w - 10, txt_rect.centery - icon_h // 2))  # 左側
            screen.blit(icon_img, (txt_rect.right + 10, txt_rect.centery - icon_h // 2))         # 右側
            pg.display.update()
            pg.time.wait(5000)
            return


        if kk_rct.colliderect(bb_rct): #こうかとんRectと爆弾Rectが重なっていたら 
            print("Game Over")
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #左右方向
                sum_mv[1] += mv[1] #上下方法

        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_img = kk_imgs.get(tuple(sum_mv), kk_imgs[(0, 0)])
        

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): #画面の外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #画面内に戻す

        #爆弾の画像と速度を時間経過とともに更新
        bb_img = bb_imgs[min(tmr//500, 9)]
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]


        bb_rct.move_ip(avx, avy) # 加速された速度で移動


        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #左右どちらかにはみ出ていたら
            vx *= -1
        if not tate: #上下どちらかにはみ出ていたら
            vy *= -1

        screen.blit(bb_img, bb_rct) # 更新された爆弾を描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
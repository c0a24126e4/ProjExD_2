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


def check_bound(rct: pg.Rect):  # -> tuple[bool, bool]:
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
    # kk_img_down = pg.transform.rotozoom(pg.image.load("fig/4.png"), 0, 0.9)
    kk_img_down = pg.transform.flip(kk_img_up, False, True)
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
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])


        if kk_rct.colliderect(bb_rct): #こうかとんRectと爆弾Rectが重なっていたら 
            print("Game Over")
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #左右方向
                sum_mv[1] += mv[1] #上下方法
        
        
        if key_lst[pg.K_UP]: #こうかとんの向きを進行方向へ変える
            kk_img = kk_img_up
        if key_lst[pg.K_DOWN]:
            kk_img = kk_img_down
        if key_lst[pg.K_LEFT]:
            kk_img = kk_img_left
        if key_lst[pg.K_RIGHT]:
            kk_img = kk_img_right

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











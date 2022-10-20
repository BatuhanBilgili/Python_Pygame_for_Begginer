import pygame 
import os#os'u(operating systeam açılımıdır) burda  import etmemizin nedeni bir cismi,şekli,fotoğrafı yüklemek istediğimizde yolu bulsun biz uğraşmıyalım diye. 
pygame.font.init()

WIDTH,HEİGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEİGHT))
pygame.display.set_caption("Second Game!")

WHİTE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5 , 0, 10, HEİGHT)

HEALTH_FONT = pygame.font.SysFont("comicsans", 40 )
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60#burda ekran yenileme hızımızı tanımladık genelde oyunlar 60 fpsi destekler
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,40#bir ifadeyi birden fazl kullanınca böyle gene tanımlamak daha iyi oluyor.

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2# 1 verirsek aynı olurlar ondan 2 dedik

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    "Assets","spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)#pygame.transform.rotate(,90) ile 90 derece döndürmüş olduk gemiyi

RED_SPACESHIP_IMAGE = pygame.image.load(
     os.path.join("Assets","spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
    (RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)#pygame.transform.rotate(,270) ile 270 derece döndürmüş olduk gemiyi

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HEİGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_heal, yellow_healt):#maine yazmaktansa ekrana ne çizmek,yapmak istiyorsak burda uygulamamız code okunaklığı açısından daha iyi olur. 
    WIN.blit(SPACE, (0, 0))
    #WIN.fill(WHİTE)#burda renk veriyoruz pygame rgbyi destekliyor ondan yukarda renklerin sayı değeriniz yazıp uyguluyoruz,ekranı ilk beyaz yaptık ardından uzay gemisini görüntüledik yoksa diğer türlüuzay gemisini göremeyiz.
    pygame.draw.rect(WIN, BLACK, BORDER)#burda başka bir fonksiyonla ekrana gösteriyoruz.burda ekranın ortasına siyah bir çizgi çektik.
    
    red_heal_text = HEALTH_FONT.render("Health: " + str(red_heal), 1, WHİTE)
    yellow_heal_text = HEALTH_FONT.render("Health: " + str(yellow_healt), 1, WHİTE)
    WIN.blit(red_heal_text, (WIDTH - red_heal_text.get_width() - 10, 10))
    WIN.blit(yellow_heal_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))#blit fonksiyonu ekrana bir şey çıkartmak istediğimizde kullanırızyazı ve ya resim fark etmez.
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    #pygamede ekrana bir şey çıkarmak istediğmizde bunun kordinatlarını vermeliyiz fakat pygamede merkezden başlamıyoruz çizime bir şey gösterilicekse top-left sol en üstteki 0,0 dan çizime başlanır bunu unutmayın.
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW , bullet)
    
    pygame.display.update()#ekranı updaetlemezsek ekranda ne değişiklik yaparsak yapalım gözükmez


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:#Left and operatörlerini ortaya siyah çizgi çektikten sonra yaptık eklememizin amacı o siyah çizgiye gelince hareket ettiremeyelim gemiyi
            yellow.x -= VEL 
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:#Right Border.x dememizin amacı 0 deseydik geminin sol en üstü olucaktı bu ve geminin burnu siyah çizgiyi geçebilicekti.
            yellow.x += VEL 
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0 :#UP
            yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEİGHT - 15:#Down
            yellow.y += VEL  

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:#Left
            red.x -= VEL 
    if keys_pressed[pygame.K_RIGHT]and red.x + VEL + red.width < WIDTH:#Right sağa gitmesini sağladık burda 
            red.x += VEL 
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0 :#UP
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEİGHT - 15:#Down
            red.y += VEL  

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet) 

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet )
        elif bullet.x < 0:
            red_bullets.remove(bullet) 

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHİTE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEİGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_healt = 10
    yellow_healt = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)#farklı bilgisayarlarda farklı fps alıcağımızdan dolayı sabit bir fps değerine sabitlememiz gerekiyor bu yüzdende 60 fps yaptık.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() 

            if event.type == pygame.KEYDOWN:#burda bir tuşa basıcağımızı söyledik ateş etmek için sol ve sağ kontrol tuşlarını kullanıcaz.
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,yellow.y + yellow.height//2 - 2, 10, 5)#karaktterin gövdesinden gelmesini istiyoruz/2 yaptık
                    yellow_bullets.append(bullet)


                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x ,red.y + red.height// 2 - 2, 10, 5)#kırmızı karaktere genişlik eklemedik çünkü kendisi sağda ve mermiler sol en önden gelmeli sağ en arkadan değil.
                    red_bullets.append(bullet) 

            if event.type == RED_HIT:
                red_healt -= 1

            if event.type == YELLOW_HIT: 
                yellow_healt -= 1

        
        winner_text = ""
        if red_healt <= 0:
            winner_text = "Yellow Wins!"

        if yellow_healt <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()#burda yaptığımız klavye hareketleri ile gemiyi hareket ettirmek
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets,red_bullets, yellow, red )

        draw_window(red, yellow, red_bullets, yellow_bullets,
         red_healt, yellow_healt)

    main( )   

if __name__ == "__main__":
    main()    

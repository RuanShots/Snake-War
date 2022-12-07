import pygame 
from pygame.locals import *
from random import randint, choice
from sys import exit
import time
import os


main_file = os.path.dirname(__file__)
assets = os.path.join(main_file, "Assets")
sounds = os.path.join(assets, "sounds")
images = os.path.join(assets, "images")
mapas = os.path.join(images, "mapas")
sprites = os.path.join(images, "sprites")
fonts = os.path.join(assets, "fonts")
effects = os.path.join(sounds, "effects")



pygame.init()
pygame.mixer.init()


# Variáveis Principais
x = 1280
y = 720
speed_geral = 8
var = 1280
contador = 3
segundos = 0
exec = 0
cooldown = 0

# Tempos
vezes = 0
seg = 2
minutos = 59

# Lógica
pause = False
inicio = True
game = False
opt = False
pausa = False
marcador = False
tela_score = False
rodadas_maca = True
run = True



# Efeitos Sonoros
botoes = pygame.mixer.Sound(os.path.join(sounds, "pause.wav"))
final_second = pygame.mixer.Sound(os.path.join(effects, "seconds_final.wav"))
seconds = pygame.mixer.Sound(os.path.join(sounds, "seconds.wav"))
apple = pygame.mixer.Sound(os.path.join(effects, "apple.wav"))
head = pygame.mixer.Sound(os.path.join(effects, "head_with_head.wav"))
batida = pygame.mixer.Sound(os.path.join(effects, "batida.wav"))
# Musicas de Fundo
vol = 0.03
pygame.mixer.music.set_volume(vol)


# Classe menu inicial
class AddSprites():
    def __init__(self, link, x=1280, y=720):

        self.image = pygame.image.load(link)
        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()
    
    def blit(self, tela, x, y):
        tela.blit(self.image, (x, y))
    
    def on_grid_random(self):
        x = randint(20, 1240)
        y = randint(20, 680)
        return(x//10*10, y//10*10)
    
    def anime(self, tela, largura, var):
        rel_x = largura % self.image.get_rect().width
        tela.blit(self.image, (rel_x - self.image.get_rect().width, 0))
        if rel_x < var:
            tela.blit(self.image, (rel_x, 0))




# Classe da Cobras
class Snake(pygame.sprite.Sprite):
    def __init__(self, pos_inicial, up=False, down=False, left=False, right=True):
        pygame.sprite.Sprite.__init__(self)

        self.pontos = 0
        self.R = 0
        self.up = 0
        self.right = 1
        self.down = 2
        self.left = 3
        self.snake = [(pos_inicial, 300), (pos_inicial + 10, 300), (pos_inicial + 20, 300), (pos_inicial + 30, 300), (pos_inicial + 50, 300)]
        self.vida_T = len(self.snake)
        self.snake_skin = pygame.Surface((10, 10))
        
        if up == True:
            self.direction = self.up
            self.ang = 0
        
        elif down == True:
            self.direction = self.down
            self.ang = -180
        
        elif right == True:
            self.direction = self.right
            self.ang = -90
        
        elif left == True:
            self.direction = self.left
            self.ang = 90

    def vida(self, tam, x, y, tela):
        font1 = pygame.font.SysFont(os.path.join(fonts, "FANTONY-ROUGH.otf"), tam)
        vida = font1.render(f"Vida: {self.vida_T}", True, (self.R, 0, 0))
        tela.blit(vida, (x, y))

    def andar(self):
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = (self.snake[i-1][0], self.snake[i-1][1])
    
    def mudar_direct(self, nome):
        
        if self.direction == self.up:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] - 10)
            self.ang = 0
            self.nick(nome, self.snake[0][0] - 7, self.snake[0][1] - 15)
        
        elif self.direction == self.down:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] + 10)
            self.ang = 180
            self.nick(nome, self.snake[0][0] - 7, self.snake[0][1] + 15)
        
        elif self.direction == self.right:
            self.snake[0] = (self.snake[0][0] + 10, self.snake[0][1])
            self.ang = -90
            self.nick(nome, self.snake[0][0] + 15, self.snake[0][1] - 7)
        
        elif self.direction == self.left:
            self.snake[0] = (self.snake[0][0] - 10, self.snake[0][1])
            self.ang = 90
            self.nick(nome, self.snake[0][0] - 15, self.snake[0][1] - 7)
    
    def blit(self, tela):
        for pos in self.snake:
            tela.blit(self.snake_skin, pos)

    def colide(self, c1, c2):
        return (c1[0] == c2[0]) and (c1[1] == c2[1])

    def nick(self, nome, x, y):
        font2 = pygame.font.SysFont(os.path.join(fonts, "Fruit_Days.otf"), 20)
        nickname = font2.render(f"{nome}", True, (0, 0, 0))
        nickname = pygame.transform.rotate(nickname, self.ang)
        window.blit(nickname, (x, y))

    def upsup(self):
        self.vida_T += 4
        self.snake_skin.fill((randint(10, 240), randint(10, 240), randint(10, 240)))
        self.snake.append((0, 0))
    
    def update(self):
        self.vida_T += 1
        self.snake_skin.fill((randint(10, 240), randint(10, 240), randint(10, 240)))
        self.snake.append((0, 0))




# Classe da Maçã
class Itens(pygame.sprite.Sprite):
    def __init__(self, link, x=1280, y=720):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(link)
        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()
        self.pos = self.on_grid_random()
        self.sorteio = randint(0, 100)

    
    def blit(self, tela):
        tela.blit(self.image, self.pos)
    
    def on_grid_random(self):
        x = randint(20, 1240)
        y = randint(20, 680)
        return(x//10*10, y//10*10)





# Classe Caracteristicas do Game
class Game():
    def __init__(self, imagem):

        self.bg = pygame.image.load(imagem)
        self.rect = self.bg.get_rect()
    
    def imagem(self, tela, x=0, y=0):
        tela.blit(self.bg, (x, y))

# Funções de Auxilio
def contagem():
    global exec, segundos, contador, window, marcador

    fonte1 = pygame.font.SysFont(os.path.join(fonts, "Fruit_Days.otf"), 200)

    if exec == 0 and pause == False:
        
        mapa1 = fonte1.render(f"{mapa_escolhido[1]}", True, (0, 0, 0))
        mapa1_rect = mapa1.get_rect()
        tam = (1280 - mapa1_rect[2]) / 2
        mapa1_rect.topleft = (tam, 0)
        window.blit(mapa1, (mapa1_rect.topleft[0], 150))

        if segundos == 30:
            segundos = 0
            time.sleep(1)
            exec = 1
        
        else:
            segundos += 1

        if contador >= 1:
            contar = fonte1.render(f"{contador}", True, (0, 0, 0))
            contar_rect = contar.get_rect()
            contar_rect.center = (x//2, y//2)
            window.blit(contar, (contar_rect.center[0], y//2-40))

        if segundos % 10 == 0:
            seconds.play()
            contador -= 1
    
    else:
        marcador = True




def timing():
    global window, frames, seg, minutos, vezes, marcador, inicio, game, tela_score
    R = G = B = 0
    if vezes < 30:
        vezes += 1
    else:
        vezes = 0
        if seg > 0:
            seg -= 1
        else:
            seg = 59
            if minutos > 0:
                minutos -= 1
    if minutos == 0 and seg == 0:
        final_second.stop()
        time.sleep(1.5) 
        marcador = False
        tela_score = True
        game = False
    elif minutos == 0 and seg <= 10:
        final_second.play()
        pygame.mixer.music.pause()
        R = 255

    
    fonte1 = pygame.font.SysFont(os.path.join(fonts, "Fruit_Days.otf"), 50)
    relogio = fonte1.render(f"{minutos}m : {seg}s", True, (R, G, B))
    window.blit(relogio, (15, 15))
 




def mapa():
    sorteio = randint(1, 150)
    desert = Game(imagem=os.path.join(mapas, "desert.jpg"))
    desert_blur = Game(imagem=os.path.join(mapas, "desert_blur.jpg"))
    gardem = Game(imagem=os.path.join(mapas, "gardem.jpg"))
    gardem_blur = Game(imagem=os.path.join(mapas, "gardem_blur.jpg"))
    beach = Game(imagem=os.path.join(mapas, "beach.jpg"))
    beach_blur = Game(imagem=os.path.join(mapas, "beach_blur.jpg"))
    campo = Game(imagem=os.path.join(mapas, "campo.jpg"))
    campo_blur = Game(imagem=os.path.join(mapas, "campo_blur.jpg"))
    pedreira = Game(imagem=os.path.join(mapas, "pedreira.jpg"))
    pedreira_blur = Game(imagem=os.path.join(mapas, "pedreira_blur.jpg"))

    if sorteio > 0 and sorteio <= 30:
        return [gardem, "GARDEM", gardem_blur]
    
    elif sorteio > 30 and sorteio <= 60:
        return [pedreira, "STONES", pedreira_blur]
    
    elif sorteio > 60 and sorteio <= 90:
        return [desert, "DESERT", desert_blur]
    
    elif sorteio > 90 and sorteio <= 120:
        return [campo, "FOOTBALL", campo_blur]
    
    elif sorteio > 120 and sorteio <= 150:
        return [beach, "BEACH", beach_blur]




mapa_escolhido = mapa()

def game_restart():
    global exec, segundos, contador, mapa_escolhido, vezes, minutos, seg, marcador, cobra1, itens, cobra2
    mapa_escolhido = mapa()
    vezes = 0
    minutos = 2
    seg = 59
    exec = 0
    segundos = 0
    contador = 3
    marcador = False
    cobra1 = Snake(30)
    maca = Itens(os.path.join(sprites, "maçã.png"), 10, 10)
    cobra2 = Snake(x - 30, left=True, right=False)



# Game caracteristicas

window = pygame.display.set_mode((x, y))
pygame.display.set_caption("Snake War")
icone = pygame.image.load(os.path.join(images, "icone.ico"))
pygame.display.set_icon(icone)


#  Personagens
maca = Itens(os.path.join(sprites, "maçã.png"), 10, 10)
cobra1 = Snake(30)
cobra2 = Snake(x - 30, left=True, right=False)

# Loop Caracters
clock = pygame.time.Clock()


# Loop
while run:

    # Tela de inicio
    if inicio == True:

        # Sempre que voltar a tela inicial o game restarta
        game_restart()
        mouse = pygame.mouse.get_pos()

        # Fechar
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                run = False
                exit()
            
            if ev.type == MOUSEBUTTONDOWN:
                if mouse[0] >= 369 and mouse[0] <= 911 and mouse[1] >= 164 and mouse[1] <= 314:
                    botoes.play()
                    inicio = False
                    game = True
                
                elif mouse[0] >= 484 and mouse[0] <= 796 and mouse[1] >= 364 and mouse[1] <= 474:
                    botoes.play()
                    time.sleep(0.5)
                    pygame.quit()
                    exit
        


        # Background Animação
        bg = AddSprites(os.path.join(images, "tela_inicial.jpg"))
        bg.anime(window, var, 1280)



        # Botões Tela Inicial
        # Jogar
        if mouse[0] >= 369 and mouse[0] <= 911 and mouse[1] >= 164 and mouse[1] <= 314:
            jogar = AddSprites(os.path.join(sprites, "jogar.png"), 570, 180)
        else:
            jogar = AddSprites(os.path.join(sprites, "jogar.png"), 550, 160)
        
        jogar.blit(window, x//2 - (550/2), y//2 - 200)
        


        # Sair
        if mouse[0] >= 484 and mouse[0] <= 796 and mouse[1] >= 364 and mouse[1] <= 474:
            sair = AddSprites(os.path.join(sprites, "sair.png"), 340, 140)
        else:
            sair = AddSprites(os.path.join(sprites, "sair.png"), 320, 120)
        
        sair.blit(window, x//2 - (320/2), y//2)
        


        # Update
        # Animação da Tela
        var -= speed_geral
    



    # Tela de game iniciado
    if game == True:
        # Fechar
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                run = False
                exit()

            # Abrir as Configurações
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    game = False
                    pausa = True
                
                # Controles cobra1
            if ev.type == KEYDOWN:
                if ev.key == K_w:
                    if cobra1.direction == cobra1.down:
                        pass
                    elif cobra1.snake[0][0] >= 1275 or cobra1.snake[0][0] <= 0 or cobra1.snake[0][1] >= 715 or cobra1.snake[0][1] <= 0:
                        pass
                    else:
                        cobra1.direction = cobra1.up
                


                elif ev.key == K_s:
                    if cobra1.direction == cobra1.up:
                        pass
                    elif cobra1.snake[0][0] >= 1275 or cobra1.snake[0][0] <= 0 or cobra1.snake[0][1] >= 715 or cobra1.snake[0][1] <= 0:
                        pass
                    else:
                        cobra1.direction = cobra1.down
                


                elif ev.key == K_a:
                    if cobra1.direction == cobra1.right:
                        pass
                    elif cobra1.snake[0][0] >= 1275 or cobra1.snake[0][0] <= 0 or cobra1.snake[0][1] >= 715 or cobra1.snake[0][1] <= 0:
                        pass
                    else:
                        cobra1.direction = cobra1.left
                


                elif ev.key == K_d:
                    if cobra1.direction == cobra1.left:
                        pass
                    elif cobra1.snake[0][0] >= 1275 or cobra1.snake[0][0] <= 0 or cobra1.snake[0][1] >= 715 or cobra1.snake[0][1] <= 0:
                        pass
                    else:
                        cobra1.direction = cobra1.right
                


            # Controles cobra2
            if ev.type == KEYDOWN:
                if ev.key == K_UP:
                    if cobra2.direction == cobra2.down:
                        pass
                    elif cobra2.snake[0][0] >= 1275 or cobra2.snake[0][0] <= 0 or cobra2.snake[0][1] >= 715 or cobra2.snake[0][1] <= 0:
                        pass
                    else:
                        cobra2.direction = cobra2.up
                


                elif ev.key == K_DOWN:
                    if cobra2.direction == cobra2.up:
                        pass
                    elif cobra2.snake[0][0] >= 1275 or cobra2.snake[0][0] <= 0 or cobra2.snake[0][1] >= 715 or cobra2.snake[0][1] <= 0:
                        pass
                    else:
                        cobra2.direction = cobra2.down
                


                elif ev.key == K_LEFT:
                    if cobra2.direction == cobra2.right:
                        pass
                    elif cobra2.snake[0][0] >= 1275 or cobra2.snake[0][0] <= 0 or cobra2.snake[0][1] >= 715 or cobra2.snake[0][1] <= 0:
                        pass
                    else:
                        cobra2.direction = cobra2.left
                


                elif ev.key == K_RIGHT:
                    if cobra2.direction == cobra2.left:
                        pass
                    elif cobra2.snake[0][0] >= 1275 or cobra2.snake[0][0] <= 0 or cobra2.snake[0][1] >= 715 or cobra2.snake[0][1] <= 0:
                        pass
                    else:
                        cobra2.direction = cobra2.right
        


        # Mapa Escolhido
        mapa_escolhido[0].imagem(window)      


        # Texto de Entrada do Game
        contagem()


        # Temporalizador
        if marcador == True:

            timing()
    
            # Vida da Cobra 1 painel
            cobra1.vida(25, 20, 60, window)
            if cobra1.vida_T == 1:
                cobra1.R = 255
            else:
                cobra1.R = 0 
            


            # Vida da Cobra 2 painel
            cobra2.vida(25, x - 100, 60, window)
            if cobra2.vida_T == 1:
                cobra2.R = 255
            else:
                cobra2.R = 0
            
            

            # Movimentação
            cobra1.andar()
            cobra2.andar()


            # Mudar Direção
            nick1 = "ShotoNeles"
            nick2 = "JujuPlugkkkj"
            cobra1.mudar_direct(nick1)
            cobra2.mudar_direct(nick2)


            # Aparecer na tela
            cobra1.blit(window)
            cobra2.blit(window)
            maca.blit(window)


            # Colisão
            # Cobra1 com a maçã
            if cobra1.colide(cobra1.snake[0], maca.pos):
                apple.play()
                cobra1.pontos += 1
                maca.pos = maca.on_grid_random()
                maca.sorteio = randint(0, 100)
                cobra1.update()
            

            # Cobra2 com a maçã
            elif cobra2.colide(cobra2.snake[0], maca.pos):
                apple.play()
                cobra2.pontos += 1
                maca.pos = maca.on_grid_random()
                maca.sorteio = randint(0, 100)
                cobra2.update()
        
            

            # Cabeça com cabeça
            elif cobra1.colide(cobra1.snake[0], cobra2.snake[0]):
                
                if len(cobra1.snake) > 3:
                    del cobra1.snake[-4:-1]
                    cobra1.vida_T -= 3
                else:
                    game = False
                    tela_score = True
                
                
                if len(cobra2.snake) > 3:
                    del cobra2.snake[-4:-1]
                    cobra2.vida_T -= 3
                else:
                    game = False
                    tela_score = True
            


            # Cabeça cobra1 com corpo da cobra2 caso so tenha a cabeça
            elif len(cobra1.snake) == 1:
                for i in range(1, len(cobra2.snake)):
                    if cobra1.colide(cobra1.snake[0], cobra2.snake[i]):
                        game = False
                        tela_score = True
            


            # Cabeça da cobra1 com corpo da cobra2 caso tenha corpo
            elif len(cobra1.snake) > 1:
                for i in range(1, len(cobra2.snake)):
                    if cobra1.colide(cobra1.snake[0], cobra2.snake[i]):
                        del cobra1.snake[-1]
                        cobra1.vida_T -= 1



            # Cabeça cobra2 com corpo da cobra1 caso so tenha a cabeça
            elif len(cobra2.snake) == 1:
                for i in range(1, len(cobra1.snake)):
                    if cobra1.colide(cobra2.snake[0], cobra1.snake[i]):
                        game = False
                        tela_score = True
            


            # Cabeça da cobra2 com corpo da cobra1 caso tenha corpo
            elif len(cobra2.snake) > 1:
                for i in range(1, len(cobra1.snake)):
                    if cobra1.colide(cobra2.snake[0], cobra1.snake[i]):
                        del cobra2.snake[-1]
                        cobra2.vida_T -= 1            
            



            # Regras da cobra viva
            # Não bater nas paredes
            if cobra1.snake[0][0] >= 1275 or cobra1.snake[0][0] <= 0 or cobra1.snake[0][1] >= 715 or cobra1.snake[0][1] <= 0:

                cobra1.vida_T -= 1


                # Mudar direção cobra1
                if cobra1.direction == cobra1.left:
                    cobra1.direction = cobra1.right

                elif cobra1.direction == cobra1.right:
                    cobra1.direction = cobra1.left
                
                elif cobra1.direction == cobra1.up:
                    cobra1.direction = cobra1.down
                
                elif cobra1.direction == cobra1.down:
                    cobra1.direction = cobra1.up
                
                else:
                    pass
                


                # Vida das Cobras
                if cobra1.vida_T > 0:
                    del cobra1.snake[-1]
                
                elif cobra1.vida_T <= 0:
                    game = False
                    tela_score = True
                


            if cobra2.snake[0][0] >= 1275 or cobra2.snake[0][0] <= 0 or cobra2.snake[0][1] >= 715 or cobra2.snake[0][1] <= 0:

                cobra2.vida_T -= 1
                # Mudar direçãop cobra2
                if cobra2.direction == cobra2.left:
                    cobra2.direction = cobra2.right

                elif cobra2.direction == cobra2.right:
                    cobra2.direction = cobra2.left
                
                elif cobra2.direction == cobra2.up:
                    cobra2.direction = cobra2.down
                
                elif cobra2.direction == cobra2.down:
                    cobra2.direction = cobra2.up
                
                else:
                    pass

                # Vida das cobras
                if cobra2.vida_T > 0:
                    del cobra2.snake[-1]
                

                elif cobra2.vida_T <= 0:
                    game = False
                    tela_score = True

                





    # Tela de Pause
    if pausa == True:

        mouse = pygame.mouse.get_pos()

        # Fechar
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                run = False
                exit()
            

            # Clicar nos Botões
            if ev.type == MOUSEBUTTONDOWN:
                
                if mouse[0] >= 454 and mouse[0] <= 826 and mouse[1] >= 112 and mouse[1] <= 212:
                    botoes.play()
                    game = True
                    pausa = False
                


                elif mouse[0] >= 453 and mouse[0] <= 826 and mouse[1] >= 311 and mouse[1] <= 412:
                    botoes.play()
                    pausa = False
                    opt = True
                


                elif mouse[0] >= 453 and mouse[0] <= 826 and mouse[1] >= 512 and mouse[1] <= 612:
                    botoes.play()
                    pausa = False
                    inicio = True
                    
            
            # Fechar as Configurações
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    game = True
                    pausa = False

        
        # Background Animação
        
        bg = AddSprites(os.path.join(images, "tela_inicial.jpg"))
        bg.anime(window, var, 1280)



        # Botões
        # Retomar
        if mouse[0] >= 454 and mouse[0] <= 826 and mouse[1] >= 112 and mouse[1] <= 212:
            voltar = AddSprites(os.path.join(sprites, "voltar.png"), 400, 130)
        else:
            voltar = AddSprites(os.path.join(sprites, "voltar.png"), 380, 110)

        voltar.blit(window, x//2 - (380/2), 108)

        # Opcoes


        if mouse[0] >= 453 and mouse[0] <= 826 and mouse[1] >= 311 and mouse[1] <= 412:
            op = AddSprites(os.path.join(sprites, "opções.png"), 400, 130)
        else:
            op = AddSprites(os.path.join(sprites, "opções.png"), 380, 110)

        op.blit(window, x//2 - (380/2), 308)



        # Sair
        if mouse[0] >= 453 and mouse[0] <= 826 and mouse[1] >= 512 and mouse[1] <= 612:
            sair_menu = AddSprites(os.path.join(sprites, "sair_menu.png"), 400, 130)
        else:
            sair_menu = AddSprites(os.path.join(sprites, "sair_menu.png"), 380, 110)
        sair_menu.blit(window, x//2 - (380/2), 508)
        
        # Updates
        # Animação
        var -= speed_geral
    



    # Opções
    if opt == True:

         # Fechar
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                run = False
                exit()

            # Fechar as Configurações
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    game = True
                    opt = False

        window.fill((0, 255, 255))
    




    # Tela final de score
    if tela_score == True:
        
        mouse = pygame.mouse.get_pos()
        
        # Critérios de Vitória
        if cobra1.vida_T > cobra2.vida_T:
            vencedor = nick1
            perdedor = nick2
        
        elif cobra1.vida_T < cobra2.vida_T:
            vencedor = nick2
            perdedor = nick1
        
        elif cobra1.vida_T == cobra2.vida_T:
            if cobra1.pontos > cobra2.pontos:
                vencedor = nick1
                perdedor = nick2
            
            elif cobra1.pontos < cobra2.pontos:
                vencedor = nick2
                perdedor = nick1



                 # Fechar
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                run = False
                exit()
            
            if ev.type == KEYDOWN:
                if ev.key == K_RETURN:
                    tela_score = False
                    game_restart()
                    game = True
            
            if ev.type == MOUSEBUTTONDOWN:
                if mouse[0] > 1088 and mouse[1] > 600 and mouse[0] < 1150 and mouse[1] < 600 + 65:
                    tela_score = False
                    inicio = True
            
                elif mouse[0] > 1200 and mouse[1] > 600 and mouse[0] < 1200 + 65 and mouse[1] < 600 + 65:
                    tela_score = False
                    game_restart()
                    game = True
        



        # Plano de fundo
        mapa_escolhido[2].imagem(window)
        

        # Botões
        if mouse[0] > 1100 and mouse[1] > 600 and mouse[0] < 1162 and mouse[1] < 600 + 65:
            home = AddSprites(os.path.join(sprites, "home.png"), 75, 75)
        else:
            home = AddSprites(os.path.join(sprites, "home.png"), 65, 65)

        home.blit(window, 1100, 600)



        if mouse[0] > 1200 and mouse[1] > 600 and mouse[0] < 1200 + 65 and mouse[1] < 600 + 65:
            reload = AddSprites(os.path.join(sprites, "reload.png"), 75, 75)
        else:
            reload = AddSprites(os.path.join(sprites, "reload.png"), 65, 65)

        reload.blit(window, 1200, 600)

        # Labels da tela
        label1 = pygame.font.SysFont(os.path.join(fonts, "Aleo-BoldItalic.ttf"), 70)
        label2 = pygame.font.SysFont(os.path.join(fonts, "Aleo-BoldItalic.ttf"), 40)

        win = label1.render("Vencedor", True, (17,6,38))
        loss = label1.render("Perdedor", True, (17,6,38))

        if vencedor == nick1:
            macas1 = label2.render(f"Maçãs Comidas - {cobra1.pontos}", True, (17,6,38))
            macas_rect = macas1.get_rect()
            macas2 = label2.render(f"Maçãs Comidas - {cobra2.pontos}", True, (17,6,38))
        
        elif vencedor == nick2:
            macas1 = label2.render(f"Maçãs Comidas - {cobra2.pontos}", True, (17,6,38))
            macas_rect = macas1.get_rect()
            macas2 = label2.render(f"Maçãs Comidas - {cobra1.pontos}", True, (17,6,38))

        nome_w = label2.render(f"{vencedor}", True, (17,6,38))
        nome_wrect = nome_w.get_rect()
        nome_l = label2.render(f"{perdedor}", True, (17,6,38))
        nome_lrect = nome_l.get_rect()




        placa = pygame.image.load(os.path.join(sprites, "score.png"))


        # Placas com resultado
        if mouse[0] >= 220 and mouse[0] <= 620 and mouse[1] >= 60 and mouse[1] <= 660:
            placa = pygame.transform.scale(placa, (450, 650))
            window.blit(placa, (195, 45))
            window.blit(win, (308, 80))
            window.blit(nome_w, ((195 + 450 / 2) - (nome_wrect[2] / 2), 150))
            window.blit(macas1, ((195 + 450 / 2) - (macas_rect[2] / 2), 300))
        else:
            placa = pygame.transform.scale(placa, (400, 600))
            window.blit(placa, (220, 60))
            window.blit(win, (310, 95))
            window.blit(nome_w, ((220 + 400 / 2) - (nome_wrect[2] / 2), 165))
            window.blit(macas1, ((220 + 400 / 2) - (macas_rect[2] / 2), 315))
        
        
        if mouse[0] >= 660 and mouse[0] <= 1060 and mouse[1] >= 60 and mouse[1] <= 660:
            placa = pygame.transform.scale(placa, (450, 650))
            window.blit(placa, (645, 45))
            window.blit(loss, (758, 80))
            window.blit(nome_l, ((645 + 450 / 2) - (nome_lrect[2] / 2), 150))
            window.blit(macas2, ((645 + 450 / 2) - (macas_rect[2] / 2), 300))

        else:
            placa = pygame.transform.scale(placa, (400, 600))
            window.blit(placa, (660, 60))
            window.blit(loss, (750, 95))
            window.blit(nome_l, ((660 + 400 / 2) - (nome_lrect[2] / 2), 165))
            window.blit(macas2, ((660 + 400 / 2) - (macas_rect[2] / 2), 315))


        print("Shoto", cobra1.vida_T, "Julio", cobra2.vida_T)
    clock.tick(30)
    pygame.display.update()

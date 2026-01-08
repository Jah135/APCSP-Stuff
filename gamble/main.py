import pygame
import random 



pygame.init()

SCREEN_SIZE = (1000, 1000)
BG = (30, 30, 30)
BTN_BG = (50, 50, 215)
safe = (50, 255, 50)
BOOM_COLOR = (255, 50, 50)

boom = random.randint(1,25)
#print(boom) #debug to see mine 

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("mine gambling")
clock = pygame.time.Clock()
running = True
h= 100
w=100
x=100
y=100
rect1=pygame.Rect(x+175*0, y+175*0, h, w)
rect2=pygame.Rect(x+175*1, y+175*0, h, w)
rect3=pygame.Rect(x+175*2, y+175*0, h, w)
rect4=pygame.Rect(x+175*3, y+175*0, h, w)
rect5=pygame.Rect(x+175*4, y+175*0, h, w)
rect6=pygame.Rect(x+175*0, y+175*1, h, w)
rect7=pygame.Rect(x+175*1, y+175*1, h, w)
rect8=pygame.Rect(x+175*2, y+175*1, h, w)
rect9=pygame.Rect(x+175*3, y+175*1, h, w)
rect10=pygame.Rect(x+175*4, y+175*1, h, w)
rect11=pygame.Rect(x+175*0, y+175*2, h, w)
rect12=pygame.Rect(x+175*1, y+175*2, h, w)
rect13=pygame.Rect(x+175*2, y+175*2, h, w)
rect14=pygame.Rect(x+175*3, y+175*2, h, w)
rect15=pygame.Rect(x+175*4, y+175*2, h, w)
rect16=pygame.Rect(x+175*0, y+175*3, h, w)
rect17=pygame.Rect(x+175*1, y+175*3, h, w)
rect18=pygame.Rect(x+175*2, y+175*3, h, w)
rect19=pygame.Rect(x+175*3, y+175*3, h, w)
rect20=pygame.Rect(x+175*4, y+175*3, h, w)
rect21=pygame.Rect(x+175*0, y+175*4, h, w)
rect22=pygame.Rect(x+175*1, y+175*4, h, w)
rect23=pygame.Rect(x+175*2, y+175*4, h, w)
rect24=pygame.Rect(x+175*3, y+175*4, h, w)
rect25=pygame.Rect(x+175*4, y+175*4, h, w)

# track revealed squares and score
revealed = [False] * 25
score = 0
font = pygame.font.SysFont(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # left mouse button pressed
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect1.collidepoint(event.pos):
                if boom == 1:
                    print("boom (square 1)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect1)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 1)")
                    if not revealed[0]:
                        score += 1
                        revealed[0] = True
                    pygame.draw.rect(screen, safe, rect1)
                    pygame.display.flip()
            elif rect2.collidepoint(event.pos):
                if boom == 2:
                    print("boom (square 2)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect2)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 2)")
                    if not revealed[1]:
                        score += 1
                        revealed[1] = True
                    pygame.draw.rect(screen, safe, rect2)
                    pygame.display.flip()
            elif rect3.collidepoint(event.pos):
                if boom == 3:
                    print("boom (square 3)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect3)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False    
                else:
                    print("safe (square 3)")
                    if not revealed[2]:
                        score += 1
                        revealed[2] = True
                    pygame.draw.rect(screen, safe, rect3)
                    pygame.display.flip()
            elif rect4.collidepoint(event.pos):
                if boom == 4:
                    print("boom (square 4)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect4)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False       
                else:
                    print("safe (square 4)")
                    if not revealed[3]:
                        score += 1
                        revealed[3] = True
                    pygame.draw.rect(screen, safe, rect4)
                    pygame.display.flip()
            elif rect5.collidepoint(event.pos):
                 if boom == 5:
                    print("boom (square 5)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect5)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                 else:
                    print("safe (square 5)")
                    if not revealed[4]:
                        score += 1
                        revealed[4] = True
                    pygame.draw.rect(screen, safe, rect5)
                    pygame.display.flip()
            elif rect6.collidepoint(event.pos):
                if boom == 6:
                    print("boom (square 6)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect6)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 6)")
                    if not revealed[5]:
                        score += 1
                        revealed[5] = True
                    pygame.draw.rect(screen, safe, rect6)
                    pygame.display.flip()
            elif rect7.collidepoint(event.pos):
                if boom == 7:
                    print("boom (square 7)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect7)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 7)")
                    if not revealed[6]:
                        score += 1
                        revealed[6] = True
                    pygame.draw.rect(screen, safe, rect7)
                    pygame.display.flip()
            elif rect8.collidepoint(event.pos):
                if boom == 8:
                    print("boom (square 8)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect8)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False   
                else:
                    print("safe (square 8)")
                    if not revealed[7]:
                        score += 1
                        revealed[7] = True
                    pygame.draw.rect(screen, safe, rect8)
                    pygame.display.flip()
            elif rect9.collidepoint(event.pos):
                if boom == 9:
                    print("boom (square 9)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect9)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False        
                else:
                    print("safe (square 9)")
                    if not revealed[8]:
                        score += 1
                        revealed[8] = True
                    pygame.draw.rect(screen, safe, rect9)
                    pygame.display.flip()
            elif rect10.collidepoint(event.pos):
                if boom == 10:
                    print("boom (square 10)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect10)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 10)")
                    if not revealed[9]:
                        score += 1
                        revealed[9] = True
                    pygame.draw.rect(screen, safe, rect10)
                    pygame.display.flip()
            elif rect11.collidepoint(event.pos):
               if boom == 11:
                    print("boom (square 11)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect11)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
               else:
                    print("safe (square 11)")
                    if not revealed[10]:
                        score += 1
                        revealed[10] = True
                    pygame.draw.rect(screen, safe, rect11)
                    pygame.display.flip()
            elif rect12.collidepoint(event.pos):
               if boom == 12:
                    print("boom (square 12)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect12)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
               else:
                    print("safe (square 12)")
                    if not revealed[11]:
                        score += 1
                        revealed[11] = True
                    pygame.draw.rect(screen, safe, rect12)
                    pygame.display.flip()
            elif rect13.collidepoint(event.pos):
                if boom == 13:
                    print("boom (square 13)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect13)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False    
                else:
                    print("safe (square 13)")
                    if not revealed[12]:
                        score += 1
                        revealed[12] = True
                    pygame.draw.rect(screen, safe, rect13)
                    pygame.display.flip()
            elif rect14.collidepoint(event.pos):
                if boom == 14:
                    print("boom (square 14)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect14)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False        
                else:
                    print("safe (square 14)")
                    if not revealed[13]:
                        score += 1
                        revealed[13] = True
                    pygame.draw.rect(screen, safe, rect14)
                    pygame.display.flip()
            elif rect15.collidepoint(event.pos):
                if boom == 15:
                    print("boom (square 15)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect15)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 15)")
                    if not revealed[14]:
                        score += 1
                        revealed[14] = True
                    pygame.draw.rect(screen, safe, rect15)
                    pygame.display.flip()
            elif rect16.collidepoint(event.pos):
                if boom == 16:
                    print("boom (square 16)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect16)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 16)")
                    if not revealed[15]:
                        score += 1
                        revealed[15] = True
                    pygame.draw.rect(screen, safe, rect16)
                    pygame.display.flip()
            elif rect17.collidepoint(event.pos):
                if boom == 17:
                    print("boom (square 17)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect17)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 17)")
                    if not revealed[16]:
                        score += 1
                        revealed[16] = True
                    pygame.draw.rect(screen, safe, rect17)
                    pygame.display.flip()
            elif rect18.collidepoint(event.pos):
                if boom == 18:
                    print("boom (square 18)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect18)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False   
                else:
                    print("safe (square 18)")
                    if not revealed[17]:
                        score += 1
                        revealed[17] = True
                    pygame.draw.rect(screen, safe, rect18)
                    pygame.display.flip()
            elif rect19.collidepoint(event.pos):
                if boom == 19:
                    print("boom (square 19)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect19)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False        
                else:
                    print("safe (square 19)")
                    if not revealed[18]:
                        score += 1
                        revealed[18] = True
                    pygame.draw.rect(screen, safe, rect19)
                    pygame.display.flip()
            elif rect20.collidepoint(event.pos):
                if boom == 20:
                    print("boom (square 20)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect20)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 20)")
                    if not revealed[19]:
                        score += 1
                        revealed[19] = True
                    pygame.draw.rect(screen, safe, rect20)
                    pygame.display.flip()
            elif rect21.collidepoint(event.pos):
                if boom == 21:
                    print("boom (square 21)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect21)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 21)")
                    if not revealed[20]:
                        score += 1
                        revealed[20] = True
                    pygame.draw.rect(screen, safe, rect21)
                    pygame.display.flip()
            elif rect22.collidepoint(event.pos):
                if boom == 22:
                    print("boom (square 22)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect22)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 22)")
                    if not revealed[21]:
                        score += 1
                        revealed[21] = True
                    pygame.draw.rect(screen, safe, rect22)
                    pygame.display.flip()
            elif rect23.collidepoint(event.pos):
                if boom == 23:
                    print("boom (square 23)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect23)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False    
                else:
                    print("safe (square 23)")
                    if not revealed[22]:
                        score += 1
                        revealed[22] = True
                    pygame.draw.rect(screen, safe, rect23)
                    pygame.display.flip()
            elif rect24.collidepoint(event.pos):
               if boom == 24:
                    print("boom (square 24)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect24)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False       
               else:
                    print("safe (square 24)")
                    if not revealed[23]:
                        score += 1
                        revealed[23] = True
                    pygame.draw.rect(screen, safe, rect24)
                    pygame.display.flip()
            elif rect25.collidepoint(event.pos):
                if boom == 25:
                    print("boom (square 25)")
                    pygame.draw.rect(screen, BOOM_COLOR, rect25)
                    pygame.display.flip()
                    pygame.time.delay(500)
                    running = False
                else:
                    print("safe (square 25)")
                    if not revealed[24]:
                        score += 1
                        revealed[24] = True
                    pygame.draw.rect(screen, safe, rect25)
                    pygame.display.flip()
            
            #ai start
            '''  
            for i, r in enumerate(rects):
                if r.collidepoint(event.pos):
                    if i == mine_index:
                        print("boom (square {})".format(i+1))
                        # optional: reveal the mine visually then quit
                        pygame.draw.rect(screen, BOOM_COLOR, r)
                        pygame.display.flip()
                        pygame.time.delay(500)
                        running = False
                    else:
                        print(i+1)
                    break
            '''
            #ai end
        
    if not running:
        break
    screen.fill(BG)
    # draw each rect, preserving revealed state
    if revealed[0]:
        pygame.draw.rect(screen, safe, rect1)
    else:
        pygame.draw.rect(screen, BTN_BG, rect1)
    if revealed[1]:
        pygame.draw.rect(screen, safe, rect2)
    else:
        pygame.draw.rect(screen,BTN_BG, rect2)
    if revealed[2]:
        pygame.draw.rect(screen, safe, rect3)
    else:
        pygame.draw.rect(screen,BTN_BG, rect3)
    if revealed[3]:
        pygame.draw.rect(screen, safe, rect4)
    else:
        pygame.draw.rect(screen,BTN_BG, rect4)
    if revealed[4]:
        pygame.draw.rect(screen, safe, rect5)
    else:
        pygame.draw.rect(screen,BTN_BG, rect5)
    if revealed[5]:
        pygame.draw.rect(screen, safe, rect6)
    else:
        pygame.draw.rect(screen, BTN_BG, rect6)
    if revealed[6]:
        pygame.draw.rect(screen, safe, rect7)
    else:
        pygame.draw.rect(screen,BTN_BG, rect7)
    if revealed[7]:
        pygame.draw.rect(screen, safe, rect8)
    else:
        pygame.draw.rect(screen,BTN_BG, rect8)
    if revealed[8]:
        pygame.draw.rect(screen, safe, rect9)
    else:
        pygame.draw.rect(screen,BTN_BG, rect9)
    if revealed[9]:
        pygame.draw.rect(screen, safe, rect10)
    else:
        pygame.draw.rect(screen,BTN_BG, rect10)
    if revealed[10]:
        pygame.draw.rect(screen, safe, rect11)
    else:
        pygame.draw.rect(screen, BTN_BG, rect11)
    if revealed[11]:
        pygame.draw.rect(screen, safe, rect12)
    else:
        pygame.draw.rect(screen,BTN_BG, rect12)
    if revealed[12]:
        pygame.draw.rect(screen, safe, rect13)
    else:
        pygame.draw.rect(screen,BTN_BG, rect13)
    if revealed[13]:
        pygame.draw.rect(screen, safe, rect14)
    else:
        pygame.draw.rect(screen,BTN_BG, rect14)
    if revealed[14]:
        pygame.draw.rect(screen, safe, rect15)
    else:
        pygame.draw.rect(screen,BTN_BG, rect15)
    if revealed[15]:
        pygame.draw.rect(screen, safe, rect16)
    else:
        pygame.draw.rect(screen, BTN_BG, rect16)
    if revealed[16]:
        pygame.draw.rect(screen, safe, rect17)
    else:
        pygame.draw.rect(screen,BTN_BG, rect17)
    if revealed[17]:
        pygame.draw.rect(screen, safe, rect18)
    else:
        pygame.draw.rect(screen,BTN_BG, rect18)
    if revealed[18]:
        pygame.draw.rect(screen, safe, rect19)
    else:
        pygame.draw.rect(screen,BTN_BG, rect19)
    if revealed[19]:
        pygame.draw.rect(screen, safe, rect20)
    else:
        pygame.draw.rect(screen,BTN_BG, rect20)
    if revealed[20]:
        pygame.draw.rect(screen, safe, rect21)
    else:
        pygame.draw.rect(screen, BTN_BG, rect21)
    if revealed[21]:
        pygame.draw.rect(screen, safe, rect22)
    else:
        pygame.draw.rect(screen,BTN_BG, rect22)
    if revealed[22]:
        pygame.draw.rect(screen, safe, rect23)
    else:
        pygame.draw.rect(screen,BTN_BG, rect23)
    if revealed[23]:
        pygame.draw.rect(screen, safe, rect24)
    else:
        pygame.draw.rect(screen,BTN_BG, rect24)
    if revealed[24]:
        pygame.draw.rect(screen, safe, rect25)
    else:
        pygame.draw.rect(screen,BTN_BG, rect25)


    # draw score
    score_surf = font.render("Score: {}".format(score), True, (255,255,255))
    screen.blit(score_surf, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
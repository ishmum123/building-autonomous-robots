import pygame, math
pygame.init()
screen=pygame.display.set_mode((800,600))
clock=pygame.time.Clock()
a=0
running=True
while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
    screen.fill((20,20,20))
    x,y,r=400,300,80
    pygame.draw.circle(screen,(230,230,230),(x,y),r,3)
    pygame.draw.line(screen,(0,255,255),(x,y),(x+int(r*math.cos(math.radians(a))),y+int(r*math.sin(math.radians(a)))),3)
    a=(a+2)%360
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

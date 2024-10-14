import pygame
from Tetris_funktioner import läsa_poäng
import random as r
pygame.init()

#Övergripande grafik

#Tilldela färg
SVART = (0, 0, 0)
VIT = (255, 255, 255)
GRÅ = (200, 200, 200)
TURKOS = (64, 224, 208)
ORANGE = (255, 165, 0)
BLÅ = (0, 0, 255)
GUL = (255, 255, 0)
RÖD = (255, 0, 0)
GRÖN = (0, 255, 0)
LILA = (128, 0, 128)

färger=[SVART, VIT, TURKOS, ORANGE, BLÅ, RÖD, GRÖN, GUL, LILA]



#Grafik för menyn:
menu_title_font = pygame.font.SysFont("Verdana", 50)
menu_font = pygame.font.SysFont("Arial", 30)
menu_instruction_font=pygame.font.SysFont("Courier New", 30)
button_font = pygame.font.SysFont("Verdana", 20)
grattis_font= pygame.font.SysFont("Verdana",50)

level_font = pygame.font.SysFont('Arial', 40)
line_font = pygame.font.SysFont('Arial', 60)

title_text = menu_title_font.render('Välkommen till Tetris', True, TURKOS)
name_text = menu_instruction_font.render("Skriv in ditt namn", True, VIT)

menu_background = pygame.Surface((700, 750))
menu_background.fill((100, 100, 100)) 
menu_background.blit(title_text, (80, 50))  
menu_background.blit(name_text, (50, 250))
pygame.draw.rect(menu_background, (150, 150, 150), (45, (295), 400, 42))

 



#Grafik för själva spelet

#Grafik för bakgrunden:
name_and_highscore=läsa_poäng(True)
namn=name_and_highscore[0]
highscore=name_and_highscore[1]


screen_width= 700
screen_height = 750
background = pygame.Surface((screen_width, screen_height))
background.fill((70, 70, 70))  



game_font = pygame.font.SysFont('Arial', 20)
game_font2 = pygame.font.SysFont('Arial', 16)


#Rita ut brädet och bakgrunden
background_x_kord=194
background_y_kord=100
for x in range(11):
    pygame.draw.line(background,SVART,(background_x_kord,100),(background_x_kord,721))
    background_x_kord+=31
for y in range(21):
    pygame.draw.line(background,SVART,(194,background_y_kord),(504,background_y_kord))
    background_y_kord+=31

#Ruta och text för nästa figur
text = game_font.render('Next figure', True, VIT)


background.blit(text, (535, 95))
square_x=535
square_y=131
for line in range(2):
    pygame.draw.line(background,SVART,(square_x,square_y+(line*155)),(square_x+155,square_y+(line*155)))
    pygame.draw.line(background,SVART,(square_x+(line*155),square_y),(square_x+(line*155),square_y+155))

#Grafik efter spelet

leaderboard_background = pygame.Surface((700, 750))
leaderboard_background.fill((100, 100, 100)) 
leaderboard_text = menu_title_font.render('Leaderboard', True, TURKOS)
leaderboard_background.blit(leaderboard_text,(80,50))


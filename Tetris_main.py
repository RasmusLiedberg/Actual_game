import pygame
import sys
import Tetris_klasser as tk
import random as r
import os

from Tetris_funktioner import*
from Tetris_grafik import*


#Betsämer var filerna hämtas så att det fungerar vid export
base_path = os.path.dirname(os.path.abspath(__file__))
klasser_path = os.path.join(base_path, 'Tetris_klasser.py')
grafik_path = os.path.join(base_path, 'Tetris_grafik.py')
funktioner_path = os.path.join(base_path, 'Tetris_funktioner.py')


#Funktionen finns i main-filen för att vissa variabler och annat hanteras här
def rita_knapp(text, x, y, w, h, färg, hover_färg, action=None):
    mus = pygame.mouse.get_pos()  #Musens position
    #klick = pygame.mouse.get_pressed()  #Aktiverar så länge som knappen är nedtryckt, kan vara användbart senarre
    klick = pygame.event.get(pygame.MOUSEBUTTONDOWN)

     # Kontrollera om musen är över knappen
    if x < mus[0] < x + w and y < mus[1] < y + h:
        pygame.draw.rect(screen, hover_färg, (x, y, w, h))

        # Kolla om vänster musknapp trycktes ner (event.button == 1)
        for event in klick:
            if event.button == 1 and action != None:
                action()  # Kör funktionen som är associerad med knappen
    else:
        pygame.draw.rect(screen, färg, (x, y, w, h))
    
    # Lägga till text på knappen
    text_yta = button_font.render(text, True, SVART)
    screen.blit(text_yta, (x + (w // 2 - text_yta.get_width() // 2), y + (h // 2 - text_yta.get_height() // 2)))

def testande():
    print("Test")


#streck=1, kvadrat=2, L=3, L-invers=4, pyramid=5, zig=6, zag=7 
figurer=[[1,None],[2,None],[3,None],[4,None],[5,None],[6,None],[7,None]]


for x in figurer:
    plats=r.randint(0,len(färger)-1)
    x[1]=färger.pop(plats)


höjd=20
bredd=10

level=0 #Håller koll på vilken nivå spelaren är på
line_counter=0 #Räknar hur många rader som tas bort, vid 10 ökas level med ett och denna återställs
poäng=0
bräde=[]
highscore=läsa_poäng(True) #Hämter första raden från topplistan True betyder bara en rad och inte alla
user_name= '' 


running = True #Running sätts till True innan menyn så att att den kan bli False då fönstret stängs

#Tids-inställningar
clock = pygame.time.Clock()
FPS = 60

#Timer i menyn
shown_empty_error_time=0
shown_lenght_error_time=0
shown_error_timer=1000


for x in range(höjd):
    temp_list=[]
    for y in range(bredd):
        temp_list.append(False)
    bräde.append(temp_list)


# Initiera Pygame
pygame.init()


# Skapa spel-fönster (bred x höjd)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")


length_error=False
input_active = True
menu=True
avsluta_menu=False

while(menu): #menyn, visar regler, skriver in namn etc...
    highscore=läsa_poäng(True)
    menu_time = pygame.time.get_ticks()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False  #Stänger av hela spelet

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Om man trycker på Enter

                    for tecken in user_name:
                        if tecken !=" ":
                            avsluta_menu=True
                    if avsluta_menu and not length_error:
                        menu = False  # Starta spelet efter namn har skrivits in och villkoren uppfylls
                    else:
                        shown_empty_error_time=menu_time

                elif event.key == pygame.K_BACKSPACE:
                    # Ta bort senaste bokstaven
                    user_name = user_name[:-1]

                else:
                    # Lägg till bokstaven i användarens text
                    if input_active and not len(user_name)>25:
                        user_name += event.unicode

    if len(user_name)>=25:
        length_error=True
    
    else:
        length_error=False
    
    error_empty_text=menu_font.render("Namnet får inte vara tomt!", True, SVART)
    error_length_text=menu_font.render("Namnet får inte vara längre än 25 tecken!", True, SVART)

    
    screen.fill(SVART)  # Bakgrundsfärg för menyn
    screen.blit(menu_background, (0, 0))  # Visa bakgrundsbilden för menyn

    input_text = menu_font.render(user_name, True, SVART)
    highscore_text= game_font2.render(f"Highscore: {highscore[0]}:{highscore[1]}",True,VIT)
    screen.blit(highscore_text,(50,220))
    screen.blit(input_text, (50, 300))
    rita_knapp("Återställ highscore", 200, 550, 200, 50, GRÅ, GRÖN, reset_highscore)

    if (length_error):
        screen.blit(error_length_text, (100, 400))

    if (menu_time-shown_empty_error_time<shown_error_timer):
        screen.blit(error_empty_text, (200, 400))

    pygame.display.flip() 

#Variablerna för loopen
first_frame=True
kör=True

#Timer för rörelse
player_move_timer = 0  
game_move_timer = 0  
down_move_timer = 0
rotation_timer = 0 

player_move_interval = 200  
down_move_interval = 100
rotation_interval= 150 

current_figure=new_figure(figurer) #Skapar den första figuren
next_figure=new_figure(figurer) #Nästa figur
shown_figure=next_figure_img(next_figure.figure_nbr,figurer)



while running: #Spel-loop

    #stänga fönstret)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    # Tid i millisekunder
    current_time = pygame.time.get_ticks()
    if level<=5:
        block_move_interval = (400- (level*50))

    if current_time - game_move_timer > block_move_interval and kör and not first_frame: #Timer för figurens rörelse
        current_figure.move(31,"down")
        game_move_timer = current_time
 

    keys = pygame.key.get_pressed()
    if current_time - player_move_timer > player_move_interval and kör and not first_frame: #Timer för rörelse i sidled
        
        #Tangenttryckningar
            #Krav är tryck, position, till höger om vägg och inget block till vänster
        if keys[pygame.K_LEFT] and not side_colision_check(current_figure, bräde, "L"):  
      
            current_figure.move(31, "left")   # Flytta vänster 
            player_move_timer= current_time 

        #Krav är tryck, position, till vänster om vägg och inget block till höger
        elif keys[pygame.K_RIGHT] and not side_colision_check(current_figure, bräde, "R"):  # Flytta höger
            current_figure.move(31, "right")
            player_move_timer = current_time  
    
        #Lägg till funktion som tar figur och returnerarr True eller False istället för kolision
    if keys[pygame.K_SPACE] and current_time - rotation_timer> rotation_interval:
            rotation_check(current_figure, bräde)
            current_figure.rotera()
            rotation_timer= current_time



    if current_time - down_move_timer > down_move_interval and keys[pygame.K_DOWN] and kör and not first_frame:
        current_figure.move(31, "down")
        down_move_timer = current_time 

    if colision_check(current_figure, bräde):
        kör=False
        bräde = into_grid(current_figure, bräde)


        fill_values=fill_check(bräde)
        antal_rader=fill_values[1]

        if antal_rader!=0: #Om anatalet fulla rader inte är noll
            pygame.time.wait(100)
            bräde = update_grid(fill_values[0],bräde)
            level_line=level_update_check(level, line_counter, antal_rader)
            level=level_line[0]
            line_counter=level_line[1]
            poäng=poäng+(give_score(antal_rader,level))
            if poäng>highscore[1]:
                highscore=(user_name,poäng)
        if lose_check(bräde):
            running=False
            
            
        current_figure=next_figure
        next_figure=new_figure(figurer)
        shown_figure=next_figure_img(next_figure.figure_nbr,figurer)
        
        kör=True



    #Ritar ut grafiken, backgrund, text och blocken
    screen.fill(SVART)
    screen.blit(background, (0, 0)) #Rensa skärmen och rita bakgrunden

    #Formatera text
    poäng_text = game_font.render(f'Poäng: {poäng}', True, VIT)
    highscore_text= game_font2.render(f"Highscore: {highscore[0]}:{highscore[1]}",True,VIT)
    namn= game_font.render(user_name, True, VIT)
    line_text=line_font.render(f"{10-line_counter}", True, RÖD)
    level_text=level_font.render(f"Lvl: {level}", True, BLÅ)

    #rita ut text
    screen.blit(highscore_text, (20,45))
    screen.blit(poäng_text, (20, 100))
    screen.blit(namn, (20,65))
    screen.blit(line_text, (30,130))
    screen.blit(level_text, (20,190))

    shown_figure.draw(screen) #Ritar nästa figur i rutan
    current_figure.draw(screen) #Rita nuvarande figuren

    for row in bräde:             #Rita blocken i brädeet
        for col in range(len(row)):
            if row[col] != False:
                row[col].draw(screen)
   

    pygame.display.flip() #Uppdaterar fönstret 
    clock.tick(FPS)  #Håller FPS konstant

    if first_frame:
        pygame.time.wait(500)
        first_frame=False



to_file=(user_name,int(poäng)) #Namn och poäng som  ska exporteras till filen

score_list=update_poäng(to_file) #Lägger in poäng på rätt plats och returnerar hela listan med alla poäng
top_5=[]
for placement in range(5):
    top_5.append(score_list[placement])

visa_grattis=False

if poäng==highscore[1]:
    visa_grattis=True


visa_leaderboard=True

while(visa_leaderboard):
    current_time = pygame.time.get_ticks()
    
    if visa_grattis:
        screen.fill(SVART)  #Återatäller bakgrunden
        screen.blit(leaderboard_background, (0, 0))  #Rita bakgrunden
        grattis_text= grattis_font.render("Grattis, nytt highscore!", True, GRÖN)
        screen.blit(grattis_text, (50,200))
        pygame.display.flip() 
        pygame.time.wait(3000)
        visa_grattis=False


    
    for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                visa_leaderboard=False

            if event.type == pygame.MOUSEBUTTONUP:  # Kolla när musknappen släpps
                if x < event.pos[0] < 200 + 200 and y < event.pos[1] < 550 + 50:  # Musen inom knappens gränser
                    testande()  #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  #Trycker på enter, avslutar leaderboard
                    visa_leaderboard=False
  
    
 
    screen.fill(SVART)  #Återatäller bakgrunden
    screen.blit(leaderboard_background, (0, 0))  #Rita bakgrunden
    place_count=1
    rita_knapp("Test!", 200, 550, 200, 50, GRÅ, GRÖN, testande)
    
    for lb_place in top_5: #Ritar ut topp fem
        place_text = game_font.render(f'{place_count} : {lb_place[0]} {lb_place[1]}', True, VIT)
        screen.blit(place_text, (50, 120+(25*place_count)))
        place_count+=1
    

    pygame.display.flip() 
    clock.tick(FPS)  #Håller FPS konstant

#Avsluta Pygame korrekt
pygame.quit()
sys.exit()

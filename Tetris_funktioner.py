import Tetris_klasser as tk
import random as r
import os
import sys

#Funktion från chatgpt
def get_score_file_path():
    if getattr(sys, 'frozen', False):
        # Om programmet körs som en kompilerad .exe (från PyInstaller)
        base_path = sys._MEIPASS
    else:
        # Om programmet körs i utvecklingsmiljön
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Återgå till den fullständiga sökvägen för poängfilen
    return os.path.join(base_path, 'Topplista.txt')



# base_path = os.path.dirname(os.path.abspath(__file__))
# score_file_path = os.path.join(base_path, 'Topplista.txt')


def new_figure(figurer): #Returnerar en slumpmässig figur
    start_pos=[289,100]
    figur=figurer[r.randint(0,6)]

    if figur[0]==1:
        return(tk.figur_streck(figur[1],start_pos))

    elif figur[0]==2:
        start_pos[1]-=31
        start_pos[0]+=31
        return(tk.figur_kvadrat(figur[1],start_pos))

    elif figur[0]==3:
         return(tk.figur_L(figur[1],start_pos))

    elif figur[0]==4:
        return(tk.figur_L_invers(figur[1],start_pos))

    elif figur[0]==5:
        return(tk.figur_pyramid(figur[1],start_pos))

    elif figur[0]==6:
        return(tk.figur_zig(figur[1],start_pos))
    
    elif figur[0]==7:
        start_pos[0]+=31
        return(tk.figur_zag(figur[1],start_pos))
    
def next_figure_img(figur,figurer): #Skapar en kopia av nästa figur och lägger in den i boxen för "Next Figure"
     if figur==1:
        return(tk.figur_streck(figurer[figur-1][1],[550,222]))

     elif figur==2:
        return(tk.figur_kvadrat(figurer[figur-1][1],[585,240]))

     elif figur==3:
         return(tk.figur_L(figurer[figur-1][1],[566,237]))

     elif figur==4:
        return(tk.figur_L_invers(figurer[figur-1][1],[566,237]))

     elif figur==5:
        return(tk.figur_pyramid(figurer[figur-1][1],[566,237]))

     elif figur==6:
        return(tk.figur_zig(figurer[figur-1][1],[566,237]))
    
     elif figur==7:
        return(tk.figur_zag(figurer[figur-1][1],[597,237]))
            
def get_places(figure): #Tar in en figur och returnerar kolonn och rad för varje block i figuren
    lista = []
    block_lista = figure.block_lista

    for block in block_lista:
        if not isinstance(block, list):
            y_kord = block.kords[1]
            x_kord = block.kords[0] + 10

            row = (((y_kord - 100) // 31) - 1)
            col = (((x_kord - 165) // 31) - 1)

            # Kontrollera att rader och kolumner ligger inom brädets gränser
            row = min(max(row, 0), 19)
            col = min(max(col, 0), 9)

            lista.append([row, col, block])

        else:
            for block_2 in block:
                y_kord = block_2.kords[1]
                x_kord = block_2.kords[0] + 10
                row = (((y_kord - 100) // 31) - 1)
                col = (((x_kord - 165) // 31) - 1)

                # Kontrollera att rader och kolumner ligger inom brädets gränser
                row = min(max(row, 0), 19)
                col = min(max(col, 0), 9)

                lista.append([row, col, block_2])

    return (lista)


def colision_check(figur,bräde): #Kollar ifall figuren är precis ovan marken eller ett block
    if figur.position[1]>=692:
        return(True)
    
    lista=get_places(figur)
    
    for x in lista:
        row, col,= x[0], x[1]
        if(row>=0 and col>=0):
            if row==19:
                return(True)
            if bräde[row+1][col]!=False:
                return(True)
    return(False)


def side_colision_check(figur, bräde, direction): #Kollar ifall figuren är precis bredvid väggen eller ett block
    lista=get_places(figur)

    if direction=="L":
        for x in lista:
            row, col,= x[0], x[1]
            if col > 0:
                if bräde[row][col - 1] != False:
                    return True
            elif col == 0:
                return True

    if direction=="R":
        for x in lista:
            row, col,= x[0], x[1]
            if col < len(bräde[0]) - 1:
                if bräde[row][col + 1] != False:
                    return True
            elif col == len(bräde[0]) - 1:
                return True
            

def into_grid(figur,bräde): #Lägger in figurens block-objekt i brädet
    temp_bräde=[]

    for rad in bräde:
        temp_bräde.append(rad)
    lista=get_places(figur)

    for x in lista:
        row, col, block  = x[0], x[1], x[2]
        temp_bräde[row][col]= block

    return(temp_bräde)

def rotation_check(figur, bräde): #Hanterar rotationen så att blocket håller sig rakt och inte flyttas/går in i vögg eller block
    figure_nbr=(figur.figure_nbr)
    rotation_nbr=(figur.rotation_nbr)
    places=get_places(figur)
    first_block=places[0]
    col=first_block[1]
    row=first_block[0]

    if figure_nbr==1:
        if (col==0 and rotation_nbr==2) or bräde[row][col - 1] != False:
            figur.move(31,"right")

        if col==9 and rotation_nbr==2 or bräde[row][col + 1] != False:
            figur.move(62,"left")
    elif figure_nbr==2:
        pass

    elif figure_nbr==3:

        if rotation_nbr==4:
            if col==0 or bräde[row][col - 1] != False:
                figur.move(31,"right")

        if rotation_nbr==2:
            if col==9 or bräde[row][col + 1] != False:
                figur.move(31,"left")
        
    elif figure_nbr==4:
        first_block=places[1]
        col=first_block[1]
        row=first_block[0]

        if rotation_nbr==4:
           if col==0 or bräde[row][col - 1] != False:
                figur.move(31,"right")
                
        if rotation_nbr==2:
            if col==9 or bräde[row][col + 1] != False:
                figur.move(31,"left")
 
    elif figure_nbr==5:

        if rotation_nbr==4:
           if col==0 or bräde[row][col - 1] != False:
                figur.move(31,"right")
                
        if rotation_nbr==2:
            if col==9 or bräde[row][col + 1] != False:
                figur.move(31,"left")

    elif figure_nbr==6:
        if rotation_nbr==2:
            if col==9 or bräde[row][col + 1] != False:
                figur.move(31,"left")

    elif figure_nbr==7:
        if rotation_nbr==2:
            if col==0 or bräde[row][col - 1] != False:
                figur.move(31,"right")


            
def fill_check(bräde): #Kollar om någon rad är full och ifall någon är returnerade vilka och hur många
   antal_rader=0
   vilka_rader=[]
   temp_bräde=[]
   for row in bräde:
       temp_bräde.append(row)

   for rad_index, rad in enumerate(temp_bräde): #används för att få både index och innehåll för varje rad.
        if all(rad):
            antal_rader += 1
            vilka_rader.append(rad_index)

   return([vilka_rader,antal_rader])


def update_grid(vilka_rader, bräde): #Clearar de fyllda radena och flyttar ned raderna ovanför de clearade
    empty_list = [False] * 10
    temp_bräde = []
    vilka_rader.sort()
    

    for x in bräde:
        temp_bräde.append(x) #Kopia av bräde
    vilka_rader.reverse() #Ska gå från största till minsta talet

    for y in vilka_rader: #Går igenom raderna som tagits bprt
        row_count=0            #Håller koll på vilken rad

        for row in temp_bräde:  #Går igenom raderna i brädet

            if row_count<y and row_count not in vilka_rader:     #Om raden är lägre än raden som tagits bort

                for place in row:
                    if (place!=False):  #Om det är ett objekt på platsen
                        place.move(31,"down")
            row_count+=1

    temp_bräde=[] #Återställer temp_bädet
    

    # Gå igenom brädet och bygg upp ett temporärt bräde utan de fyllda raderna
    for rad_index, rad in enumerate(bräde):
        if rad_index not in vilka_rader:
            temp_bräde.append(rad)

    # Lägg till tomma rader ovanpå så att brädet återgår till sin fulla storlek
    while len(temp_bräde) < 20:
        temp_bräde.insert(0, empty_list[:])


    return (temp_bräde)



def give_score(nbr,level): #Tar in antal rader clearade och returnerar motsvarande poäng
    if nbr==1:
        return(40*(level+1))
    elif(nbr==2):
        return(100*(level+1))
    elif(nbr==3):
        return(300*(level+1))
    elif(nbr==4):
        return(120*(level+1))
    
def level_update_check(level, lines, antal_rader): #Uppdaterar antal clearade rader och kollar ifall nivån ska uppdateras
    line_nbr=lines+antal_rader

    if line_nbr>=10:
        level+=1
        line_nbr=(line_nbr%10)
    
    return([level, line_nbr])

def lose_check(bräde): #Returnerar True ifall översta raden har block i sig = förlorar
    for x in bräde[0]:
        if x!=False:
            return(True)
    return(False)


#Min funktion
# def läsa_poäng(first:bool):

#     highscores = []
#     with open(score_file_path, 'r') as file:
#         for line in file:
#             parts = line.split(':')
#             namn, poäng = parts
#             highscores.append((namn, int(poäng)))  
#     if first:
#         return(highscores[0])
#     return highscores


#Funktion från chatgpt
# def läsa_poäng(first: bool):
#     score_file_path = get_score_file_path()
#     highscores = []
#     try:
#         with open(score_file_path, 'r') as file:
#             for line in file:
#                 parts = line.strip().split(':')
#                 if len(parts) == 2:
#                     namn, poäng = parts
#                     highscores.append((namn, int(poäng)))
#     except FileNotFoundError:
#         print("Ingen poängfil hittades, startar en ny lista.")
    
#     if first:
#         return highscores[0] if highscores else None
#     return highscores

#Funktion 2 från gpt
def läsa_poäng(first: bool):
    score_file_path = get_score_file_path()  # Få rätt sökväg
    highscores = []
    
    try:
        with open(score_file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    namn, poäng = parts
                    highscores.append((namn, int(poäng)))
    except FileNotFoundError:
        print("Ingen poängfil hittades, startar en ny lista.")
    
    if first:
        return highscores[0] if highscores else None
    return highscores


#Min funktion
# def update_poäng(to_file):
#     put_in=True
#     poäng=to_file[1]
#     scores=läsa_poäng(False)
#     score_list=[]

#     for score in scores:        #Uppdaterar score_list med senaste poängen
#         if score[1]<=poäng and put_in:
#             score_list.append(to_file)
#             put_in=False
#         score_list.append(score)
#     if put_in:
#         score_list.append(to_file)

#      # Öppnar filen i skrivläge ('w') för att skriva över den
#     with open(score_file_path, 'w') as file:
#         for namn, poäng in score_list:
#             file.write(f'{namn}:{poäng}\n')

# return(score_list)

#Funktion från chatgpt
def update_poäng(to_file):
    score_file_path = get_score_file_path()
    put_in = True
    poäng = to_file[1]
    scores = läsa_poäng(False)
    score_list = []

    for score in scores:
        if score[1] <= poäng and put_in:
            score_list.append(to_file)
            put_in = False
        score_list.append(score)

    if put_in:
        score_list.append(to_file)

    with open(score_file_path, 'w') as file:
        for namn, poäng in score_list:
            file.write(f'{namn}:{poäng}\n')

    return score_list




#Min funktion
# def reset_highscore():
#     with open(score_file_path, 'w') as file:
#         for x in range(5):
#             file.write(f" :0\n")

#Funktion från chatgpt
def reset_highscore():
    score_file_path = get_score_file_path()
    with open(score_file_path, 'w') as file:
        for _ in range(5):
            file.write(" :0\n")


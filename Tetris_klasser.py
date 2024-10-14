import random as r
import pygame

class block: #Skapas av figurklassen

    def __init__(self, färg:tuple, figur:int, kords:list):
        self.färg=färg
        self.figur=figur
        self.kords=kords

    def __repr__(self):  #Detta används för att ge en representation av objektet i listor, etc.
        return "X"


    def get_färg(self):
        return(self.färg)
    
    def skriv(self):
        print(self.kords)

    def draw(self,screen):
        block_x = self.kords[0]
        block_y = self.kords[1]

        pygame.draw.rect(screen, self.färg, (block_x, (block_y-29), 28, 28))
    
    def move(self, length:int, direction:str):
        if direction=="down":
            self.kords[1]+=length

        elif direction=="up":
            self.kords[1]-=length

        elif direction=="left":
            self.kords[0]-=length
        
        elif direction=="right":
            self.kords[0]+=length

        




class figur: #Huvvudklassen som de andra figurerna byggs på
    def __init__(self,färg:int,position:list):
        self.block_lista=[]
        self.färg=färg
        self.position=position
        self.figure_nbr=0
        self.rotation_nbr=0

    def draw(self,screen):
        if self.figure_nbr==1:
            for x in self.block_lista:
                x.draw(screen)
        else:
            for x in self.block_lista:
                for y in x:
                 y.draw(screen)

    def move(self, length:int, direction:str):
        if self.figure_nbr==1:
            for x in self.block_lista:
                x.move(length, direction)
            self.position=self.block_lista[0].kords

        else:
            for y in self.block_lista:
                for x in y:
                    x.move(length, direction)
            self.position=self.block_lista[0][0].kords



class figur_streck(figur):

    def __init__(self, färg:int, position:list):
        super().__init__(färg, position)
        self.rotation_nbr=1
        self.figure_nbr=1

        
        for x in range(4):
            block_position = [self.position[0] + x * 31, self.position[1]]
            self.block_lista.append(block(self.färg, self.figure_nbr, block_position))
        
    
    def rotera(self):
        if self.rotation_nbr==1:
            a=0
            for x in self.block_lista:
                x.move(a*31, "left")
                x.move(a*31, "up")
                a+=1
            
            self.move(31,"right")
            self.rotation_nbr=2
            
        elif (self.rotation_nbr==2):
            b=0
            for z in self.block_lista:
                z.move(b*31, "right")
                z.move(b*31, "down")
                b+=1
            
            self.move(31,"left")
            self.rotation_nbr=1

        self.position=self.block_lista[0].kords
        

    

class figur_kvadrat(figur):

    def __init__(self, färg:int, position:list):
        super().__init__(färg, position)
        self.figure_nbr=2
        

        for y in range(2):
            temp_list=[]
            for x in range(2):
                block_position = [self.position[0] + x * 31, self.position[1]]
                temp_list.append(block(self.färg, self.figure_nbr, block_position))
            self.block_lista.append(temp_list)
            self.position[1]=self.position[1]-31
            block_position = [self.position[0],self.position[1]]



    def rotera(self):
        pass

        

class figur_L(figur):

    def __init__(self,färg:int,position:list):
        super().__init__(färg, position)
        self.figure_nbr=3
        self.rotation_nbr=1
        #r.randint(1,4)


        temp_list=[]

        for x in range(3):
            block_position = [self.position[0] + x * 31, self.position[1]]
            temp_list.append(block(self.färg, self.figure_nbr, block_position))
        self.block_lista.append(temp_list)
        block_position=[self.position[0]+62,self.position[1]-31]
        self.block_lista.append([block(self.färg, self.figure_nbr, block_position)])
            

    def move(self, length:int, direction:str,):
        for y in self.block_lista:
            for x in y:
                x.move(length, direction)

            
    def skriv(self):
        for x in self.block_lista:
            for y in x:
             print(y.kords)
            print("")
    
    def rotera(self):
        c=0
        if self.rotation_nbr==1:
            a=["left","up","right","down"]
            b=[93,31]
            kord=[0,0]
            self.rotation_nbr=2

        elif self.rotation_nbr==2:
            a=["left","down","right","up"]
            b=[31,93]
            kord=[1,0]
            self.rotation_nbr=3

        elif self.rotation_nbr==3:
            a=["right","down","left","up"]
            b=[93,31]
            kord=[0,2]
            self.rotation_nbr=4

        elif self.rotation_nbr==4:
            a=["right","up","left","down"]
            kord=[0,0]
            b=[31,93]
            self.rotation_nbr=1
            
            
        for y in self.block_lista[0]:
            y.move(31*c, a[0])
            y.move(31*c, a[1])
            c+=1
        self.block_lista[1][0].move(b[0],a[0])
        self.block_lista[1][0].move(b[1],a[1])
        self.move(31,a[2])
        self.move(31,a[3])
        self.position=self.block_lista[kord[0]][kord[1]].kords

            
    
class figur_L_invers(figur):

    def __init__(self,färg:int,position:list):
        super().__init__(färg, position)
        self.figure_nbr=4
        self.rotation_nbr=1
        #self.start_rotation=r.randint(1,4)


        temp_list=[]
        block_position=[self.position[0],self.position[1]-31]
        self.block_lista.append([block(self.färg, self.figure_nbr, block_position)])
        for x in range(3):
            block_position = [self.position[0] + x * 31, self.position[1]]
            temp_list.append(block(self.färg, self.figure_nbr, block_position))
        self.block_lista.append(temp_list)
        
        
    def move(self, length:int, direction:str,):
        for y in self.block_lista:
            for x in y:
                x.move(length, direction)

            
    def skriv(self):
        for x in self.block_lista:
            for y in x:
             print(y.kords)
            print("")
    
    def rotera(self):
        self.block_lista[1].reverse() #Vänder på "kroppeen" för att göra rotationen enklare
        c=0
        if self.rotation_nbr==1:
            a=["right","down","left","up"]
            b=[31,93]
            kord=[0,0]
            self.rotation_nbr=2

        elif self.rotation_nbr==2:
            a=["right","up","left","down"]
            b=[93,31]
            kord=[1,0]
            self.rotation_nbr=3

        elif self.rotation_nbr==3:
            a=["left","up","right","down"]
            b=[31,93]
            kord=[1,0]
            self.rotation_nbr=4

        elif self.rotation_nbr==4:
            a=["left","down","right","up"]
            b=[93,31]
            kord=[1,2]
            self.rotation_nbr=1
            
            
        for y in self.block_lista[1]:
            y.move(31*c, a[0])
            y.move(31*c, a[1])
            c+=1
        self.block_lista[0][0].move(b[0],a[0])
        self.block_lista[0][0].move(b[1],a[1])
        self.move(31,a[2])
        self.move(31,a[3])
        self.position=self.block_lista[kord[0]][kord[1]].kords

        self.block_lista[1].reverse() #Vänder tillbaka den
    
    
class figur_pyramid(figur):

    def __init__(self,färg:int,position:list):
        super().__init__(färg, position)
        self.rotation_nbr=1
        #self.start_rotation=r.randint(1,4)
        self.figure_nbr=5

        temp_list=[]

        for x in range(3):
            block_position = [self.position[0] + x * 31, self.position[1]]
            temp_list.append(block(self.färg, self.figure_nbr, block_position))

        self.block_lista.append(temp_list)
        block_position=[self.position[0]+31,self.position[1]-31]
        self.block_lista.append([block(self.färg, self.figure_nbr, block_position)])



    def rotera(self):
        c=0
        if self.rotation_nbr==1:
            a=["up","left","left","right","down"]
            kord=[0,0]
            self.rotation_nbr=2

        elif self.rotation_nbr==2:
            a=["down","left","down","up","right"]
            kord=[1,0]
            self.rotation_nbr=3

        elif self.rotation_nbr==3:
            a=["down","right","right","left","up"]
            kord=[0,2]
            self.rotation_nbr=4

        elif self.rotation_nbr==4:
            a=["up","right","up","down","left"]
            kord=[0,0]
            self.rotation_nbr=1
            
            
        for y in self.block_lista[0]:
            y.move(31*c, a[0])
            y.move(31*c, a[1])
            c+=1

        self.block_lista[1][0].move(62,a[2])
        self.move(31,a[3])
        self.move(31,a[4])
        self.position=self.block_lista[kord[0]][kord[1]].kords
        
class figur_zig(figur):

    def __init__(self,färg:int,position:list):
        super().__init__(färg, position)
        self.rotation_nbr=1
        #self.start_rotation=r.randint(1,4)
        self.figure_nbr=6

        for y in range(2):

            temp_list=[]

            for x in range(2):
                block_position = [self.position[0] + x * 31, self.position[1]]
                temp_list.append(block(self.färg, self.figure_nbr, block_position))

            self.block_lista.append(temp_list)
            self.position[1]=self.position[1]-31
            self.position[0]=self.position[0]+31
            block_position = [self.position[0],self.position[1]]

        
    def rotera(self):
        if self.rotation_nbr==1:
            a=["down", "right"]
            b=["down", "left"]
            c=["left"]
            self.rotation_nbr=2

        elif self.rotation_nbr==2:
            a=["up", "left"]
            b=["up", "right"]
            c=["right"]
            self.rotation_nbr=1

        self.block_lista[0][0].move(31,a[0])
        self.block_lista[0][0].move(31,a[1])

        self.block_lista[1][0].move(31,b[0])
        self.block_lista[1][0].move(31,b[1])

        self.block_lista[1][1].move(31,c[0])
        self.block_lista[1][1].move(31,c[0])
        

class figur_zag(figur):
     
    def __init__(self,färg:int,position:list):
        super().__init__(färg, position)
        self.rotation_nbr=1
        #self.start_rotation=r.randint(1,4)
        self.figure_nbr=7

        for y in range(2):

            temp_list=[]

            for x in range(2):
                block_position = [self.position[0] + x * 31, self.position[1]]
                temp_list.append(block(self.färg, self.figure_nbr, block_position))

            self.block_lista.append(temp_list)
            self.position[1]=self.position[1]-31
            self.position[0]=self.position[0]-31
            block_position = [self.position[0],self.position[1]]

 
        
    def rotera(self):
        if self.rotation_nbr==1:
            a=["up", "left"]
            b=["up", "right"]
            c=["left"]
            self.rotation_nbr=2
            self.move(31,"right")

        elif self.rotation_nbr==2:
            a=["down", "right"]
            b=["down", "left"]
            c=["right"]
            self.rotation_nbr=1
            self.move(31,"left")

        self.block_lista[0][0].move(31,a[0])
        self.block_lista[0][0].move(31,a[1])

        self.block_lista[0][1].move(31,c[0])
        self.block_lista[0][1].move(31,c[0])

        self.block_lista[1][0].move(31,b[0])
        self.block_lista[1][0].move(31,b[1])
    
        
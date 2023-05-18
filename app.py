import pyxel

def generate_map(wid,hei):
    carte = [[ None for i in range(wid)] for j in range(hei)]
    return carte
    
def generate_False(wid,hei):
    carte = [[ False for i in range(wid)] for j in range(hei)]
    return carte
    
def generate_vision(m,p):
    wid = len(m[0])
    hei = len(m)
    vision = generate_False(wid,hei)
    for y in range(hei):
        for x in range(wid):
            objet = m[y][x]
            if objet == None : continue
            if objet.player == p:
                v= objet.vision
                for a in range(-1*v,v+1):
                    for b in range(-1*v,v+1):
                        if 0<=a+x<wid and 0<=b+y<hei :
                            vision[b+y][a+x] = True
    return vision


def find_empty(m,b):
    x = b.x
    y = b.y
    pos = [[x,y-1],[x+1,y-1],[x-1,y],[x+2,y],[x-1,y+1],[x+2,y+1],[x,y+2],[x+1,y+2]]
    tot = []
    wid = len(m[0])
    hei = len(m)
    for i in pos :
        if (0<=i[0]<wid and 0<=i[1]<hei) and m[i[1]][i[0]] == None : tot.append(i)
    return tot
        
def build(bat,m):
    x = bat.x
    y = bat.y
    if y+1==len(m) or x+1==len(m[0]) : return
    if not(m[y][x] == None and m[y][x+1] == None and m[y+1][x] == None and m[y+1][x+1] == None) : return
    m[y][x+1] = bat
    m[y+1][x] = bat
    m[y][x] = bat
    m[y+1][x+1] = bat


def make(b,unit,m,p):
    pos = find_empty(m,b)
    if len(pos) == 0 : return False
    position = pos[pyxel.rndi(0,len(pos)-1)]
    m[position[1]][position[0]] = unit(position[0],position[1],p)
    return True
        

class Personnage:
    def __init__(self,x,y,vie,attaque,unite,player,mvt,ar,vision):
        self.mvtmax = mvt
        self.mvt = 0
        self.x=x
        self.y=y
        self.attaque = attaque
        # ar is atack range
        self.ar = ar
        self.unite=unite
        self.vie=vie
        self.player=player
        self.vision=vision
        self.nbatack = 1
        
    def move(self,d,m):
        x = self.x
        y = self.y
        wid = len(m[0])
        hei = len(m)
        if not(0<=d[0]+x<wid and 0<=d[1]+y<hei) : return
        if not(m[y+d[1]][x+d[0]] == None) : return
        if self.mvt == 0 : return
        self.x = x+d[0]
        self.y = y+d[1]
        m[y+d[1]][x+d[0]] = self
        m[y][x] = None
        self.mvt -= 1
        
    def damage(self,n,m):
        self.vie -= n
        if self.vie <= 0:
            m[self.y][self.x] = None
            
    def atack(self,thing,m):
        if abs(thing.x-self.x + thing.y-self.y)/2 >= self.ar : return
        if self.nbatack == 0 : return
        self.nbatack -= 1
        thing.damage(self.attaque,m)
        
    def new_turn(self):
        self.mvt =self.mvtmax
        self.nbatack = 1

        
    def update(self,offset):
        pyxel.blt((self.x+offset[0])*8,(self.y+offset[1])*8,2,0,self.unite*32+16*self.player,8,8,0)

class Batiment:
    def __init__(self,x,y,vie,unite,player,vision):
        self.x=x
        self.y=y
        self.unite=unite
        self.vie=vie
        self.vie_max=vie
        self.player=player
        self.vision=vision

    def damage(self,n,m):
        self.vie -= n
        if self.vie <= 0:
            m[self.y][self.x] = None
            m[self.y+1][self.x+1] = None
            m[self.y+1][self.x] = None
            m[self.y][self.x+1] = None

    def update(self,offset):
        pyxel.blt((self.x+offset[0])*8,(self.y+offset[1])*8,1,0,self.unite*32+16*self.player,16,16,0)
        if self.vie<self.vie_max:
            pyxel.rect((self.x+offset[0])*8+3,(self.y+offset[1])*8-1,10,1,8)
            pyxel.rect((self.x+offset[0])*8+3,(self.y+offset[1])*8-1,int(10*self.vie/self.vie_max),1,3)

class knight(Personnage):
    def __init__(self,x,y,player):
        Personnage.__init__(self,x,y,15,4,0,player,7,1,2)

class archer(Personnage):
    def __init__(self,x,y,player):
        Personnage.__init__(self,x,y,8,5,1,player,5,5,3)

class scout(Personnage):
    def __init__(self,x,y,player):
        Personnage.__init__(self,x,y,5,1,2,player,12,1,8)

class base(Batiment):
    def __init__(self,x,y,player):
        Batiment.__init__(self,x,y,50,0,player,2)

class ferme(Batiment):
    def __init__(self,x,y,player):
        Batiment.__init__(self,x,y,10,1,player,1)
        
class caserne(Batiment):
    def __init__(self,x,y,player):
        Batiment.__init__(self,x,y,20,2,player,1)


class tour(Batiment):
    def __init__(self,x,y,player):
        Batiment.__init__(self,x,y,20,3,player,10)
        
class mur(Batiment):
    def __init__(self,x,y,player):
        Batiment.__init__(self,x,y,70,4,player,0)


class Curseur():
    def __init__(self,x,y,player):
        self.x=x
        self.y=y
        self.player=player
    
    def update(self,offset):
        pyxel.blt((self.x+offset[0])*8,(self.y+offset[1])*8,2,0,8*(11+self.player),8,8,0)

class App:
    def __init__(self):
        pyxel.init(128,128, title="NDC 2023")
        pyxel.load("NDC.pyxres")
        self.gold = [100,100] # La quantité de départ de gold de chaque joueurs
        self.joueur=0
        self.affichage=4
        self.wid = 50
        self.hei = 50
        self.carte=generate_map(self.wid,self.hei)
        self.offset=[0,0]
        build(base(8,8,1),self.carte)
        build(base(41,41,0),self.carte)
        self.curseur=Curseur(8,8,1)
        self.fond=8*pyxel.rndi(0,3)
        self.ecran=[]
        self.select = None
        self.bat = None
        self.attacking = None # The unit selected to attack
        for i in range(self.hei):
            self.ecran.append([])
            for j in range(self.wid):
                self.ecran[i].append(8*pyxel.rndi(0,4))
        pyxel.run(self.update, self.draw)

    def joueur_suivant(self,joueur):
        nb_ferme = 0
        self.select = None
        self.attacking = None
        found = False
        for i in self.carte:
            for j in i:
                if j!=None :
                    if type(j)==ferme and j.player == joueur:
                        nb_ferme += 1
                    if type(j) in [knight,archer,scout]:
                        j.new_turn()
                    if type(j)==base and j.player == joueur and not found:
                        self.curseur.x=j.x
                        self.curseur.y=j.y
                        self.offset[0]=-(j.x-7)
                        self.offset[1]=-(j.y-7)
                        self.affichage=3
                        self.joueur=joueur
                        self.curseur.player=joueur
                        found = True
                        
        self.gold[self.joueur] += 10 + nb_ferme*2

    def update(self):
        vision = generate_vision(self.carte,1)
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pyxel.quit()

        elif self.affichage==0:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.affichage=1
            
        elif self.affichage==1 or self.affichage==2:
            if pyxel.btnp(pyxel.KEY_RETURN):
                if self.joueur==0:
                    self.joueur_suivant(1)
                else:
                    self.joueur_suivant(0)

        elif self.affichage==3:
            if pyxel.btnp(pyxel.KEY_UP):
                self.curseur.y-=1
                if self.select != None : self.select.move([0,-1],self.carte)
                if self.curseur.y<0:
                    self.curseur.y=0
                if not self.vision[self.curseur.y][self.curseur.x] : self.curseur.y += 1
                if self.curseur.y + self.offset[1] < 7 : self.offset[1]+=1
            
            elif pyxel.btnp(pyxel.KEY_DOWN):
                self.curseur.y+=1
                if self.select != None : self.select.move([0,1],self.carte)
                if self.curseur.y>=self.hei:
                    self.curseur.y=self.hei-1
                if not self.vision[self.curseur.y][self.curseur.x] : self.curseur.y -= 1
                if self.curseur.y + self.offset[1] > 8 : self.offset[1]-=1
            
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.curseur.x-=1
                if self.select != None : self.select.move([-1,0],self.carte)
                if self.curseur.x<0:
                    self.curseur.x=0
                if not self.vision[self.curseur.y][self.curseur.x] : self.curseur.x += 1
                if self.curseur.x + self.offset[0] < 7 : self.offset[0]+=1
            
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.curseur.x+=1
                if self.select != None : self.select.move([1,0],self.carte)
                if self.curseur.x>=self.wid:
                    self.curseur.x=self.wid-1
                if not self.vision[self.curseur.y][self.curseur.x] : self.curseur.x -= 1
                if self.curseur.x + self.offset[0] > 8 : self.offset[0]-=1

            bat = self.carte[self.curseur.y][self.curseur.x]
            self.bat = bat

            if bat != self.select : self.select = None

            
            if pyxel.btnp(pyxel.KEY_1) or pyxel.btnp(pyxel.KEY_KP_1):
                if bat == None:
                    if self.gold[self.joueur] >= 50:
                        self.gold[self.joueur] -= 50
                        build(tour(self.curseur.x,self.curseur.y,self.joueur),self.carte)
                if type(bat) == caserne and bat.player==self.joueur:
                    if self.gold[self.joueur] >= 20:
                        if make(bat,knight, self.carte,self.joueur):
                            self.gold[self.joueur] -= 20
                if type(bat) in [knight, archer, scout] and bat.player==self.joueur:
                    if self.select == bat : self.select = None
                    else : self.select = bat

            if pyxel.btnp(pyxel.KEY_2) or pyxel.btnp(pyxel.KEY_KP_2):
                if bat == None:
                    if self.gold[self.joueur] >= 150:
                        self.gold[self.joueur] -= 150
                        build(mur(self.curseur.x,self.curseur.y,self.joueur),self.carte)
                if type(bat) == caserne and bat.player==self.joueur:
                    if self.gold[self.joueur] >= 30:
                        if make(bat,archer, self.carte,self.joueur):
                            self.gold[self.joueur] -= 30
                if type(bat) in [knight, archer, scout] and bat.player==self.joueur:
                    if self.attacking == bat or bat.player != self.joueur : self.attacking = None
                    else : self.attacking = bat
                else : self.attacking = None

                
            if pyxel.btnp(pyxel.KEY_3) or pyxel.btnp(pyxel.KEY_KP_3):
                if bat == None:
                    if self.gold[self.joueur] >= 70:
                        self.gold[self.joueur] -= 70
                        build(caserne(self.curseur.x,self.curseur.y,self.joueur),self.carte)
                
                if type(bat) == caserne and bat.player==self.joueur:
                    if self.gold[self.joueur] >= 10:
                        if make(bat,scout, self.carte,self.joueur):
                            self.gold[self.joueur] -= 10

                if self.attacking != None and bat != None :
                    self.attacking.atack(bat,self.carte)
                    

            if pyxel.btnp(pyxel.KEY_4) or pyxel.btnp(pyxel.KEY_KP_4):
                if bat == None:
                    if self.gold[self.joueur] >= 40:
                        self.gold[self.joueur] -= 40
                        build(ferme(self.curseur.x,self.curseur.y,self.joueur),self.carte)


            if pyxel.btnp(pyxel.KEY_RETURN):
                if self.joueur == 0 : self.affichage = 2
                else : self.affichage = 1
          
        
    def draw(self):
        if self.affichage==0:
            pyxel.cls(3)
            pyxel.blt(48,48,0,0,64,32,32,0)
            pyxel.text(38,28,"Pyxel Knights",7)
            pyxel.text(42,100,"Press start",7)
        elif self.affichage==1:
            pyxel.cls(0)
            pyxel.text(32,60,"Player 1's turn",7)
        elif self.affichage==2:
            pyxel.cls(0)
            pyxel.text(31,60,"Player 2's turn",7)
        elif self.affichage==3:
            pyxel.cls(0)
            self.vision = generate_vision(self.carte,self.joueur)
            for x in range(0,16):
                for y in range(0,16):
                    if not(0<=x-self.offset[0]<self.wid  and 0<=y-self.offset[1]<self.hei): continue
                    if self.vision[y-self.offset[1]][x-self.offset[0]] :
                        pyxel.blt(x*8,y*8,0,self.ecran[y-self.offset[1]][x-self.offset[0]],self.fond,8,8)
            
            for x in range(len(self.carte[0])):
                for y in range(len(self.carte)):
                    a=self.carte[y][x] 
                    if a != None and self.vision[y][x]:
                        a.update(self.offset)
            for y in range(16):
                for x in range(16):
                    if not(0<=x-self.offset[0]<self.wid  and 0<=y-self.offset[1]<self.hei):
                        pyxel.rect(x*8,y*8,8,8,6)
                    elif not(self.vision[y-self.offset[1]][x-self.offset[0]]):
                        pyxel.blt(x*8,y*8,0,40,self.fond,8,8)
    
            pyxel.blt(0,0,0,0,240,16,16,7)
            pyxel.text(13,6,str(self.gold[self.joueur]),0)
            pyxel.blt(0,16,0,0,224,16,16,7)
            if self.bat == None : a=0
            else : a=self.bat.vie
            pyxel.text(15,22,str(a),0)

            self.curseur.update(self.offset)

        elif self.affichage==4:
            pyxel.cls(0)
            pyxel.text(35,60,"Player "+str(self.joueur+1)+" win !",7)
App()

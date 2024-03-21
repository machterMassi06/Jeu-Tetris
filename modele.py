### Le MODELE(etp2)
##modele
import random
# la constante des formes
#list(list(tuples)) qui contient les coords relatives des formes de jeu
# Rq: on a ajouter quelques formes aux formes proposées 
LES_FORMES = [[(-1,1),(-1,0),(0,0),(1,0)],[(-1,0),(0,0),(0,1),(1,1)],[(-1,0),(0,0),(-1,1),(-2,1)],[(-1,0),(0,0),(1,0),(1,1)],[(0,1),(-1,1),(0,0),(1,1)],[(0,0),(1,0),(0,1),(1,1)],[(0,3),(0,2),(0,1),(0,0)],[(0,0)],[(0,0),(0,1),(1,1),(2,1),(2,0)]]

class ModeleTetris:
    '''
        La class modele est constitué de deux element principale :
        *le terrin qui est une matrice d'entiers (list(list))
        *les carrée des formes qui se pose en bas
        *la forme qui tombe
    '''
    
    def __init__(self,nblig=19,nbcol=14):
        
        ''' ModeleTetris , int ,int -> ModeleTetris

          elle prend en parametre un nombre de ligne et un nbr de colonnes
          que nous initialison par default en cas ou ce n'est pas priciser,
          ce constructeur crée une instance de l'objet ModelTetris
        
        '''
        # 5 lignes sont ajoutée(le loncer de formes ,qui est la zone grisé)
        self.__haut=nblig+5
        self.__larg=nbcol
        
        ## l'indice de la premiere ligne  de la zone noir
        # on a choisie self.__base a 5 au lieu de 4 pour que l'affichage s'adapte aux formes qu'on a ajouté 
        self.__base=5
        ##definir la matrice qui contienne le terrain de jeu
        l=[]
        for i in range (self.__haut):#on parcure les lignes
            l2=[]
            ##les quatres premieres lignes(les lignes grisé) sont initialiser a -2
            if i<5:
                for j in range(self.__larg):
                    l2.append(-2)
                l.append(l2)
            else :
                #les autres lignes du terrain sont initialiser a -1
                for j in range(self.__larg):
                    l2.append(-1)
                l.append(l2)
                
        self.__terrain=l
        self.__forme=Forme(self)#initialisation a une nouvelle forme
        self.__suivante=Forme(self)#initialisation de la forme suivante 
        self.__score=0#initialisation du score a 0
        
    
    def get_largeur(self):
        ''' ModeleTetris -> int
            elle retourne la largeur de terrain (nbr de columns)
        '''
        return self.__larg
    
    def get_hauteur(self):
        ''' ModeleTetris -> int
            elle retourne la hauteur de terrain (nbr de lignes)
        '''
        return self.__haut
    
    def get_valeur(self,nl,nc):
        ''' ModeleTetris , int ,int -> int
            retourne la valeur du terrain a la case en ligne (nl)
            et colonne (nc)
        '''
        return self.__terrain[nl][nc]
    
    def est_occupe(self,nl,nc):
        ''' ModeleTetris , int ,int -> bool
            retourne true si la case en ligne (nl) et colonne (nc) est occupée,
            false sinon.
            rmrq: une case avec une valeur negative indique qu'elle est vide(non occupée),
            c-a-d: une case avec une valeur positive elle est occupée
        '''
        
        return self.get_valeur(nl,nc)>=0
    
    def fini(self):
        ''' ModeleTetris -> bool
           teste si la partie de jeu est finie : cela lorsqu'une case des cases
           la ligne noire la plus haute (celle d’indice self.__base) est occupée
        '''
        for i in range (self.get_largeur()):
            #le faite de trouver une qui est occupé la partie sera finie
            if self.est_occupe(self.__base,i):
                return True
        #si toutes les cases de la ligne la plus haute noir ne sont pas occopées 
        return False
    
    def ajoute_forme(self):
        ''' ModeleTetris -> elle pose la forme sur le terrain de jeu'''
        # a chaque coords absolue de self.__forme on
        # ajoute la valeur de sa couleur dans le terrain
        # au coordonnées correspondants
        # Rq: on ajoutant la valeur de la couleur dans le terrain la case..
        # va etre occupée 
        for tup in self.get_coords_forme():
            self.__terrain[tup[1]][tup[0]]=self.__forme.get_couleur()
    
    def forme_tombe(self):
        ''' ModeleTetris -> bool
            fait tomber la forme (self.__forme) sur le terrain;
            si il y'a eu de collision alors la forme va etre ajoutée dans le terrain.
            *retourne true si il ya eu collision ,false sinon
        '''
        self.supprime_lignes_completes()
        self.__forme.tombe() #on fait tomber la forme
        
        if self.__forme.collision():#on teste si y'a de collision 
            # alors on ajoute la forme alors sur le terrain 
            self.ajoute_forme()
            # alors self.__forme prend la forme suivante 
            self.__forme=self.__suivante
            # on reinitialise la forme suivante a une nouvelle forme 
            self.__suivante=(Forme(self))
            return True
        return False
    
    def get_couleur_forme(self):
        ''' ModeleTetris -> retourne la couleur de la forme (self.__forme)'''
        return self.__forme.get_couleur()
    
    def get_coords_forme(self):
        ''' ModeleTetris -> list(int,int)
            elle retourne les coords absolue de la forme (c-a-d self.__forme)
        '''
        return (self.__forme.get_coords())
    
    def forme_a_gauche(self):
        ''' ModeleTetris -> None
            elle demande a la forme de se deplacer a gauche si possible
        '''
        self.__forme.a_gauche()
    
    def forme_a_droite(self):
        ''' ModeleTetris -> None
            elle demande a la forme de se deplacer a gauche si possible
        '''
        self.__forme.a_droite()
    
    def forme_tourne(self):
        '''ModeleTetris -> None
            elle demande a la forme de se tourner de 90 degrée si c possible
        '''
        self.__forme.tourne()
    
    def est_ligne_complete(self,lig):
        ''' ModeleTetris,Int -> Bool
            elle teste si la ligne a l'indice lig est complete '''
        # une ligne est complete si toutes ses cases sont occupee
        for i in range(self.get_largeur()):
            if not (self.est_occupe(lig,i)) :
                return False
        return True
    
    def supprime_ligne(self,lig):
        ''' ModeleTetris , iNT->none
            elle modifie le modele car elle suprime la ligne d'indice lig
            ,de ce fait , toutes les autres lignes descendent d'un cran(d'une ligne)
        '''
        #on supprime la ligne a l'indice lig
        for i in range(self.get_largeur()):
            self.__terrain[lig][i]=-1
        # on fais decendre les autres d'un cran   
        for i in range(lig,self.__base,-1):
           for j in range(self.get_largeur()):
               self.__terrain[i][j]=self.__terrain[i-1][j]
           
        
        
    def supprime_lignes_completes(self):
        '''ModeleTetris -> none
            elle modifie le modifie de sorte qu'elle supprimme toutes les lignes completes
        '''
        for i in range(self.__base,self.get_hauteur()):
            if (self.est_ligne_complete(i)):
                self.supprime_ligne(i)
                self.__score+=1
    
    def get_score(self):
        ''' ModeleTetris -> int
            elle retourne le score'''
        return self.__score
    
    def get_coords_suivante(self):
        '''ModeleTetris->list(tup(int,int))
            elle retourne les coords relatives de la forme suivante'''
        return self.__suivante.get_coords_relatives()
    def get_couleur_suivante(self):
        ''' ModeleTetris -> Int
            elle retourne la couleur de la forme suivante
        '''
        return self.__suivante.get_couleur()
    
    def reinitialisation(self):
        
        ''' ModeleTetris -> ModeleTetris
        elle retourne une nouvelle instance du modele'''
        return ModeleTetris()

##la forme
from random import randint
class Forme :
    '''
        la class Forme c'est celle qui prend en charges tous ce qui est forme
        dans le jeu , elle est relier a la classe modele car elle prend une instance
        de "ModeleTetris" en parametre.
        
   '''
    def __init__(self,modele):
        ''' Forme , ModeleTetris -> Forme
            c'est le constructeur de la classe Forme
            il prend en parametre une instance de la classe Modeletetris
            il cree une forme
        '''
        #l'attribut qui contient l'instance de Modele de jeu 
        self.__modele=modele
        ind=random.randint(0,len(LES_FORMES)-1) # tirez au hasard un indice entre 0 et len(LES_FORMES)
        #initialison l'attribut de couleur a 0 
        self.__couleur=ind
        #initialisation des coords relatives de la forme
        self.__forme=LES_FORMES[ind]
        
        #les attributes self.__x0 et self.__y0 representant les cordonnées de pivot dans le terrain
        self.__x0=self.__modele.get_largeur()//2 #elle est initialiser au milieu d'axe principale(axe des x)
        self.__y0=0 #initialiser a l'indice de la premiere ligne grise de terrain
    
    def get_couleur(self):
        ''' Forme -> retourne la couleur de la forme courante .
        '''
        return self.__couleur
    
    def get_coords(self):
        ''' Forme -> list((int,int))
             elle retourne la liste des tuples representant les coordonées absolue de la
             forme dans le terrain de jeu.
        '''
        l=[]
        # l est une liste qui contient les cords absolue de la forme dans le terrain
        # on fait refference a l'indice du pivot (x0 et y0)
        for tup in self.__forme:
            l.append((tup[0]+self.__x0,tup[1]+self.__y0))
        return l
    
    def collision(self):
        ''' Forme -> bool
            elle retourne true si la forme doit se poser ,false sinon
        '''
        for tup in self.get_coords():
            # y a collision lorsque pour l’une des coordonnees absolues de la forme
            # soit arriver a la derniere ligne de terrain
            # soit elle est au dessus d'une cellule deja occupée
            if (tup[1]==self.__modele.get_hauteur()-1) or self.__modele.est_occupe(tup[1]+1,tup[0]):
                # alors la forme peut doit se poser
                return True
        
        return False
    
    def tombe(self):
        ''' Forme -> bool
            elle fait tomber la forme d'une ligne c-a-d elle change la valeur de (self.__y0)
            a condition : si il y'a pas de collision
        '''
        if not(self.collision()):
            self.__y0+=1
            return False
        else:
            # retourne True si il y'a une collision c-a-d la forme n'a pas bougé
            return True
    
    def position_valide(self):
        ''' Forme -> bool
            elle teste si les coords (x,y) dela forme son valide
            rq: une coord (x,y) est valide si x,y sont dans l'intervalle valide
            c-ad si x entre (0,largeur-1) et y entre (0,hauteur-1)
        '''
        #on recupere les coords absolue de la forme
        coords=self.get_coords()
        # Rq: tup[0] respresente le x, tup[1] represente le y
        for tup in coords:
            #si le x ou y n'est pas dans le bon intervalle
            # on retourne false
            if not( tup[0] in range(self.__modele.get_largeur())) or not(tup[1] in range(self.__modele.get_hauteur())):
                return False
            if self.__modele.est_occupe(tup[1],tup[0]):
                # donc si elle est occupee en (x,y) on retourne False
                return False
                    
        #sinon on retourne True( si toutes les coords sont valides)
        return True
        
    def a_gauche(self):
        ''' Forme -> none
            elle deplace la forme d'une colonne vers la gauche(si possible)
        '''
        # on deplace vers la gauche c-a-d on decrement le self.__x0 de 1
        self.__x0-=1
        # si la nouvelle position de la forme ni pas valide
        # alors on reprend la valeur initiale de self.__x0
        if not(self.position_valide()):
            self.__x0+=1
    
    def a_droite(self):
        ''' Forme -> none
            elle deplace la forme d'une colonne vers la droite(si possible)
        '''
        # on deplace vers la droite c-a-d on increment le self.__x0 de 1
        self.__x0+=1
        # si la nouvelle position de la forme ni pas valide
        # alors on reprend la valeur initiale de self.__x0
        if not(self.position_valide()):
            self.__x0-=1
    
    def tourne(self):
        ''' Forme -> none
            elle fait tourner une forme de 90 deg si c'est possible
            et cela on modifiant la liste des coords relatives de la forme
        '''
        forme_prec=self.__forme # on memorise la liste initiale des coords..
        self.__forme=[]
        # ..dans la variable forme_prec
        for i in range(len(forme_prec)) :
            #les coords relativs (x,y) deviennent (-y,x)
            self.__forme.append((-forme_prec[i][1],forme_prec[i][0]))
             
        if not(self.position_valide()):
            # si la nouvelle forme n'est pas valide alors on reprend sa valeur initiale
            self.__forme=forme_prec
    
    def get_coords_relatives(self):
        ''' Forme -> list(tuple(int,int))
            elle retourne une copie des coords relatives de la forme '''
        return self.__forme
    

    
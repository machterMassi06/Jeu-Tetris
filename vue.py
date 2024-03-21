import tkinter
import modele

##definition des constantes

DIM=30 # taille d'une cellule du tetris(un carree)
SUIVANT=7#constante utiles pour affiché la forme suivante
TOP_SCORE=0
#définition des coulerus qui seront utiliser dans le jeu (9couleurs !=tes)
COULEURS= ["red","blue","green","yellow","orange","purple","pink","magenta","cyan","dark grey","black"]

#la classe vueTetris
class VueTetris:
    ''' cette class modelise tous ce qui est affichage et graphisme,la fenetre de
        de jeu c-a-d l'interface et le contact avec l'utilisateur '''
    
    def __init__(self,mod):
        ''' VueTetris,ModeleTetris -> VueTetris
            le constructeur de la classe de VueTetris prend en pamrametre une
            instance de la classe ModeleTetris ,
            elle construit le window principale(la fenetre) de l'application et
            toutes ses composantes.
        '''
        self.__modele=mod
        #la fenetre principale de jeu
        self.__fen=tkinter.Tk()
        self.__fen.title("Tetris")
        # le canvas
        larg=self.__modele.get_largeur()*DIM #largeur de canvas
        haut=self.__modele.get_hauteur()*DIM # hauteur de canavas 
        self.__can_terrain=tkinter.Canvas(self.__fen,width=larg,height=haut)
        self.__can_terrain.pack(side="left")
        # mettre les objets dans une liste de liste 
        l=[]
        for i in range (self.__modele.get_hauteur()):
            l2=[]
            for j in range (self.__modele.get_largeur()):
                l2.append(self.__can_terrain.create_rectangle(j*DIM, i*DIM, (j+1)*DIM, (i+1)*DIM, fill=COULEURS[self.__modele.get_valeur(i,j)],outline=COULEURS[self.__modele.get_valeur(i,j)]))
            l.append(l2)
        
        self.__les_cases=l
        
        #le frame pour le boutoun quitter et les autres element(score...)
        fr=tkinter.Frame(self.__fen)
        fr.pack(side="left")
        #label pour affiché le game over lorsque la partie est finie
        self.__lbl_game=tkinter.Label(fr,text="",fg="red")
        self.__lbl_game.pack()
        #btn commencer ,reprend,restart , recommencer
        self.__btn_crpr=tkinter.Button(fr,text="Commencer",command=self.met_a_jour_btn)
        self.__btn_crpr.pack()
        
        self.__etat=False#etat de jeu
        
        
        # afficher l'étiquete forme suivante
        lbl_affich_fsuivante=tkinter.Label(fr,text="Forme suivante:")
        lbl_affich_fsuivante.pack()
        #canvas pour afficher la forme suivante
        DIM2=SUIVANT*DIM # largeur et hauteur de canvas 
        self.__can_fsuivante=tkinter.Canvas(fr,width=DIM2,height=DIM2)
        self.__can_fsuivante.pack()
        l=[]
        for i in range(SUIVANT):
            l2=[]
            for j in range(SUIVANT):
                l2.append(self.__can_fsuivante.create_rectangle(j*DIM, i*DIM, (j+1)*DIM, (i+1)*DIM, fill=COULEURS[-1]))
            l.append(l2)
        self.__les_suivants=l#on memorise les objets du canvas(forme_suivante) dans list(list)
        # label de score 
        self.__lbl_score=tkinter.Label(fr,text="Score : 0")
        self.__lbl_score.pack()
        
        #btn quitter le jeu
        btnquitter=tkinter.Button(fr,text="Au revoir",command=self.__fen.destroy)
        btnquitter.pack()
        
        
    
    def fenetre(self):
        ''' VueTetris -> retourne l'instance Tk de l'application'''
        return self.__fen
    
    def dessine_case(self,i,j,coul):
        ''' VueTetris ,int,int,int-> none
            elle remplit la case en ligne i et la colonne j de la couleur a l'indice
            coul
        '''
        self.__can_terrain.itemconfigure(self.__les_cases[i][j],fill=COULEURS[coul])
    
    def dessine_case_suivante(self,x,y,coul):
        ''' VueTetris ,int,int,int-> none
            elle remplit la case en ligne i et la colonne j  avec la couleur coul
            dans le canvas qui sert a afficher la forme suivante 
        '''
        self.__can_fsuivante.itemconfigure(self.__les_suivants[x][y],fill=COULEURS[coul])
    
    def nettoie_forme_suivante(self):
        ''' VueTetris -> none
            elle modifie le self__can_fsuivante
            elle remet du noir sur tous les carres de self.___can_fsuivante'''
        for i in range(SUIVANT):
            for j in range(SUIVANT):
                self.__can_fsuivante.itemconfigure(self.__les_suivants[i][j],fill=COULEURS[-1])
                
    def dessine_terrain(self):
        ''' VueTetris -> none
            elle mis a jour la couleur deu terrain en fonction des valeurs de modeles
        '''
        for i in range (len(self.__les_cases)):
            for j in range (len(self.__les_cases[i])):
                self.dessine_case(i,j,self.__modele.get_valeur(i,j))
    
    def dessine_forme(self,coords,couleur):
        ''' VueTetris ,list(int,int),int->none
            remplit de couleur les cases dont les coordonnees sont donnee dans coords
            elle permet de faire apparaitre une forme dans le terrain '''
        for tup in coords:
            self.dessine_case(tup[1],tup[0],couleur)
            
    def dessine_forme_suivante(self,coords,coul):
        ''' VueTetris ,list(int,int),int->None
            remplit de coul la couleur des cases dont les coordonnees (coords) passee en
            parametre.
            elle permet de faire apparaitre LA forme suivante dans le canvas concerné '''
        
        self.nettoie_forme_suivante()#on nettoie le canvas (mettre de black pour toutes les cases)
        
        for tup in coords:#on afficher sur le panneau..
            #..la forme suivante avec sa couleur
            self.dessine_case_suivante(tup[1]+3,tup[0]+3,coul)
    
    def met_a_jour_score(self,val):
        '''VueTetris , int->none
            affiche val dans le teexte du Label score
            c-a-d elle mis a jour l'affichage  de score'''
        self.__lbl_score["text"]="Score : "+str(val)
        
        
    def met_a_jour_btn(self):
        
        '''VueTetris -> none
        elle modifie un composant:(self.__btn_crpr)
        elle mis a jour le button commencer , pause , reprendre et rejouer
        elle mis a jour le boolean self.__etat (etat de jeu pause ou nn)
        '''
        if self.__btn_crpr["text"]=="Commencer" or self.__btn_crpr["text"]=="Reprendre" or self.__btn_crpr["text"]=="Recommencer":
            
            self.__btn_crpr["text"]="Pause" #on met le text de botton a pause
            #pour permettre a l'utilisateur de igée le jeu (le mettre en pause)
            
            self.change_etat() # alors on reprend le jeu cad le jeu n'est pas en pause
        else :
            # si il a cliquez sur pause
            #on remmet le btn a raprendre et l'attribut __etat a false..
            #c-a-d la partie est en pause
            # et le text de button a reprendre pour permettre au joueur de reprendre la partie 
            self.__btn_crpr["text"]="Reprendre"
            self.change_etat()
      
    def change_etat(self):
        '''VueTetris -> none
        elle change l'etat de jeu c-a-d elle modifie le self.__etat'''
        self.__etat=not(self.__etat)
    
    def etat_de_jeu(self):
        ''' VueTetris -> boolean
            elle retourne l'etat de jeu en pause(False) ou nn(True)
        '''
        return self.__etat
    
    def botton_crpr(self):
        ''' VueTetris -> BTN
            elle retourne le boutton (commencer, pause...)
        '''
        return self.__btn_crpr
    
    def affiche_game_over(self):
        ''' VueTetris -> none
            elle modifie le label __lbl_game a game over
        '''
        self.__lbl_game["text"]='Game Over !'
        
    def efface_game_over(self):
        ''' VueTetris -> none
            elle modifie le label __lbl_game(elle efface game over)
        '''
        
        self.__lbl_game["text"]=''
        
    def reinitialisation(self,mod):
        ''' VueTetris,ModeleTetris ->none
            elle reinistialise self.__modele au nouveau modele (mod)passée en parametre
        '''
        self.__modele=mod
    
        
        
        
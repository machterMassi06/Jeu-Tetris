###le controleur
import vue
import modele
import time
##controleur
class Controleur:
    def __init__(self,mod):
        ''' Controleur , ModeleTetris -> Controleur
            c'est le constructeur de la classe Controleur:
            il prend une instance de Modele de jeu et il cree une instance de
            la vue (VueTetris)   
        '''
        self.__tetris=mod
        # il cree une instance de vueTetris
        # il passe le modele en parametre a la vue 
        self.__vue=vue.VueTetris(self.__tetris)
        
        #recuperation et enregistrement de la fenetre de l'application dans un attribut
        self.__fen=self.__vue.fenetre()
        # faire le lien entre les appui de l'utilisateur et 
        # aux actions de deplacement(gauche et droite)
        self.__fen.bind("<Key-Left>",self.forme_a_gauche)
        self.__fen.bind("<Key-Right>",self.forme_a_droite)
        # deplacement vite vers le bas 
        self.__fen.bind("<Key-Down>",self.forme_tombe)
        #tomber directement la forme en cliquant sur la barre d'espace
        self.__fen.bind("<space>",self.forme_tombe_directement)
        #lier la touche entrée au boutton commencer ,pause...
        self.__fen.bind("<Return>",self.change_btn)
        # faire tourner la forme
        self.__fen.bind("<Key-Up>",self.forme_tourne)
        #demander a la vue de dessiner la forme du modele
        # suivant ses coords absolue dans le terrain 
        self.__vue.dessine_forme(self.__tetris.get_coords_forme(),self.__tetris.get_couleur_forme())
        
        self.__delai=280 # nbr de milliscnds d'attente a la descente d'une forme
        self.joue()
        self.__fen.mainloop()#lancez la boucle d'ecoute des evnmnts
        
    def joue(self):
        ''' Controleur -> None
        Boucle principale de jeu,elle fait tomber une forme d'une
        ligne '''
        if not self.__tetris.fini() :
            self.affichage()
            self.__fen.after(self.__delai,self.joue)
        else:
            
            self.__vue.affiche_game_over()
            #si la partie finie
            self.__vue.change_etat() #demander a la vue de changer l'etat de jeu..
            # c-ad la partie est finie dans elle mis l'etat de jeu a false
            
            #alors on modifie le btn pour afficher a (recommencer)
            self.__vue.botton_crpr()['text']="Recommencer" # on mis le btn a recommencer
            #pour permettre au joueur de rejouer on cliquant sur le btn recommencer
            self.__tetris=self.__tetris.reinitialisation()#reinistalisation du modele a un nouveau modele
            self.__vue.reinitialisation(self.__tetris)#reinistialisation de la vue avec le nouveau modele
            
            self.joue()#alors on reinistialise le jeu, c-a-d on attend si le joueur a choisie de recommencer la partie 
    
    def affichage(self):
        ''' Controleur -> None
            le controleur indique au modele qu’il doit faire tomber la forme,
            puis il demande a la vue de redessiner son terrain,puis redessiner la forme
            demande a la vue de redissiner la forme suivante.
            '''
        if self.__vue.etat_de_jeu():#si la partie n'est pas en pause (controle d'etat de jeu)
            self.__vue.efface_game_over()#efface le label game_over
            self.__vue.dessine_forme_suivante(self.__tetris.get_coords_suivante(),self.__tetris.get_couleur_suivante())
            boole=self.__tetris.forme_tombe()# fait tomber la forme
            if boole:#si il a eu collision et la forme elle s'est posée
                # alors on remmett l'attribut self.__delai a sa valeur initiale
                self.__delai=280
                # demander a la vue d'afficher la forme suivante 
                self.__vue.dessine_forme_suivante(self.__tetris.get_coords_suivante(),self.__tetris.get_couleur_suivante())
            self.__vue.dessine_terrain() # dessiner le terrain
            #redissiner la forme sur le terrain de jeu 
            self.__vue.dessine_forme(self.__tetris.get_coords_forme(),self.__tetris.get_couleur_forme())
            #mettre a jour le score
            self.__vue.met_a_jour_score(self.__tetris.get_score())
        
        

        
            
    def forme_a_gauche(self,event):
        ''' Controleur , event -> None
            elle demande au modele qu'il deplace la forme a gauche'''
        self.__tetris.forme_a_gauche()
        
    def forme_a_droite(self,event):
        ''' Controleur , event -> None
            elle demande au modele qu'il deplace la forme a droite'''
        self.__tetris.forme_a_droite()
    
    def forme_tombe(self,event):
        
        ''' Controleur -> None 
            elle modifie la valeur de l'attribut self.__delai
            cela pour faire tomber vite la forme '''
        self.__delai=100
    
    def forme_tombe_directement(self,event):
        ''' Controleur -> None 
            elle modifie la valeur de l'attribut self.__delai
            cela pour faire tomber directement la forme dans le terrain,
            cette methode est reliée a l'evenement cliquez sur espace
        '''
        self.__delai=0
    
    def forme_tourne(self,event):
        ''' Controleur -> None
            elle demande au modele de faire tourner la forme de
            90 degree si c'est possible'''
        self.__tetris.forme_tourne()
    
    def change_btn(self,event):
        ''' Controleur , event -> rien
            elle demande ala vue de mettre a jour le btn commencer,pause...'''
        self.__vue.met_a_jour_btn()

##le scripte principale
if __name__ == "__main__" :
    # creation du modele
    tetris = modele.ModeleTetris()
    # cr´eation du controleur. c'est lui qui cree la vue
    # et lance la boucle d’ecoute des evts
    ctrl = Controleur(tetris)
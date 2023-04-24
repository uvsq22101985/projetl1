#programme fourmis de langton
import tkinter as tk
from tkinter import *

#Cases de la grille
cases = []
# constante de proportionnalité
n = 125
# configuration du canevas 
config_courante = []
# placement de la fourmi 
x_fourmi = 0 
y_fourmi = 0 
# position de la tête 
position_tete_fourmi = 0 
# pause 
var_pause = False
boutton_pause = 0 
# vitesse
vitesse = 1000
#########################################
# fonctions
def fourmi_de_langton(n):
    configuration_courante_vide(n)

n = 30

config_courante = []

#Variables de position et d'orientation de la fourmie
x_fourmi = 0
y_fourmi = 0
variable_orientation = ""

#Variable pour mettre en pause l'automate
var_pause = False
#Variable permettant l'execution automatique ou permettant les etapes une a une
auto = False


def jeu_Fourmi():
    '''Fonction intermédiaire permettant le lancement du jeu'''
    
    widget_a_cacher()   
    configuration_courante_vide()
#fonction pour cacher les widgets a la lancée du jeu
def widget_a_cacher():
    
    hide(bouton_haut, True)
    hide(bouton_bas, True)
    hide(bouton_droit, True)
    hide(bouton_gauche, True)
    hide(txt_orientation, True)
    hide(txt_informatif, True)
    hide(bouton_next, True)
    hide(bouton_play, True)
    hide(bouton_pause, True)
    hide(scale_vitesse, True)
    hide(bouton_save, True)
    hide(bouton_load, True)
    hide(bouton_retour, True)

def configuration_courante_vide():
    '''Initialise la configuration courante vide du jeu'''
    global config_courante

    for i in range(n):     
        config_courante.append([0 for x in range(n)])

    return init_grille()  #initialisation de la grille

def init_grille():
    '''Fonctions qui permet l'initialisation de la grille'''
    global cases

    c = HAUTEUR / n  #calcul du nombre de cases dans la grille proportionnellement a n
    for ligne in range(n):
        transit = []
        for colonne in range(n): #creation des cases
            transit.append(canevas.create_rectangle(colonne * c + 2, ligne * c + 2, (colonne + 1) * c + 2, (ligne + 1) * c + 2, fill="snow", outline="darkSeaGreen1"))
        cases.append(transit)

def maj_grille():
    '''Fonction qui met à jour la grille en fonction de la configuration courante au sein du jeu'''
    
    for ligne in range(n):
        for colonne in range(n):
            if config_courante[ligne][colonne] == 0:                        #0 represente une case blanche
                canevas.itemconfigure(cases[ligne][colonne], fill='snow')   #Changement de la couleur de la case en noir
            if config_courante[ligne][colonne] == 1:                        #1 represente une case noire
                canevas.itemconfigure(cases[ligne][colonne], fill='black')  #Changement de la couleur de la case en noir

def creation_fourmi():
    '''Fonction permettant le placement aléatoire d'une fourmi et pour aller plus loin, permet de choisir l'orientation de la fourmi'''
    global config_courante, x_fourmi, y_fourmi

    #on determine des coordonnees aleatoires pour la fourmi
    x_fourmi = randint(0,n-1) 
    y_fourmi = randint(0,n-1)

    #on modifie la configuration courante pour afficher la position de la fourmi et on l'affiche en mettant a jour la grille
    config_courante[y_fourmi][x_fourmi] += 1
    maj_grille()

    #On cache le bouton permettant la creation d'une fourmi
    hide(bouton_creer_fourmi, True)

    #On appelle la fonction affiche_fleche pour permettre a l'utilisateur de choisir l'orientation de la fourmi
    affiche_fleches()

def hide(widget, presence:bool):
    '''Fonction permettant de cacher ou d'afficher un widget'''

    if presence == True : #Si le widget est present, on le cache avec la methode .grid_remove() qui permet de garder en memoire les options de grilles
        widget.grid_remove()
    else :
        widget.grid()     #Sinon, on affiche le widget en utilisant la methode simple .grid()

def affiche_fleches():
    '''Fonction permettant de d'afficher les flèches avec le label attribué pour choisir l'orientation de la fourmi'''

    hide(txt_orientation, False)
    hide(bouton_haut, False)
    hide(bouton_bas, False)
    hide(bouton_droit, False)
    hide(bouton_gauche, False)

def cache_fleche():
    '''Fonction permettant de cacher les boutons fleches et le label associe'''
    
    hide(bouton_haut, True)
    hide(bouton_bas, True)
    hide(bouton_droit, True)
    hide(bouton_gauche, True)
    hide(txt_orientation, True)

def changement_txt(label, txt_modif:str):
    '''Fonction permettant de changer le texte d'un label'''

    label.configure(text=txt_modif) 

def widget_a_afficher():
    '''Fonction permettant d'afficher les boutons du jeu'''

    hide(txt_informatif, False)
    hide(bouton_next, False)
    hide(bouton_play, False)
    hide(bouton_pause, False)
    hide(scale_vitesse, False)
    hide(bouton_save, False)
    hide(bouton_load, False)
    hide(bouton_retour, False)

def orientation_fourmi(direction:str):
    '''Fonction permettant d'attribuer l'orientation choisi par l'utilisateur à la fourmi'''
    global variable_orientation
    
    #On cache les boutons fleches et le label associé après la sélection de l'orientation
    cache_fleche()

    #On affiche les boutons necessaires a la suite du jeu
    widget_a_afficher()

    #On appelle la fonction changement_txt en fonction de l'orientation choisie par l'utilisateur et on modifie la variable de l'orientation de la fourmi
    if direction == "haut":
        changement_txt(txt_informatif, "La fourmi démarre\n par le haut")
        variable_orientation = "haut"
    elif direction == "bas":
        changement_txt(txt_informatif, "La fourmi démarre\n par le bas")
        variable_orientation = "bas"
    elif direction == "droite":
        changement_txt(txt_informatif, "La fourmi démarre\n par la droite")
        variable_orientation = "droite"
    else :
        changement_txt(txt_informatif, "La fourmi démarre\n par la gauche")
        variable_orientation = "gauche"

def deplacement():
    ''' Fonction permettant le déplacement de la fourmi en fonction du choix de l'orientation par l'utilisateur'''
    global x_fourmi, y_fourmi, config_courante, variable_orientation
        
    if var_pause == False :     #Si la variable pause n'est pas en position False, le deplacement peut s'effectuer
        if variable_orientation == "haut":
            y_fourmi -= 1
            verif_coordonnee()  #On verifie les coordonnees pour savoir si la fourmi est a proximite d'un cote
            if config_courante[y_fourmi][x_fourmi] == 0:    #Si on est sur une case blanche
                variable_orientation = "droite"             #On change l'orientation
                config_courante[y_fourmi][x_fourmi] += 1    #On change la couleur en noir
            else:
                config_courante[y_fourmi][x_fourmi] -= 1    #Sinon, la case est noir, on change la couleur en blanc
                variable_orientation = "gauche"             #On change l'orientation
                
        elif variable_orientation == "bas":
            y_fourmi += 1
            verif_coordonnee()
            if config_courante[y_fourmi][x_fourmi] == 0:
                config_courante[y_fourmi][x_fourmi] += 1
                variable_orientation = "gauche"
            else :
                config_courante[y_fourmi][x_fourmi] -= 1
                variable_orientation = "droite"

        elif variable_orientation == "droite":
            x_fourmi += 1
            verif_coordonnee()
            if config_courante[y_fourmi][x_fourmi] == 0:
                config_courante[y_fourmi][x_fourmi] += 1
                variable_orientation = "bas"
            else :
                config_courante[y_fourmi][x_fourmi] -= 1
                variable_orientation = "haut"

        elif variable_orientation == "gauche":
            x_fourmi -= 1
            verif_coordonnee()
            if config_courante[y_fourmi][x_fourmi] == 0:
                config_courante[y_fourmi][x_fourmi] += 1
                variable_orientation = "haut"
            else :
                config_courante[y_fourmi][x_fourmi] -= 1
                variable_orientation = "bas"
        
        maj_grille()    #On met a jour la grille pour prendre en compte les deplacement

        if auto == True:      #Si la variable automate est en position True, cela signifie que l'automate doit etre actif
            #On rappelle la fonction deplacement de maniere automatique en prenant en compte la vitesse recuperee par le scale
            canevas.after(scale_vitesse.get(), deplacement)

def verif_coordonnee():
    '''Fonction permettant de modifier les coordonnees si la fourmi doit changer de cote'''
    global x_fourmi, y_fourmi

    if y_fourmi < 0:        #Si la coordonnee y est inferieur a 0, alors la fourmi passe en bas 
            y_fourmi = n-1

    if y_fourmi > n-1:      #Si la coordonnee y est superieur a n-1, alors la fourmi passe en haut 
            y_fourmi = 0

    if x_fourmi > n-1:      #Si la coordonnee x est superieur a n-1, alors la fourmi passe a gauche 
            x_fourmi = 0

    if x_fourmi < 0:        #Si la coordonnee x est inferieur a 0, alors la fourmi passe a droite
            x_fourmi = n-1

def automate():
    '''Fonction activant l'automate du jeu'''
    global var_pause, auto

    #On modifie la variable pause en False pour activer le deplacement automatique
    var_pause = False
    auto = True  
    deplacement()

def pause():
    '''Fonction permettant d'arreter l'automate'''
    global var_pause, auto

    #On modifie la variable pause en True pour dire que l'automate doit se mettre en pause
    var_pause = True

def next():
    '''Fonction permettant de passer les etapes une a une'''
    global auto, var_pause

    var_pause = False
    auto = False
    deplacement()

def save():
    '''Fonction permettant de sauvegarder la partie en cours dans un fichier sauvegarde.txt'''
    
     #Creation d'un fichier sauvegarde.txt en ecriture pour y stocker la configuration courante, les coordonnees et l'orientation de la fourmi
    fic = open("sauvegarde.txt", 'w')
    
    #Boucle pour stocker les elements de la configuration courante
    for i in range(n):
        for j in range(n):
            fic.write(str(config_courante[i][j]) + "\n")

    #Ajout des coordonnees courantes et l'orientation de la fourmi a la fin du fichier txt
    fic.write(str(y_fourmi) + '\n')
    fic.write(str(x_fourmi) + '\n')
    fic.write(variable_orientation)

    fic.close()

def load():
    '''Fonction permettant de charger une partie sauvegardee'''
    global config_courante, x_fourmi, y_fourmi, variable_orientation

    #On ouvre le fichier en mode lecture pour recuperer la configuration courante, les coordonnees et l'orientation de la fourmi
    fic = open("sauvegarde.txt", 'r')

    #Boucle permettant la recuperation des elements de la configuration courante
    for i in range(n):
        for j in range(n):
            val = int(fic.readline())
            config_courante[i][j] = val     #On met a jour la configuration courante avec les valeurs de la partie a charger
    
    lignes = fic.readlines()                #On stocke dans une liste les elements restants : coordonnees et orientation de la fourmi
    x_fourmi = int(lignes[1])   
    y_fourmi = int(lignes[0])
    variable_orientation = lignes[2]
    fic.close()
    return maj_grille()                     #On met a jour la grille avec la nouvelle configuration courante

def retour(): #ENCORE EN DVPT
    '''Fonction qui permet de revenir d'une etape en arriere'''
    global config_courante, x_fourmi, y_fourmi, variable_orientation

    if config_courante[y_fourmi][x_fourmi] == 1 : #si c'est noir
        config_courante[y_fourmi][x_fourmi] = 0 #on remet la case en blanc
        if variable_orientation == "gauche":
            y_fourmi -= 1
            variable_orientation = "bas"
        elif variable_orientation == "droite":
            y_fourmi += 1
            variable_orientation = "haut"
        elif variable_orientation == "haut":
            x_fourmi += 1
            variable_orientation = "gauche"
        elif variable_orientation == "bas":
            x_fourmi -= 1
            variable_orientation = "droite "
    else :
        config_courante[y_fourmi][x_fourmi] = 1 #on remet la case en noir
        if variable_orientation == "gauche":
            y_fourmi += 1
            variable_orientation = "haut"
        elif variable_orientation == "droite":
            y_fourmi -= 1
            variable_orientation = "bas"
        elif variable_orientation == "haut":
            x_fourmi -= 1
            variable_orientation = "droite"
        elif variable_orientation == "bas":
            x_fourmi += 1
            variable_orientation = "gauche"
    
    maj_grille()

def fermer_fenetre():
    '''Fonction permettant de fermer la fenetre'''

    fenetre.destroy()

#########################################
### PARTIE PRINCIPALE
#########################################

##CREATION DES WIDGETS

#Widgets principaux

fenetre = Tk()
canevas = Canvas(fenetre, height=HAUTEUR, width=LARGEUR, highlightthickness=4, highlightbackground="ForestGreen")

#Creation d'une police de base avec mise en gras du texte
font_base = Font(family='Helvetica', size=12, weight='bold') 

#Boutons

bouton_creer_fourmi = Button(fenetre, text="Creer une fourmi", font=font_base, width=15, height=3, bg="wheat3", fg="wheat4", command=creation_fourmi)

    #Bouton play pour lancer le jeu de manière automatique
bouton_play = Button(fenetre, text="Play", font=font_base, width=10, height=3, command=automate)

    #Bouton next pour passer les étapes une à une
bouton_next = Button(fenetre, text="Next", font=font_base, width=10, height=3, command=next)

    #Bouton pause pour mettre le jeu en pause
bouton_pause = Button(fenetre, text="Pause", font=font_base, width=10, height=3, command=pause)

    #Chargement des images pour les boutons fleches
im_haut = PhotoImage(file = r"C:\Users\novan\Documents\L1\S2-python\projets\fourmi\fleche_haut.png")
im_bas = PhotoImage(file = r"C:\Users\novan\Documents\L1\S2-python\projets\fourmi\fleche_bas.png")
im_droite = PhotoImage(file = r"C:\Users\novan\Documents\L1\S2-python\projets\fourmi\fleche_droit.png")
im_gauche = PhotoImage(file = r"C:\Users\novan\Documents\L1\S2-python\projets\fourmi\fleche_gauche.png")

    #Bouton fleches
bouton_haut = Button(fenetre, image = im_haut, borderwidth=1, command= lambda : orientation_fourmi("haut"))
bouton_bas = Button(fenetre, image = im_bas, borderwidth=1, command= lambda : orientation_fourmi("bas"))
bouton_droit = Button(fenetre, image = im_droite, borderwidth=1, command= lambda : orientation_fourmi("droite"))
bouton_gauche = Button(fenetre, image = im_gauche, borderwidth=1, command= lambda : orientation_fourmi("gauche"))

    #Bouton sauvegarde
bouton_save = Button(fenetre, text="Sauvegarde", font=font_base, width=10, height=3, command=save)

    #Bouton load
bouton_load = Button(fenetre, text="Load", font=font_base, width=10, height=3, command=load)

    #Bouton retour
bouton_retour = Button(fenetre, text="Retour", font=font_base, width=10, height=3, command=retour)

    #Bouton quitter
bouton_quitter = Button(fenetre, text="Quitter", font=font_base, width=10, height=3, command=fermer_fenetre)

#Labels
txt_orientation = Label(text="Choisir l'orientation\n de la fourmi :", font=font_base, width=15, height=3, bg="wheat4", fg="wheat3", padx=15)
txt_informatif = Label(text="", font=font_base, width=15, height=3, bg="wheat4", fg="wheat3", padx=15)

#Scale pour la vitesse
scale_vitesse = Scale(fenetre, orient='horizontal', from_=0, to=500, tickinterval=100, length=400, label='Temps d\'execution (ms)')

##Placement des widgets

#Placement du canevas
canevas.grid(column=3, row=0, rowspan=4, columnspan=4)

#Placement des boutons

    #bouton pour creer une fourmi
bouton_creer_fourmi.grid(column=0, row=1, columnspan=2, rowspan=2, padx=5)

    #bouton pour choisir l'orientation
bouton_bas.grid(column =1, row = 1, rowspan=2, sticky="s")
bouton_haut.grid(column =1, row = 2, rowspan=2, sticky="n")
bouton_droit.grid(column =2, row = 2)
bouton_gauche.grid(column =0, row = 2)

def fourmi_langton():


###BOUCLE PRINCIPALE
jeu_Fourmi()
fenetre.mainloop()

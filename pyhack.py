#!/usr/bin/env python3
"""
essai de nethack
"""
from random import randint
import sys


def plateau_jeu():
    """
    construit l'arrière plan du jeu
    """
    tableau = [[" "] + 100*["_"]]
    for _ in range(30):
        ligne = ["|"]
        for _ in range(100):
            ligne.append('#')
        ligne.append("|")
        tableau.append(ligne)
    tableau.append([" "] + 100*["—"])
    return tableau


def partie_alignee(ordonnees_salle1, ordonnees_salle2):
    """
    retourne un booelien si il y une partie alignée entre les deux salles
    et retourne aussi les ordonnees de la partie alignee des deux salles
    """
    ordonnees = max(ordonnees_salle1[0], ordonnees_salle2[0]), \
    min(ordonnees_salle1[1], ordonnees_salle2[1])
    if ordonnees[0] < ordonnees[1]:
        return True, ordonnees
    else:
        return False, None


def caracteristiques_aleatoires(limite_abscisse, limite_ordonnee):
    """
    retourne les coordonnees du premiers sommet de la salle_aleatoire
    et sa hauteur et sa largeur de notre salle aleatoire qui doit etre
    limité par limite_abscisse et limite_ordonnee
    """
    coordonnees = randint(int((limite_abscisse[0])), int((limite_abscisse[1] + \
    limite_abscisse[0])/2)), randint(int((limite_ordonnee[0])), \
    int((limite_ordonnee[1] + limite_ordonnee[0])/2))
    hauteur = randint(coordonnees[1], limite_ordonnee[1]) - coordonnees[1]
    largeur = randint(coordonnees[0], limite_abscisse[1]) - coordonnees[0]
    #cette différence ajoutée à la largeur et la hauteur sert à ce que cette distance se compte dés
    #le point de départ et non pas du 0
    while largeur < 6 or largeur > 13:
        largeur = randint(coordonnees[0], limite_abscisse[1]) - coordonnees[0]
    while hauteur < 6 or hauteur > 13:
        hauteur = randint(coordonnees[1], limite_ordonnee[1]) - coordonnees[1]
    return coordonnees, hauteur, largeur


def distance(abcisses_salle1, abcisses_salle2):
    """
    retourne la distance entre les deux salles
    sous forme de tuple des abcisses de l'espace entre les
    deux salles
    """
    return abcisses_salle1[1], abcisses_salle2[0]


def ordonnee_couloir(ordonnees_salle1, ordonnees_salle2):
    """
    si il existe une partie alignée entre les deux salles
    on fait un couloir directe et cette fct retourne cet ordonnee
    aleatoire
    sinon on retourne deux ordonnée celui du départ et l'autre d'arrivée
    """
    if partie_alignee(ordonnees_salle1, ordonnees_salle2)[0]:
        #si il existe une partie alignée
        return randint(partie_alignee(ordonnees_salle1, ordonnees_salle2)[1][0], \
    partie_alignee(ordonnees_salle1, ordonnees_salle2)[1][1])
    else:
        #s'il n'existe pas une partie alignée on aura pas un couloir directe,
        #alors on aura besoin de deux ordonnées pour le couloir
        return randint(ordonnees_salle1[0], ordonnees_salle1[1]), \
    randint(ordonnees_salle2[0], ordonnees_salle2[1])


def nature_couloir(ordonnees_salle1, ordonnees_salle2):
    """
    retourne True si le couloir est ascendant et False si le couloir
    est descendant en partant de salle1
    """
    assert partie_alignee(ordonnees_salle1, ordonnees_salle2)[0] is False
    return ordonnees_salle2[1] >= ordonnees_salle1[0]
    #cette inégalité ça veut dire si la salle2 est en dessous
    #de la salle1


def expliquer_jeu():
    """
    explique le jeu
    """
    print("    Welcome to Nethack    ")
    print("    ")
    print("           z ==> up      ")
    print("q ==> left           d ==> right")
    print("           x ==> down      ")
    print("s ==> sortir du jeu")
    print(" le but est d'arriver à manger les dollars '$' \n & : sont des\
    monstres qu'il faut eviter\n\
    < : decrément la durée de vie\n\
    > : incrément la durée de vie\n")


class Nethack:
    """
    c'est la classe qui manipule l'etude de notre jeu
    """
    def __init__(self, plateau):
        """
        constructeur
        """
        self.plateau = plateau
        #plateau : c'est le plateau de notre jeu


    def salle_aleatoire(self, limite_abscisse, limite_ordonnee):
        """
        crèe une salle aleatoire
        """
        coordonnees, hauteur, largeur = \
        caracteristiques_aleatoires(limite_abscisse, limite_ordonnee)
        abcisse, ordonnee = coordonnees[0], coordonnees[1]
        for ligne in range(ordonnee, hauteur + ordonnee):
            for colonne in range(abcisse, largeur + abcisse):
                self.plateau[ligne][colonne] = '.'
        return coordonnees, hauteur - 1, largeur
#-1 pour faire la correction au couloir


    def dessiner_salles(self):
        """
        on met toutes les salles dans notre plateau
        retourne une liste de tuple
        chaque tuple contient les coordonnees du premier point,
         la hauteur et la largeur de la salle
        """
        limites_abcisses = [(1, 33), (33, 66), (66, 98)]
        info_salles = []
        for limite_abscisse in limites_abcisses:
            info_salles.append(self.salle_aleatoire((limite_abscisse[0], \
            limite_abscisse[1]), (2, 15)))
        for limite_abscisse in limites_abcisses:
            info_salles.append(self.salle_aleatoire((limite_abscisse[0], \
            limite_abscisse[1]), (15, 29)))
        return info_salles


    def couloir_vertical(self, colonne, depart, arrivee):
        """
        dessine un couloir verticale
        """
        for ligne in range(depart, arrivee + 1):
            self.plateau[ligne][colonne] = "."


    def couloir_horizontal(self, ligne, depart, arrivee):
        """
        dessine un couloir horizontal
        """
        for colonne in range(depart, arrivee + 1):
            self.plateau[ligne][colonne] = "."


    def dessin_couloir(self, coords_salle1, coords_salle2):
        """
        dessin un couloir entre les deux salles
        """
        abcisses_salle1, ordonnees_salle1 = (coords_salle1[0][0], coords_salle1[0][0] + \
        coords_salle1[2]), (coords_salle1[0][1], coords_salle1[0][1] + coords_salle1[1])
        abcisses_salle2, ordonnees_salle2 = (coords_salle2[0][0], coords_salle2[0][0] + \
        coords_salle2[2]), (coords_salle2[0][1], coords_salle2[0][1] + coords_salle2[1])
        distance1 = distance(abcisses_salle1, abcisses_salle2)
        if partie_alignee(ordonnees_salle1, ordonnees_salle2)[0]:
            self.couloir_horizontal(ordonnee_couloir(ordonnees_salle1, ordonnees_salle2)\
            , distance1[0], distance1[1])
        else:
            abcisse_couloir_vertical = randint(distance1[0], distance1[1])
            ordonnees_couloir = ordonnee_couloir(ordonnees_salle1, ordonnees_salle2)
            self.couloir_horizontal(ordonnees_couloir[0], distance1[0], abcisse_couloir_vertical)
            self.couloir_horizontal(ordonnees_couloir[1], abcisse_couloir_vertical, distance1[1])
            self.couloir_vertical(abcisse_couloir_vertical, ordonnees_couloir[0], \
                ordonnees_couloir[1])
            self.couloir_vertical(abcisse_couloir_vertical, ordonnees_couloir[1], \
                ordonnees_couloir[0])
        return self.plateau


    def dessin_tous_les_couloirs(self):
        """
        on met les couloirs aleatoires dans notre plateau du jeu
        """
        info_salles = self.dessiner_salles()
        self.dessin_couloir(tuple(info_salles[0]), tuple(info_salles[1]))
        self.dessin_couloir(info_salles[1], info_salles[2])
        self.dessin_couloir(info_salles[0], info_salles[4])
        self.dessin_couloir(info_salles[3], info_salles[4])
        self.dessin_couloir(info_salles[4], info_salles[5])
        self.dessin_couloir(info_salles[1], info_salles[5])


    def placer_caractere(self):
        """
        traite le mouvement du caractère
        retourne les coordonnées du caractère
        """
        #le point de debut du caractere est aleatoire
        ligne, colonne = randint(1, 29), randint(1, 99)
        while self.plateau[ligne][colonne] == "#":
            ligne, colonne = randint(1, 29), randint(1, 99)
        self.plateau[ligne][colonne] = "@"
        return ligne, colonne


    def verifie_mouvement(self, mouvement):
        """
        verifie si la destination est accessible ou non
        """
        endroits_accessibles = ".<>$"
        return self.plateau[mouvement[0]][mouvement[1]] in endroits_accessibles


    def autres_caracteres(self):
        """
        - ajoute les dollars '$' : les gains qu'il faut manger
        - < : decrémente la durée de vie par 1
        - > : incrémente la durée de vie par 1
        cette fonction ajoute les caracteres a notre plateau du Jeu
        et retourne les caracteres ajoutés
        """
        caracteres = 10*["$"] + 5*[">"] + 5*["<"]
        for caractere in caracteres:
            position_caractere = randint(1, 29), randint(1, 99)
            while self.plateau[position_caractere[0]][position_caractere[1]] != ".":
                position_caractere = randint(1, 29), randint(1, 99)
            self.plateau[position_caractere[0]][position_caractere[1]] = caractere


    def placer_monstres(self):
        """
        place les monstres sur le plateau
        et retourne une liste de tuple des coordonnées des monstres
        """
        monstres = "&&&&&&&&&"
        coords_monstres = []
        for monstre in monstres:
            position_monstre = randint(1, 29), randint(1, 99)
            while self.plateau[position_monstre[0]][position_monstre[1]] != ".":
                position_monstre = randint(1, 29), randint(1, 99)
            self.plateau[position_monstre[0]][position_monstre[1]] = monstre
            coords_monstres.append(position_monstre)
        return coords_monstres


    def mouvement_monstres(self, coords_monstres):
        """
        on met les monstres en mouvement aleatoire
        dans un carré 5*5
        et on retourne les nouveaux coordonnéées des monstres
        """
        for indice, coords_monstre in enumerate(coords_monstres):
            nouvelle_ligne = randint(coords_monstre[0] - 2, coords_monstre[0] + 2)
            nouvelle_colonne = randint(coords_monstre[1] - 2, coords_monstre[1] + 2)
            while nouvelle_ligne < 0 or nouvelle_ligne > 29 or \
            nouvelle_colonne < 0 or nouvelle_colonne > 99 or\
            self.plateau[nouvelle_ligne][nouvelle_colonne] not in  '@.':
                nouvelle_ligne = randint(coords_monstre[0] - 2, coords_monstre[0] + 2)
                nouvelle_colonne = randint(coords_monstre[1] - 2, coords_monstre[1] + 2)
            self.plateau[nouvelle_ligne][nouvelle_colonne] = "&"
            self.plateau[coords_monstre[0]][coords_monstre[1]] = "."
            coords_monstres[indice] = nouvelle_ligne, nouvelle_colonne
        return coords_monstres


    def dessin_plateau(self):
        """
        affiche notre jeu
        """
        for ligne in self.plateau:
            print(''.join(ligne))



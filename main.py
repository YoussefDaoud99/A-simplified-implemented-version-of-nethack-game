from random import randint
import sys
from pyhack import plateau_jeu, expliquer_jeu, Nethack

def main():
    """
    programme principal
    """
    jeu = Nethack(plateau_jeu())
    expliquer_jeu()
    print("Are you ready (y/n) ?! ")
    reponse = str(input())
    if reponse == "y":
        jeu.dessin_tous_les_couloirs()   #cette ligne sert à dessiner les salles et les couloirs
        coords_caractere = jeu.placer_caractere() #elle place le caractère @
        jeu.autres_caracteres() #elle place les autres caracères du jeu
        coords_monstres = jeu.placer_monstres()
        jeu.dessin_plateau()  #afficher le plateau du jeu
        mouvement = str(input("choisir direction: "))
        score, live = 0, 1
        print('score = ', 0, end=" ")
        print('live =', live)
        while score < 10 and live > 0 and coords_caractere not in coords_monstres:
            nouv_coords = {"z": (coords_caractere[0] - 1, coords_caractere[1]),\
             "d": (coords_caractere[0], coords_caractere[1] + 1),\
             "q": (coords_caractere[0], coords_caractere[1] - 1),\
             "x": (coords_caractere[0] + 1, coords_caractere[1])}
            if mouvement == "s":
                sys.exit(1)
            elif mouvement in nouv_coords and jeu.verifie_mouvement(nouv_coords[mouvement]):
                jeu.plateau[coords_caractere[0]][coords_caractere[1]] = "."
                if jeu.plateau[nouv_coords[mouvement][0]][nouv_coords[mouvement][1]] == "$":
                    score += 1
                elif jeu.plateau[nouv_coords[mouvement][0]][nouv_coords[mouvement][1]] == ">":
                    live += 1
                elif jeu.plateau[nouv_coords[mouvement][0]][nouv_coords[mouvement][1]] == "<":
                    live -= 1
                jeu.plateau[nouv_coords[mouvement][0]][nouv_coords[mouvement][1]] = "@"
                coords_caractere = nouv_coords[mouvement]
                coords_monstres = jeu.mouvement_monstres(coords_monstres)
            jeu.dessin_plateau()
            mouvement = str(input("choisir direction: "))
            print("score = ", score, end="  ")
            print('live =', live)
            if score == 10:
                print("well done")



main()

from rumorFunctions import *
import argparse
from random import randint, choice

def main():
    #Grâce à ArgParse, je vais regarder chaque entré de l'utilisateur, et lui
    #Envoyer une erreur si son(ses) paramètre(s) est(sont) incorrecte(s)

    #On importe les variables initiées dans rumorFunctions
    #alea_indice, alea_init, nbr_simu = variable_arg()

    parser = argparse.ArgumentParser()
    parser.add_argument("nom_fichier",
                        help="chemin vers le fichier contenant le reseau")
    parser.add_argument("-s",
                        default="NULL",
                        help="Nom de la personne initiant la rumeur")
    parser.add_argument("-r",
                        type=int,
                        default=randint(0, 255),
                        help="valeur de la rumeur initiale")
    parser.add_argument("-p",
                        type=float,
                        default=0.1,
                        help="Probabilité qu'une rumeur soit modifiée " \
                             "lorsqu'elle est racontée (réel entre 0 et 1)")
    parser.add_argument("-t",
                        type=int,
                        default=-1,
                        help="Nombre d'étapes dans la simulation")
    parser.add_argument("-d",
                        help = "Si cette option est choisie, chaque personne " \
                               "connaissant la rumeur la transmet à un ami " \
                               "choisi aléatoirement parmi ceux ne " \
                               "connaissant pas déjà la rumeur", \
                        action="store_true")
    parser.add_argument("-m",
                        type=str,
                        default="none",
                        help = "Type de modification éventuelle de la rumeur " \
                               "lorsqu'elle est racontée (choix : " \
                               "incremental, bitflip, none)")
    args = parser.parse_args()

    nom_pers, reseau = loadNetwork(args.nom_fichier)
    pers_info = [False for pers in range(len(nom_pers))]
    #si args.s a sa valeur par défaut
    if args.s == "NULL":
        #on choisit une personne de la liste au hasard
        args.s = choice(nom_pers)

    #On vérifie si tout est correcte
    args.s, args.r, args.p = verification_arg(args, nom_pers, pers_info)
    
    print("Etat initial : \n")
    printState(nom_pers, pers_info)
    
    #On répète le nombre de fois qu'on nous demande en précisant l'étape
    #A laquelle on se trouve et le nombre de personnes qui ont
    #Apprises la rumeur
    for simulation in range(1, args.t):
        print("Etape " + str(simulation) + \
              " (" + str(update(reseau, pers_info)) + \
              " personnes l'ont apprise) : ")
        printState(nom_pers, pers_info)

#J'importe rumorFunctions dans rumor
if __name__ == "__main__":
    main()

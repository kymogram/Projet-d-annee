from rumorFunctions import *
import argparse
from random import randint, choise

def main():
    #On prends les valeurs de update, pour afficher combien de personnes
    #ont apprisent la rumeur
    val_rumeur, rumeur_apprise = update(pers_info, reseau, args)

    #Grâce à ArgParse, je vais regarder chaque entré de l'utilisateur, et lui
    #Envoyer une erreur si son(ses) paramètre(s) est(sont) incorrecte(s)

    #On importe les variables
    alea_indice, alea_init, nbr_simu = variable_arg()

    parser = argparse.ArgumentParser()
    parser.add_argument("nom_fichier",
                        help="chemin vers le fichier contenant le réseau")
    parser.add_argument("-s",
                        default="NULL",
                        help="Nom de la personne initiant la rumeur")
    parser.add_argument("-r",
                        type=int,
                        default=randint(0,255),
                        help="valeur de la rumeur initiale")
    parser.add_argument("-p",
                        type=float, default=0.1, help= \
                        "Probabilité qu'une rumeur soit modifiée " \
                        "lorsqu'elle est racontée (réel entre 0 et 1)")
    parser.add_argument("-t",
                        type=int,
                        default=-1,
                        help="Nombre d'étape dans la simulation")
    parser.add_argument("-d",
                        default=False,
                        help="Si cette option est choisie, chaque personne " \
                        "connaissant la rumeur la transmet à un ami " \
                        "choisi aléatoirement parmi ceux ne " \
                        "connaissant pas déjà la rumeur", \
                        action = "store_true")
    parser.add_argument("-m",
                        type=str,
                        default="none", \
                        help="Type de modification éventuelle de la " \
                        "rumeur lorsqu'elle est racontée (choix : " \
                        "incremental, bitflip, none)")
    parser.add_argument("-u",
                        type=str,
                        default="stable",
                        help="Règle " \
                        "de mise à jour lorsqu'une personne apprend une " \
                        "nouvelle version de la rumeur (choix : " \
                        "stable, rewrite, mixture)")
    args = parser.parse_args()
    
    nom_pers, reseau = loadNetwork(args.nom_fichier)
    #si args.s a sa valeur par défaut
    if args.s == "NULL":
        #on choisit une personne de la liste au hasard
        args.s = choise(nom_pers)
    #si args.t a sa valeur par défaut
    if args.t == -1:
        #le nombre de simulation continuera jusqu'à ce que tout le monde soit
        #au courant
        args.t = nbr_simu

    #On vérifie si tout est correcte
    try:
        verification_arg(args, nom_pers)
    except Exception as e:
        print(e)
        return
    #On excécute loadNetwork en l'associant à des valeurs
    nom_pers, reseau = loadNetwork()

    #Initialisation des personnes informées(à la base, personne ne la connaît)
    pers_info = [False for pers in range(len(nom_pers))]
    
    print("Etat initial : \n")
    printState(nom_pers, pers_info, args)
    
    #On répète le nombre de fois qu'on nous demande en précisant l'étape
    #A laquelle on se trouve et le nombre de personnes qui ont
    #Apprises la rumeur
    for simulation in range(1, nbr_simu):
        print("\nEtape " + str(simulation) + \
              " (" + str(rumeur_apprise) + \
              " personnes l'ont apprise) : ")
        printState(nom_pers, pers_info, args)

if __name__ == "__main__":
    main()
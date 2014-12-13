import rumorFunctions
import argparse
from random import randint

def main():
    #On excécute inputData en l'associant à des valeurs
    nom_pers, reseau = rumorFunctions.inputData()

    #Initialisation des personnes informées(à la base, personne ne la connaît)
    pers_info = [False for pers in range(len(nom_pers))]

    #Grâce à ArgParse, je vais regarder chaque entré de l'utilisateur, et lui
    #Envoyer une erreur si son(ses) paramètre(s) est(sont) incorrecte(s)

    #On importe les variables initiées dans rumorFunctions
    alea_indice, alea_init, nbr_simu = variable_arg()

    parser = argparse.ArgumentParser()
    parser.add_argument("-s",
                        default=nom_pers[alea_indice],
                        help="Nom de la personne initiant la rumeur")
    parser.add_argument("-r",
                        type=int,
                        default=alea_init,
                        help="valeur de la rumeur initiale")
    parser.add_argument("-p",
                        type=float,
                        default=0.1,
                        help="Probabilité qu'une rumeur soit modifiée " \
                             "lorsqu'elle est racontée (réel entre 0 et 1)")
    parser.add_argument("-t",
                        type=int,
                        default=nbr_simu,
                        help = "Nombre d'étapes dans la simulation")
    parser.add_argument("-d",
                        default=False,
                        help = "Si cette option est choisie, chaque personne " \
                               "connaissant la rumeur la transmet à un ami " \
                               "choisi aléatoirement parmi ceux ne " \
                               "connaissant pas déjà la rumeur", \
                        action="store_true")
    parser.add_argument("-m",
                        type=str,
                        default = "none",
                        help = "Type de modification éventuelle de la rumeur " \
                               "lorsqu'elle est racontée (choix : " \
                               "incremental, bitflip, none)")
    args = parser.parse_args()
    #On vérifie si tout est correcte
    args.s, args.r, args.p = verification_arg(args)



    #On excécute inputData en l'associant à des valeurs
    nom_pers, reseau = rumorFunctions.inputData()
    
    print("Etat initial : \n")
    rumorFunctions.printState(nom_pers, pers_info)
    
    #On répète le nombre de fois qu'on nous demande en précisant l'étape
    #A laquelle on se trouve et le nombre de personnes qui ont
    #Apprises la rumeur
    for simulation in range(1, nbr_simu):
        print("Etape " + str(simulation) + \
              " (" + str(rumorFunctions.update(reseau, pers_info)) + \
              " personnes l'ont apprise) : ")
        rumorFunctions.printState(nom_pers, pers_info)

#J'importe rumorFunctions dans rumor
if __name__ == "__main__":
    main()

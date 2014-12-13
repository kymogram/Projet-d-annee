from random import randint
    
def loadNetwork(nom_fichier):
    nom_pers = []
    fichier = open(nom_fichier)
    ligne = [line.strip() for line in fichier.readlines()]
    fichier.close()
    nbr_pers_res = len(ligne)
    reseau = [[0 for j in range(nbr_pers_res)]for i in range(nbr_pers_res)]
    #J'initialise le nom des personnes dans la liste nom_pers
    for i in range(nbr_pers_res):
        reseau[i][i] = True
        pers = ligne[i].split(':')
        nom = str(pers[0]).strip()
        nom_pers.append(nom)
    
    for i in range(nbr_pers_res):
        pers = ligne[i].split(':')
        ami = pers[1].split(',')
        #Je prends la liste de la personne a en ami et je l'isole et la nettoie
        #Dans le for
        for j in range(len(ami)):
            ami[j] = "".join(ami[j]).strip()
        for j in range(len(ami)):
            if ami[j] in nom_pers:
                for k in range(nbr_pers_res):
                    if i != k:
                        if nom_pers[k] in ami:
                            reseau[i][k] = True
                        else:
                            reseau[i][k] = False
    return nom_pers, reseau
    
def incremental(args):
    dec_rumor = args.r
    incr_decr = randint(0,1)
    if dec_rumor == 255:
        dec_rumor -= 1
    elif dec_rumor == 0:
        dec_rumor += 1
    else:
        if incr_decr == 0:
            dec_rumor -= 1
        if incr_decr == 1:
            dec_rumor += 1
    return dec_rumor

def convert_dec(dec_rumor):
    str_bin = ""
    bin_rumor = list(bin(dec_rumor)[2:])
    while len(bin_rumor) < 8:
        add_zero = ['0']
        bin_rumor = add_zero + bin_rumor[:]
    return bin_rumor
    
def convert_bin(bin_rumor):
    dec_rumor = int(bin_rumor, 2)
    return dec_rumor

#J'utilise la fonction str_bin pour ne pas avoir une liste contenant chaque bit
#mais pour avoir une string de ces bits réunis
def str_bin(bin_rumor):
    str_bin = ""
    for elem in bin_rumor:
        str_bin += str(elem)
    return str_bin

def to_str_bin(n):
    return "{0:08b}".format(n)

def bit_flip(args):
    dec_rumor = args.r
    bin_rumor = convert_dec(dec_rumor)
    alea_bit_flip = randint(0,7)

    if bin_rumor[alea_bit_flip] == '0':
        bin_rumor[alea_bit_flip] = 1
    else:
        bin_rumor[alea_bit_flip] = 0
    bin_rumor = str_bin(bin_rumor)

    args.r = convert_bin(bin_rumor)
    return bin_rumor

def variable_arg():
    #Variable pour '-s'
    alea_indice = randint(0,len(nom_pers)-1)
    #Variable pour '-r'
    alea_init = randint(0,255)
    #Variable pour '-t'
    nbr_simu = 0
    while count != len(pers_info):
        count = 0
        for elem in pers_info:
            if elem:
                count += 1
        nbr_simu += 1
    return alea_indice, alea_init, nbr_simu
    
def verification_arg(args, pers_info):
    if args.s in nom_pers:
        pers_info[nom_pers.index(args.s)] = True
    else:
        raise ValueError("Cette personne n'existe pas dans votre réseau")

    if args.r < 0:
        print("\nSoyez raisonnable...\n")
        raise ValueError("Aucun nombre négatif n'est toléré")
    elif args.r > 255:
        print("\nVeuillez mettre une valeur ne dépassant pas 255\n")
        raise ValueError("Votre valeur est trop grande")

    if args.t != "nbr_simu":
        nbr_simu = args.t

    if args.p < 0:
        print("\nSoyez raisonnable...\n")
        raise ValueError("Aucun nombre négatif n'est toleré")
    elif args.p > 1:
        print("\nVeuillez mettre une valeur ne dépassant pas 1\n")
        raise ValueError("Votre valeur est trop grande")

    if args.m not in ["incremental", "bitflip", "none"] or \
                        args.u not in ["stable", "rewrite", "mixture"]:
        print("\nSi vous ne savez pas quoi faire, demandez l'aide avec '-h'\n")
        raise ValueError("le paramètre choisi est incorrect")

    return args.s, args.r, args.t, args.p, args.m, args.u

def fichier_printer(nom_fichier):
    fichier = open(nom_fichier)
    document = " ".join(fichier.readlines())
    fichier.close()
    return document
    
def printState(nom_pers, pers_info, reseau, args):
    val_rumeur, rumeur_apprise = update()
    #J'initialise à 20 le nombre d'espace qu'il faut mettre après le nom
    espace_ecart = 20
    print("le réseau est le suivant :\n" + fichier_printer(nom_fichier) + \
    "\nPersonne initiant la rumeur: " + str(args.s))
    dec_rumor = randint(0,255)
    print("Valeur de la rumeur initiale: " + str(dec_rumor) + \
          "\nNom                      BIN\tDEC")
    for pers in range(len(nom_pers)):
        print(str(nom_pers[pers]) + \
              ' '*(espace_ecart-len(nom_pers[pers])), end='')
        #Verifie si la personne connait la rumeur
        if pers_info[pers]:
            print(to_str_bin(val_rumeur) + "\t" + str(val_rumeur))
        else:
            print("ne connait pas la rumeur")

def si_connait_pas(pers_info, args, val_rumeur, alea, rumeur_apprise):
    if args.m == "none":
        val_rumeur[alea] = args.r
    elif args.m == "incremental":
        val_rumeur[alea] = incremental(args)
    elif args.m == "bitflip":
        val_rumeur[alea] = convert_bin(bit_flip(args))
    pers_info[alea] = True
    rumeur_apprise += 1
    return val_rumeur, pers_info, rumeur_apprise

def update(pers_info, reseau, args):
    rumeur_apprise = 0
    val_rumeur = [[] for i in range(len(pers_info))]
    for pers in range(len(pers_info)):
        if pers_info[pers]:
            alea = randint(0,len(pers_info)-1)
            #Tant que c'est lui-même ou quelqu'un avec qui il n'est pas ami
            #La valeur aléatoire change pour qu'il puisse la transmettre à
            #Quelqu'un d'adéquat
            while pers == alea or not reseau[alea][pers]:
                alea = randint(0, len(pers_info)-1)
            proba_rumeur = 10*args.p
            val_alea_rumeur = randint(1,10//proba_rumeur)
            #1 étant un chiffre aléatoire qui a une chance d'arrivé par rapport
            #à args.p et par rapport aux caculs ci-dessus
            if val_alea_rumeur == 1:
                #Si l'option "Don't tell" est choisi, seules les personnes ne
                #connaissant pas la rumeur, peuventl'apprend.
                #Les autres gardent celle qu'ils avaient
                if args.d:
                    if not pers_info[alea]:
                        val_rumeur, pers_info, rumeur_apprise = \
                            si_connait_pas(pers_info, args, val_rumeur, alea)
                else:
                    if pers_info[alea]:
                        if args.u == "rewrite":
                            val_rumeur[alea] = val_rumeur[pers]
                        elif args.u == "mixture":
                            dec_rumor = args.r
                            bin_rumor = convert_dec(dec_rumor)
                            for elem in bin_rumor:
                                #pour la probabilité de 1/9 : si on fait un
                                #randint de 0 à 9, chaque chiffre a une
                                #possibilité de 1/10 d'apparaitre
                                proba = randint(0,9)
                                if val_rumeur[pers][elem] != \
                                                val_rumeur[alea][elem]:
                                    if proba == 0
                                        val_rumeur[alea][elem] = \
                                                val_rumeur[pers][elem]
                    else:
                        val_rumeur, pers_info, rumeur_apprise = \
                            si_connait_pas(pers_info, args, val_rumeur, alea)
            else:
                val_rumeur[pers] = args.r
        else:
            val_rumeur[pers] = "Ne connait pas la rumeur"
    return val_rumeur, rumeur_apprise
from random import randint, choice, random

def pourcentage(proportion):
    alea = random()
    return alea < proportion

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
                        reseau[i][k] = nom_pers[k] in ami
    return nom_pers, reseau

def incremental(v):
    return (v + choice([1, -1]))%256

def convert_bin(bin_rumor):
    return int(bin_rumor, 2)

def bit_flip(v):
    bin_rumor = list(to_bin_str(v))
    alea_bit_flip = randint(0,7)
    if bin_rumor[alea_bit_flip] == '0':
        bin_rumor[alea_bit_flip] = '1'
    else:
        bin_rumor[alea_bit_flip] = '0'
    return convert_bin("".join(bin_rumor))
    
def verification_arg(args, nom_pers, pers_info):
    if args.s in nom_pers:
        pers_info[nom_pers.index(args.s)] = args.r
    else:
        raise ValueError(args.s + " n'existe pas dans votre réseau")
            
    if args.r < 0:
        print("\nSoyez raisonnable...\n")
        raise ValueError("Aucun nombre négatif n'est toléré")
    elif args.r > 255:
        print("\nVeuillez mettre une valeur ne dépassant pas 255\n")
        raise ValueError("Votre valeur est trop grande")
    
    if args.p < 0:
        print("\nSoyez raisonnable...\n")
        raise ValueError("Aucun nombre négatif n'est toleré")
    elif args.p > 1:
        print("\nVeuillez mettre une valeur ne dépassant pas 1\n")
        raise ValueError("Votre valeur est trop grande")
        
    if args.m not in ["incremental", "bitflip", "none"]:
        print("\nSi vous ne savez pas quoi faire, demandez l'aide avec '-h'\n")
        raise ValueError("le paramètre choisi est incorrect")

def to_bin_str(n):
    return "{0:08b}".format(n)

def printState(nom_pers, pers_info):
    #J'initialise à 20 le nombre d'espace qu'il faut mettre après le nom
    espace_ecart = 20
    print("Nom                      BIN    DEC")
    for pers in range(len(nom_pers)):
        print(str(nom_pers[pers]) + ' ' * (espace_ecart-len(nom_pers[pers])),
              end='')
        #Verifie si la personne connait la rumeur
        if pers_info[pers]:
            print(to_bin_str(pers_info[pers]) + "    " + str(pers_info[pers]))
        else:
            print("ne connaît pas la rumeur")

def update(reseau, pers_info, args):
    #Variable qui va compter combien de gens vont apprendre la rumeur à chaque
    #Appel à la fonction
    pers_connait = 0
    for pers in range(len(pers_info)):
        #Si la personne connait la rumeur, il peut la transmettre
        if pers_info[pers]:
            if not args.d:
                #crée une liste avec les amis de pers
                amis = [i for i in range(len(pers_info)) if reseau[pers][i] \
                                                         and i != pers]
            #Si l'option don't tell again a été choisi, seules les personnes ne
            #Connaissant pas la rumeur peuvent recevoir la rumeur
            else:
                #crée une liste avec les amis de pers qui ne connaissent
                #pas la rumeur
                amis = [i for i in range(len(pers_info)) \
                          if reseau[pers][i] and not pers_info[i] and i != pers]
            if len(amis) != 0:
                apprenti = choice(amis)
                if not pers_info[apprenti]:
                    pers_connait += 1
                rumeur_apprise = pers_info[pers]
                if pourcentage(args.p)
                    if args.m == "bitflip":
                        rumeur_apprise = bit_flip(rumeur_apprise)
                    elif args.m == "incremental":
                        rumeur_apprise = incremental(rumeur_apprise)
                pers_info[apprenti] = rumeur_apprise
    return pers_connait


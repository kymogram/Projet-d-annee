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
                        reseau[i][k] = nom_pers[k] in ami
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
    
def convert_bin(bin_rumor):
    dec_rumor = int(bin_rumor, 2)
    return dec_rumor
  
def str_bin(bin_rumor):
    str_bin = ""
    for elem in bin_rumor:
        str_bin += str(elem)
    return str_bin
  
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
    
def rumeur_pers(nom_pers, dec_rumor):
    val_rumeur = [[] for i in range(len(nom_pers))]
    
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
    
def verification_arg(args, nom_pers, pers_info):
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
    
    if args.p < 0:
        print("\nSoyez raisonnable...\n")
        raise ValueError("Aucun nombre négatif n'est toleré")
    elif args.p > 1:
        print("\nVeuillez mettre une valeur ne dépassant pas 1\n")
        raise ValueError("Votre valeur est trop grande")
        
    if args.m not in ["incremental", "bitflip", "none"]:
        print("\nSi vous ne savez pas quoi faire, demandez l'aide avec '-h'\n")
        raise ValueError("le paramètre choisi est incorrect")
    return args.r, args.p, args.m

def to_bin_str(n):
    return "{0:08b}".format(n)

def fichier_printer(nom_fichier):
    fichier = open(nom_fichier)
    document = "".join(fichier.readlines())
    fichier.close()
    return document

def printState(nom_pers, pers_info):
    #J'initialise à 20 le nombre d'espace qu'il faut mettre après le nom
    espace_ecart = 20
    print("Nom                      BIN    DEC")
    for pers in range(len(nom_pers)):
        print(str(nom_pers[pers]) + ' ' * (espace_ecart-len(nom_pers[pers])),
              end='')
        #Verifie si la personne connait la rumeur
        if pers_info[pers]:
            print(to_bin_str(pers_info[pers]))
        else:
            print("ne connaît pas la rumeur")

def update(reseau, pers_info, args):
    #Variable qui va compter combien de gens vont apprendre la rumeur à chaque
    #Appel à la fonction
    pers_connait = 0
    for pers in range(len(pers_info)):
        #Si la personne connait la rumeur, il peut la transmettre
        if pers_info[pers]:
            alea = randint(0,len(pers_info)-1)
            if not args.d:
                while pers == alea or not reseau[alea][pers]:
                    alea = randint(0, len(pers_info)-1)
                if not pers_info[alea]:
                    pers_connait += 1
                pers_info[alea] = True
                
            #Si l'option don't tell again a été choisi, seul les personne ne
            #Connaissant pas la rumeur peuvent recevoir la rumeur
            else:
                while pers == alea or not reseau[alea][pers] \
                                        or not pers_info[alea]:
                    alea = randint(0, len(pers_info)-1)
                pers_connait += 1
                pers_info[alea] = True
    return pers_connait


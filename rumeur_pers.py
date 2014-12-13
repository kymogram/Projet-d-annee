import rumorFunctions

def si_connait_pas(pers_info, args, val_rumeur, alea):
    if args.m == "none":
        val_rumeur[alea] = args.r
    elif args.m == "incremental":
        val_rumeur[alea] = incremental(args)
    elif args.m == "bitflip":
        val_rumeur[alea] = convert_bin(bit_flip(args))
    pers_info[alea] = True
    return val_rumeur, pers_info

def rumeur_pers(nom_pers, reseau):
    val_rumeur = [[] for i in range(len(nom_pers))]
    for pers in range(len(nom_pers)):
        if pers_info[pers]:
            alea = randint(0,len(nom_pers)-1)
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
                        val_rumeur, pers_info = \
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
                        val_rumeur, pers_info = \
                            si_connait_pas(pers_info, args, val_rumeur, alea)
            else:
                val_rumeur[pers] = args.r
        else:
            val_rumeur[pers] = "Ne connait pas la rumeur"
    return val_rumeur

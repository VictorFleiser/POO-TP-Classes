import random as r
import warnings as w

# FONCTION POUR COLORER LES CHAINES DE CARACTERES

COLOR = {
    'blue': '\033[94m',
    'default': '\033[99m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}

def color_string(string, couleur, couleurs_autorise_bool):
	'''
	Retourne la chaine de caractères colorée avec la couleur sélectionnées (cf : dictionnaire 'COLOR') si couleurs_autorise_bool est vrai
	'''
	return (COLOR.get(couleur, COLOR['default']) + string + '\033[0m' if couleurs_autorise_bool else string)

def pv_color(pv, pv_max):
	'''
	Retourne la chaine de caractères de la couleur correspondant à ce niveau de PV :
	PV = 100% => "cyan"
	PV < 100% => "green"
	PV < 66% => "yellow"
	PV < 33% => "red"
	PV = 0% => "red"
	'''
	match pv:
		case pv if pv <= 0 :								#mort
			return "red"
		case pv if pv <= int(pv_max/3): 					#moins de 33% PV
			return "red"
		case pv if pv <= int(2*pv_max/3): 					#moins de 66% PV
			return "yellow"
		case pv if pv < pv_max:								#moins de 100% PV
			return "green"
		case pv_max : 										#max PV
			return "cyan"


#FONCTIONS DE NOMS ALEATOIRES

def get_random_name():
	'''
	Retourne un nom aléatoire parmis les 18239 noms disponibles dans list_of_names.txt (dans le même dossier)
	'''
	with open("list_of_names.txt", "r") as file:
		names = file.readlines()
		return r.choice(names).strip()

def get_random_name_description():
	'''
	Retourne une description de nom aléatoire parmis les 56 descriptions disponibles dans list_of_name_description.txt (dans le même dossier)
	'''
	with open("list_of_name_description.txt", "r") as file:
		name_description = file.readlines()
		return r.choice(name_description).strip()

def random_name():
	'''
	Retourne un nom ainsi que sa description.
	'''
	return (get_random_name() + ' ' + get_random_name_description())



# FONCTIONS D'OPERATIONS MATHEMATIQUES POUR MODIFIER LINEAIREMENT UNE VALEUR EN FONCTION DE LA DISTANCE

def reduction_lineaire(distance, distance_down, distance_up, valeur_down, valeur_up, sens="down"):


	'''
	Réduit une valeur (dégats, soin...) de manière linéaire sur la plage [valeur_down;valeur_up] 
	en fonction de la distance sur une plage [distance_down;distance_up]; 
	Si le sens est "down" la valeur diminue quand la distance augmente,
	Sinnon c'est l'inverse : la valeur augmente quand la distance augmente

	Exemple pratique : 
	Dégats = 15, Distance = randint(0, 100)
	en fonction de la distance les dégats infligés sont :

	distance entre 0 et 50 : dégats entiers : 15 dégats
	distance entre 51 et 75 : dégats diminués linéairement de 15 à 0 : dégats entre 15 et 0		<- reduction_lineaire() s'occupe de cette partie
	distance entre 75 et 100 : Attaque ratée : 0 dégats

	reduction_lineaire(distance, 50, 75, 15, 0, "down")
	'''
	d = distance - distance_down	
	delta_distance = distance_up - distance_down

	if(d<0 or d>delta_distance):		#Ne devrait jamais se produire : je lance un warning au cas où j'ai mis une mauvaise valeur dans les arguments
		w.warn("Distance passée à reduction_lineaire() n'est pas dans l'intervalle de distance, retourne valeur_down par défaut\n", stacklevel=2)
		return valeur_down

	x = d/delta_distance
	delta_valeur = valeur_up - valeur_down
	if (sens == "down"):
		return(valeur_down + (1-x)*delta_valeur)
	else :
		return(valeur_down+x*delta_valeur)

'''

#tests:
for i in range(25, 75):
#	print(str(i)+" : "+str(reduction_lineaire(i, 25, 75, 5, 30)))
	print(str(reduction_lineaire(i, 25, 75, 5, 30)))

'''
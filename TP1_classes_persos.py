import random as r
import warnings as w

from TP1_global_variables import *

from TP1_functions import *

decors_string = "|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|\n"

#CLASSE DE BASE

class Personnage:
	def __init__(self, nom, pv_modifier):
		self.__nom = nom
		self.__max_pv = r.randint(20,30) + pv_modifier
		self.__pv = self.__max_pv
		self.__effets = {'regeneration' : 0, 'poison' : 0, 'paralyse' : 0}		#liste des effets actifs : nombre de tours

	def distance(self):
		return r.randint(0,100)
	
	@property
	def pv(self):
		return self.__pv

	@property
	def effets(self):
		return self.__effets

	@pv.setter
	def pv(self, valeur):
		self.__pv = valeur

		if self.__pv >= self.__max_pv :
			self.__pv = self.__max_pv
		if self.__pv <= 0 :
											#TO DO : mort du personnage
			pass

	@property
	def nom(self):
		return self.__nom

	@property
	def effets(self):
		return self.__effets
	
	@effets.setter
	def effets(self, valeur):
		try:
			effet, tours = valeur
		except ValueError :
			w.warn("Warning : Valeur passée dans le setter d'effet ne possède pas 2 valeurs\n", stacklevel=2) 
		self.__effets[effet] += tours
		if (self.__effets[effet] == 0):
			print("Effet " + str(effet) + " de " + self.__nom + " s'est dissipé.\n")

	def all_info(self):
		return ("Nom : " + self.__nom + "\n" + color_string("Points de vie : ", "green", couleurs_autorise_bool) + color_string(str(self.__pv), pv_color(self.__pv, self.__max_pv), couleurs_autorise_bool) + " / " + color_string(str(self.__max_pv), "cyan", couleurs_autorise_bool) + "\n")

#CLASSES INTERFACES

class IAttaquant():
	def attaquer(self):
		raise NotImplementedError()

class IDefenseur():
	def soigner(self):
		raise NotImplementedError()

#CLASSES INTERMEDIAIRES

class Guerrier(Personnage, IAttaquant):
	def __init__(self, nom, pts_attaque_modifier, pv_modifier):

		Personnage.__init__(self, nom, pv_modifier)
		
		self.__pts_attaque = 10 + pts_attaque_modifier
	
	@property
	def pts_attaque(self):
		return self.__pts_attaque

	def all_info(self):
		return (Personnage.all_info(self) + color_string("Points d'attaques de base : " + str(self.__pts_attaque), "red", couleurs_autorise_bool) + "\n")

class Soigneur(Personnage, IDefenseur):
	def __init__(self, nom, pts_soin_modifier, pv_modifier):

		Personnage.__init__(self, nom, pv_modifier)
		
		self.__pts_soin = 10 + pts_soin_modifier
	
	@property
	def pts_soin(self):
		return self.__pts_soin

	def all_info(self):
		return (Personnage.all_info(self) + color_string("Points de soins de base : " + str(self.__pts_soin), "yellow", couleurs_autorise_bool) + "\n")

class Paladin(Personnage, IAttaquant, IDefenseur):
	def __init__(self, nom, pts_attaque_modifier, pts_soin_modifier, pv_modifier):

		Personnage.__init__(self, nom, pv_modifier)
		
		self.__pts_attaque = 5 + pts_attaque_modifier

		self.__pts_soin = 5 + pts_soin_modifier
	
	@property
	def pts_soin(self):
		return self.__pts_soin

	@property
	def pts_attaque(self):
		return self.__pts_attaque

	def all_info(self):
		return (Personnage.all_info(self) + color_string("Points d'attaques de base : " + str(self.__pts_attaque), "red", couleurs_autorise_bool) + "\n" + color_string("Points de soins de base : " + str(self.__pts_soin), "yellow", couleurs_autorise_bool) + "\n")


# CLASSES SPECIFIQUES

#CLASSES GUERRIERS

class Barbare(Guerrier):
	def __init__(self, nom):
		
		pts_attaque_modifier = 5
		pv_modifier = 8

		Guerrier.__init__(self, nom, pts_attaque_modifier, pv_modifier)
		
		self.__compteur_tours_rage = 0				#compteur de tours : inflige x2 dégats tous les 2 tours
		self.__rage_multiplieur = 1
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nLe Barbare : double ses dégats toutes les 2 attaques\nIl s'inflige des dégats soi même lorsequ'il attaque\nPortée : Courte\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def attaquer(self, cible: Personnage|list[Personnage]):
		degats = self.pts_attaque * self.__rage_multiplieur
		self_damage = 3

		self.__compteur_tours_rage += 1
		if not (self.__compteur_tours_rage % 2):	#Augmente le multiplicateur de dégats (rage) tous les 2 attaques
			self.__rage_multiplieur *= 2

		distance = Personnage.distance(self)

		print("\n------\n\nAttaque :\n")
		print("Distance : " + str(distance) + "\n")

		if (distance > 75) :	#distance bcp trop grande : attaque rate
			degats = 0
			print("La distance est beaucoup trop élevée : L'attaque ratte : 0 dégats infligés\n")
		elif (distance > 50) :	#distance trop grande : diminution de dégats linéaire jusqu'à 75 unitées de longeur
			degats = int(reduction_lineaire(distance, 50, 75, 1,  degats))
			print("La distance est trop élevée : Dégats diminués : " + str(degats) + " dégats infligés\n")
		else :
			print("L'attaque est un succès, " + str(degats) + " dégats infligés\n")

		self.pv -= self_damage
		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement, puis soigne
			cible[0].pv -= degats
		else :
			cible.pv -= degats
		
		print("------\n")

	def all_info(self):
		return (decors_string + Guerrier.all_info(self) + color_string("Niveau de rage : dégats = x" + str(int(self.__rage_multiplieur)), "magenta", couleurs_autorise_bool) + "\n" + self.__description_personnage + decors_string)

class Archer(Guerrier):
	def __init__(self, nom):
		
		pts_attaque_modifier = 0
		pv_modifier = -1

		Guerrier.__init__(self, nom, pts_attaque_modifier, pv_modifier)
		
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nL'Archer : Inflige plus de dégats sur les cibles loin\nInflige des coups critiques sur les cibles très loin\nPortée : Très longue\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def attaquer(self, cible: Personnage|list[Personnage]):
		degats = self.pts_attaque

		distance = Personnage.distance(self)

		print("\n------\n\nAttaque :\n")
		print("Distance : " + str(distance) + "\n")

		if (distance > 85) :	#distance très grande : coup critique
			degats *= 2
			print("La distance est très grande : L'attaque inflige un coup critique : " + str(degats) + " dégats infligés\n")
		elif (distance > 50) :	#distance grande : augmentation de dégats linéaire jusqu'à 85 unitées de longeur
			degats = int(reduction_lineaire(distance, 50, 85, degats, degats+5, "up"))
			print("La distance est grande : Dégats augmentés : " + str(degats) + " dégats infligés\n")
		else :
			print("L'attaque est un succès, " + str(degats) + " dégats infligés\n")

		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement, puis soigne
			cible[0].pv -= degats
		else :
			cible.pv -= degats
		
		print("------\n")

	def all_info(self):
		return (decors_string + Guerrier.all_info(self) + self.__description_personnage + decors_string)

class Assassin(Guerrier):
	def __init__(self, nom):
		
		pts_attaque_modifier = 10
		pv_modifier = -5

		Guerrier.__init__(self, nom, pts_attaque_modifier, pv_modifier)
		
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nL'Assassin : Inflige des coups critiques sur les cibles très proches\nPortée : Courte\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def attaquer(self, cible: Personnage|list[Personnage]):
		degats = self.pts_attaque

		distance = Personnage.distance(self)

		print("\n------\n\nAttaque :\n")
		print("Distance : " + str(distance) + "\n")

		if (distance > 75) :	#distance bcp trop grande : attaque rate
			degats = 0
			print("La distance est beaucoup trop élevée : L'attaque ratte : 0 dégats infligés\n")
		elif (distance > 50) :	#distance trop grande : diminution de dégats linéaire jusqu'à 75 unitées de longeur
			degats = int(reduction_lineaire(distance, 50, 75, 1, degats))
			print("La distance est trop élevée : Dégats diminués : " + str(degats) + " dégats infligés\n")
		elif (distance > 25) :	#distance reussie
			print("L'attaque est un succès, " + str(degats) + " dégats infligés\n")
		else :					#coup critique
			degats *= 5
			print("La distance est très courte : L'attaque inflige un coup critique : " + str(degats) + " dégats infligés\n")

		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement, puis soigne
			cible[0].pv -= degats
		else :
			cible.pv -= degats
		
		print("------\n")

	def all_info(self):
		return (decors_string + Guerrier.all_info(self) + self.__description_personnage + decors_string)

class Mage(Guerrier):
	def __init__(self, nom):
		
		pts_attaque_modifier = -4
		pv_modifier = -7

		Guerrier.__init__(self, nom, pts_attaque_modifier, pv_modifier)
		
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nLe Mage : Inflige des dégats à 5 cibles\nPortée : Moyenne\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def attaquer(self, cible: Personnage|list[Personnage]):

		print("\n------\n\nAttaque :\n")

		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement
			nombre_de_cibles = len(cible)
			if (nombre_de_cibles > 5):
				nombre_de_cibles = 5
		else :
			cible = [cible]				#transforme la cible (de type Personnage) en liste de Personnages
			nombre_de_cibles = 1

		while (nombre_de_cibles) :		#une attaque par cible

			degats = self.pts_attaque

			distance = Personnage.distance(self)

			print("Distance : " + str(distance) + "\n")

			if (distance > 75) :	#distance très grande : dégats dimminués
				degats = int(reduction_lineaire(distance, 75, 100, 1, degats))
				print("La distance est trop élevée : Dégats diminués : " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")
			elif (distance < 25) :	#distance très petite : dégats dimminués
				degats = int(reduction_lineaire(distance, 0, 25, 1, degats, "up"))
				print("La distance est trop courte : Dégats diminués : " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")
			else :					#attaque réussie
				print("L'attaque est un succès, " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")

			cible[nombre_de_cibles-1].pv -= degats

			nombre_de_cibles -= 1
		
		print("------\n")

	def all_info(self):
		return (decors_string + Guerrier.all_info(self) + self.__description_personnage + decors_string)

class SorcierDeChaos(Guerrier):				#TODO : a lot
	def __init__(self, nom):
		
		pts_attaque_modifier = r.randint(-3,3)
		pv_modifier = -6

		Guerrier.__init__(self, nom, pts_attaque_modifier, pv_modifier)
		
		self.__description_personnage = "\n\n\t-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n\tLe Sorcier de Chaos : possède des effets aléatoires :\n\n\t4/5 : choisit des cibles adverses\n\t1/5 : choisit des cibles alliées\n\n\t16/20 : 1 cible choisie\n\t3/20 : entre 3 et 5 cibles choisies\n\t1/20 : tous les personnages sont choisis\n\n\t3/5 : inflige des dégats aux cibles\n\t1/5 : soigne les cibles\n\t1/5 : donne un effet aléatoire (durée aléatoire)\n\n\tPortée : infinie\n\t-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def attaquer(self, cible: Personnage|list[Personnage]):

		print("\n------\n\nAttaque :\n")

		nombre_alea = r.randint(1,5)						#CHOIX DU JOUEUR AFFECTE
		if (nombre_alea == 5):
			player_target = 0		#TODO : à faire
		else :
			player_target = 1		#TODO : à faire

		nombre_alea = r.randint(1,20)						#CHOIX DU NOMBRE DE CIBLES
		if (nombre_alea <= 16):
			nombre_cibles = 1
		elif (nombre_alea <= 19):
			nombre_cibles = r.randint(3,5)
		else:
			nombre_cibles = 100		#TODO : à modifier avec la valeur correcte

		while (nombre_cibles):
			nombre_alea = r.randint(1,5)					#CHOIX DEGAT/SOIN
			if (nombre_alea == 5):
				pass					#TODO : à faire le soin de la cible

			elif (nombre_alea == 1):						#CHOIX SI EFFET OU NON
				duree_effet = nombre_alea = r.randint(1,10)	#CHOIX DUREE EFFET
				nombre_alea = r.randint(1,3)				#CHOIX QUEL EFFET
				match nombre_alea :
					case 1 :
						pass			#TODO : effet regen
					case 2 :
						pass			#TODO : effet poison
					case 3 :
						pass			#TODO : effet para
					case _ :
						pass

			else :											#Dégats
				pass					#TODO : à faire les dégats de la cible


			nombre_cibles -= 1


		print("------\n")

	def all_info(self):
		return (decors_string + Guerrier.all_info(self) + self.__description_personnage + "\n"+decors_string)



#CLASSES SOIGNEURS

class Pretre(Soigneur):
	def __init__(self, nom):
		
		pts_soin_modifier = 20
		pv_modifier = 1

		Soigneur.__init__(self, nom, pts_soin_modifier, pv_modifier)
		
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nLe Prètre : soigne énormement de PV sur un allié proches\nPortée : Courte\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def soigner(self, cible: Personnage|list[Personnage]):
		soin = self.pts_soin

		distance = Personnage.distance(self)
		
		print("\n------\n\nSoin :\n")
		print("Distance : " + str(distance) + "\n")

		if (distance > 75) :	#distance bcp trop grande : le soin rate
			soin = 5
			print("La distance est beaucoup trop élevée : Le soin ratte : 5 PV soignés\n")
		elif (distance > 25) :	#distance trop grande : diminution de dégats linéaire jusqu'à 75 unitées de longeur
			soin = int(reduction_lineaire(distance, 25, 75, 5, soin))
			print("La distance est trop élevée : Soins diminués : " + str(soin) + " PV soignés\n")
		else :					#soin reussi
			print("La distance est courte : Le soin est un succès : " + str(soin) + " PV soignés\n")


		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement, puis soigne
			cible[0].pv += soin
		else :
			cible.pv += soin

		print("------\n")

	def all_info(self):
		return (decors_string + Soigneur.all_info(self) + self.__description_personnage + decors_string)

class Druide(Soigneur):
	def __init__(self, nom):
		
		pts_soin_modifier = 0
		pv_modifier = 3

		Soigneur.__init__(self, nom, pts_soin_modifier, pv_modifier)
		
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nLe Druide : soigne les PV d'un allié au cours du temps\nPortée : longue\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def soigner(self, cible: Personnage|list[Personnage]):
		soin = self.pts_soin
		tour_effet = 1
		distance = Personnage.distance(self)
		
		print("\n------\n\nSoin :\n")
		print("Distance : " + str(distance) + "\n")

		if (distance > 85) :	#distance bcp trop grande : le soin rate
			soin -= 5
			tour_effet = 1
			print("La distance est trop élevée : Le soin est réduit à 5 PV soignés, l'effet de régénération est affecté pendant 1 tour\n")
		elif (distance > 65) :	#distance trop grande : le soin est diminué
			soin -= 3
			tour_effet = 2
			print("La distance est élevée : Le soin est réduit à 7 PV soignés, l'effet de régénération est affecté pendant 2 tour\n")
		elif (distance > 45) :	#distance grande : le soin est diminué
			soin -= 2
			tour_effet = 3
			print("La distance est moyenne : Le soin est réduit à 8 PV soignés, l'effet de régénération est affecté pendant 3 tour\n")
		elif (distance > 25) :	#distance moyenne : le soin est diminué
			soin -= 1
			tour_effet = 4
			print("La distance est courte : Le soin est réduit à 9 PV soignés, l'effet de régénération est affecté pendant 4 tour\n")
		else :					#soin reussi
			tour_effet = 5
			print("La distance est très courte : Le soin est réussi : 10 PV soignés, l'effet de régénération est affecté pendant 5 tour\n")


		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement, puis soigne
			cible[0].pv += soin
			cible[0].effets = ("regeneration", tour_effet)
		else :
			cible.pv += soin
			cible.effets = ("regeneration", tour_effet)

		print("------\n")

	def all_info(self):
		return (decors_string + Soigneur.all_info(self) + self.__description_personnage + decors_string)

class TODO_FIND_NAME(Soigneur):
	def __init__(self, nom):
		
		pts_soin_modifier = 3
		pv_modifier = 5

		Soigneur.__init__(self, nom, pts_soin_modifier, pv_modifier)
		
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nLe TODO_FIND_NAME : soigne des PV à 2 alliés\nPortée : longue\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def soigner(self, cible: Personnage|list[Personnage]):
		soin = self.pts_soin

		distance = Personnage.distance(self)
		
		print("\n------\n\nSoin :\n")
		print("Distance : " + str(distance) + "\n")

		if (distance > 75) :	#distance bcp trop grande : le soin rate
			soin = 5
			print("La distance est beaucoup trop élevée : Le soin ratte : 5 PV soignés\n")
		elif (distance > 25) :	#distance trop grande : diminution de dégats linéaire jusqu'à 75 unitées de longeur
			soin = int(reduction_lineaire(distance, 25, 75, 5, soin))
			print("La distance est trop élevée : Soins diminués : " + str(soin) + " PV soignés\n")
		else :					#soin reussi
			print("La distance est courte : Le soin est un succès : " + str(soin) + " PV soignés\n")


		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement, puis soigne
			cible[0].pv += soin
		else :
			cible.pv += soin

		print("------\n")

	def all_info(self):
		return (decors_string + Soigneur.all_info(self) + self.__description_personnage + decors_string)

#CLASSES PALADINS

class Gardien(Paladin):
	def __init__(self, nom):
		
		pts_soin_modifier = -2
		pts_attaque_modifier = -2
		pv_modifier = 20

		Paladin.__init__(self, nom, pts_attaque_modifier, pts_soin_modifier, pv_modifier)
		
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nLe Gardien : soigne très de PV mais sur tous les aliés\ninflige des dégats faibles et l'effet paralyse sur 3 cibles \nPortée : longue\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def attaquer(self, cible: Personnage|list[Personnage]):

		print("\n------\n\nAttaque :\n")

		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement
			nombre_de_cibles = len(cible)
			if (nombre_de_cibles > 3):
				nombre_de_cibles = 3
		else :
			cible = [cible]				#transforme la cible (de type Personnage) en liste de Personnages
			nombre_de_cibles = 1

		while (nombre_de_cibles) :		#une attaque par cible

			degats = self.pts_attaque
			duree_effet = 1
			distance = Personnage.distance(self)

			print("Distance : " + str(distance) + "\n")

			if (distance > 66) :	#distance très grande : effet paralyse rate
				duree_effet = 0
				print("La distance est trop élevée : " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")
			elif (distance < 20) :	#distance très petite :  durée paralyse augmenté
				duree_effet = 2
				print("La distance est courte : paralyse pendant 2 tours ainsi que " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")
			else :					#attaque réussie
				print("La distance est moyenne : paralyse pendant 1 tours ainsi que " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")

			cible[nombre_de_cibles-1].pv -= degats
			if duree_effet :
				cible[nombre_de_cibles-1].effets = ("paralyse",duree_effet)
			nombre_de_cibles -= 1
		
		print("------\n")

	def soigner(self, cible: Personnage|list[Personnage]):			#NOT DONE!!
		soin = self.pts_soin
		
		print("\n------\n\nSoin :\n")
		
		if (type(cible) != list) :		#test si la cible n'est pas une liste de Personages
			cible = [cible]				#transforme la cible (de type Personnage) en liste de Personnages

		for allie in cible :
			distance = Personnage.distance(self)

			if (distance < 25) :	#distance très proche
				soin += 1			#total = 6PV
			elif (distance < 50) :	#distance moyenne
				pass				#total = 5PV
			elif (distance < 75) :	#distance grande
				soin -= 1			#total = 4PV
			else :					#distance trop grande
				soin -= 2			#total = 3PV

		allie.pv += soin

		print("Tous les alliés séléctionnés ont été soignés entre 3 et 6 PV\n")

		print("------\n")


	def all_info(self):
		return (decors_string + Paladin.all_info(self) + self.__description_personnage + decors_string)

class Templier(Paladin):			#TODO : soigner()
	def __init__(self, nom):
		
		pts_soin_modifier = 5
		pts_attaque_modifier = 5
		pv_modifier = 20

		Paladin.__init__(self, nom, pts_attaque_modifier, pts_soin_modifier, pv_modifier)
		
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nLe Gardien : soigne très de PV mais sur tous les aliés\ninflige des dégats faibles et l'effet paralyse sur 3 cibles \nPortée : longue\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def attaquer(self, cible: Personnage|list[Personnage]):

		print("\n------\n\nAttaque :\n")

		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement
			nombre_de_cibles = len(cible)
			if (nombre_de_cibles > 3):
				nombre_de_cibles = 3
		else :
			cible = [cible]				#transforme la cible (de type Personnage) en liste de Personnages
			nombre_de_cibles = 1

		while (nombre_de_cibles) :		#une attaque par cible

			degats = self.pts_attaque
			duree_effet = 1
			distance = Personnage.distance(self)

			print("Distance : " + str(distance) + "\n")

			if (distance > 66) :	#distance très grande : effet paralyse rate
				duree_effet = 0
				print("La distance est trop élevée : " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")
			elif (distance < 20) :	#distance très petite :  durée paralyse augmenté
				duree_effet = 2
				print("La distance est courte : paralyse pendant 2 tours ainsi que " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")
			else :					#attaque réussie
				print("La distance est moyenne : paralyse pendant 1 tours ainsi que " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")

			cible[nombre_de_cibles-1].pv -= degats
			if duree_effet :
				cible[nombre_de_cibles-1].effets = ("paralyse",duree_effet)
			nombre_de_cibles -= 1
		
		print("------\n")


	def soigner(self, cible: Personnage|list[Personnage]):			#NOT DONE!!
		soin = self.pts_soin
		
		print("\n------\n\nSoin :\n")
		
		if (type(cible) != list) :		#test si la cible n'est pas une liste de Personages
			cible = [cible]				#transforme la cible (de type Personnage) en liste de Personnages

		for allie in cible :
			distance = Personnage.distance(self)

			if (distance < 25) :	#distance très proche
				soin += 1			#total = 6PV
			elif (distance < 50) :	#distance moyenne
				pass				#total = 5PV
			elif (distance < 75) :	#distance grande
				soin -= 1			#total = 4PV
			else :					#distance trop grande
				soin -= 2			#total = 3PV

		allie.pv += soin

		print("Tous les alliés séléctionnés ont été soignés entre 3 et 6 PV\n")

		print("------\n")

	def all_info(self):
		return (decors_string + Paladin.all_info(self) + self.__description_personnage + decors_string)

class Chevalier(Paladin):
	def __init__(self, nom):
		
		pts_soin_modifier = 5
		pts_attaque_modifier = 2
		pv_modifier = 15

		Paladin.__init__(self, nom, pts_attaque_modifier, pts_soin_modifier, pv_modifier)
		
		self.__description_personnage = "-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\nLe Chevalier : soigne ses propres PV ainsi que se donne l'effet régéneration\nPeut attaquer 2 cibles à la fois\nPortée : moyenne\n-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-\n"

	def attaquer(self, cible: Personnage|list[Personnage]):

		print("\n------\n\nAttaque :\n")

		if (type(cible) == list) :		#test si la cible est une liste de Personages ou un Personnage directement
			nombre_de_cibles = len(cible)
			if (nombre_de_cibles > 2):
				nombre_de_cibles = 2
		else :
			cible = [cible]				#transforme la cible (de type Personnage) en liste de Personnages
			nombre_de_cibles = 1

		while (nombre_de_cibles) :		#une attaque par cible

			degats = self.pts_attaque
			distance = Personnage.distance(self)

			print("Distance : " + str(distance) + "\n")

			if (distance > 75) :	#distance trop grande : attaque rate
				print("La distance est beacoup trop élevée : l'attaque rate et inflige 0 dégats à " + cible[nombre_de_cibles-1].nom + "\n")
			elif (distance > 50) :	#distance très grande : dégats diminués
				degats = int(reduction_lineaire(distance, 50, 75, 1, degats))
				print("La distance est trop élevée : Dégats diminués : " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")
			else :					#attaque réussie
				print("L'attaque est un succès, " + str(degats) + " dégats infligés à " + cible[nombre_de_cibles-1].nom + "\n")
			cible[nombre_de_cibles-1].pv -= degats

			nombre_de_cibles -= 1
		
		print("------\n")


	def soigner(self, cible: Personnage|list[Personnage]):
		soin = self.pts_soin
		tour_effet = 7
		
		print("\n------\n\nSoin :\n")
		
		self.pv += soin
		self.effets = ("regeneration", tour_effet)

		print(self.nom + " s'est régéneré " + str(soin) + " PV et a obtenu l'effet régéneration pendant " + str(tour_effet) + " tours\n")

		print("------\n")

	def all_info(self):
		return (decors_string + Paladin.all_info(self) + self.__description_personnage + decors_string)



#LISTE DE CLASSES

liste_personnages_classes = [Barbare, Archer, Assassin, Mage, SorcierDeChaos, Pretre, Druide, TODO_FIND_NAME, Gardien, Templier, Chevalier]
liste_guerrier_classes = [Barbare, Archer, Assassin, Mage, SorcierDeChaos]
liste_soigneur_classes = [Pretre, Druide, TODO_FIND_NAME]
liste_paladin_classes = [Gardien, Templier, Chevalier]



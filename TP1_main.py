
import random as r
import warnings as w


from TP1_global_variables import *

from TP1_functions import *

from TP1_classes_persos import *

from TP1_GUI import *


class Joueur:
	nombre_de_joueurs = 0
	def __init__(self):
		'''Cette fonction permet d'initialiser un joueur'''
		Joueur.nombre_de_joueurs += 1
		self.__numero_joueur = Joueur.nombre_de_joueurs
		self.__personnages = []

	@property
	def numero_joueur(self):
		return self.__numero_joueur

	@property
	def personnages(self):
		return self.__personnages

	def afficher_personnages(self):
		'''
		Affiche la liste des Personnages du joueur
		'''
		print("liste des personnage de joueur " + str(self.__numero_joueur) + ":\n")
		for p in self.__personnages :
			print(p.all_info())

	def update_personnages(self):
		'''Cette fonction met à jour les personnages en rapport avec leur effets (eg poison, regeneration) ainsi que si le personnage est mort'''
		return_string = "\n"
		for p in self.__personnages :
			if p.pv <= 0:
				self.__personnages.remove(p)	#mort du personnage
				return_string += "Le personnage " + p.nom + " est mort\n"
			else :
				for effet in p.effets :
					if p.effets[effet] > 0 :
						p.effets[effet] -= 1
						if effet == "regeneration" :
							p.pv += 5
							return_string += "Le personnage " + p.nom + " s'est soigné 5 PV par l'effet régenération\n"
						if effet == "poison" :
							p.pv -= 5
							return_string += "Le personnage " + p.nom + " s'est bléssé de 5 PV par l'effet poison\n"
							if p.pv <= 0:
								self.__personnages.remove(p)	#verifie la mort du personnage encore une fois
								return_string += "Le personnage " + p.nom + " est mort\n"
		return return_string

class Jeu:
	def __init__(self):
		self.__tour = 0
		self.__joueurs = []
		self.__personnage_selectionne = None
		self.__cibles = []	#Cibles selectionnées (Personnages alliés ou ennemis)
		for _ in range(2):
			joueur = Joueur()
			for _ in range(nombre_de_personnages):
				self.creer_personnage(joueur)
			self.__joueurs.append(joueur)

	@property
	def joueurs(self):
		return self.__joueurs

	@property
	def tour(self):
		return self.__tour

	@tour.setter
	def tour(self, new_tour):
		self.__tour = new_tour

	@property
	def cibles(self):
		return self.__cibles

	@cibles.setter
	def cibles(self, new_cibles):
		self.__cibles = new_cibles

	@property
	def personnage_selectionne(self):
		return self.__personnage_selectionne

	@personnage_selectionne.setter
	def personnage_selectionne(self, new_personnage_selectionne : Personnage):
		self.__personnage_selectionne = new_personnage_selectionne


	def creer_personnage(self, joueur : Joueur, nom = None, classe = None):
		'''
		Crée un personnage avec le nom et classe fournis et l'ajoute à la liste de personnages du joueur, si le nom ou classe ne sont pas fournis, ils seront choisis aléatoirement
		'''
		#genère un nom et titre epique aléatoire (si non fourni)
		personnage_nom_couleur = ("blue" if joueur.numero_joueur%2 == 1 else "green")
		if not nom :		#teste si le nom est None ou ""
			nom = random_name()
		personnage_nom = color_string(nom,personnage_nom_couleur,couleurs_autorise_bool)

		#genère une classe aléatoire (si non fournie)
		if (type(classe) == str and str(classe) in liste_personnages_classes_string):	#Utilisé pour la création de personnages par les boutons
			if str(classe) in globals():
				classe = globals()[str(classe)]
			else:
				print(f"Error: class {str(classe)} not found")
		if classe not in liste_personnages_classes :
			classe = r.choice(liste_personnages_classes)
		personnage = classe(personnage_nom)

		#ajout du personnage à la liste de personnages du joueur
		joueur.personnages.append(personnage)


if __name__ == "__main__":
	'''Ici commence le programme pour le jeu entier'''
	jeu = Jeu()

	app = Application(jeu)
	app.mainloop()

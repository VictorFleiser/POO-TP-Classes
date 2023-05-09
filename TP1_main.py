
import random as r
import warnings as w


from TP1_global_variables import *

from TP1_functions import *

from TP1_classes_persos import *

from TP1_GUI import *

class Joueur:
	nombre_de_joueurs = 0
	def __init__(self, nombre_de_personnages):
		Joueur.nombre_de_joueurs += 1
		self.__numero_joueur = Joueur.nombre_de_joueurs
		self.__personnages = []
#		self.__cibles = []	#Cibles selectionnées (Personnages alliés ou ennemis)

		#Génération des personnages :
#		for _ in range(nombre_de_personnages):
#			self.creer_personnage()
#		
		self.afficher_personnages()

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


class Jeu:
	def __init__(self):
		self.__tour = 0
		self.__nombre_de_joueurs = nombre_de_joueurs
		self.__joueurs = []
		self.__personnage_selectionne = None
		self.__cibles = []	#Cibles selectionnées (Personnages alliés ou ennemis)
		for _ in range(nombre_de_joueurs):
			joueur = Joueur(nombre_de_personnages)
			for _ in range(nombre_de_personnages):
				self.creer_personnage(joueur)
			self.__joueurs.append(joueur)

	@property
	def joueurs(self):
		return self.__joueurs

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

	def selection_cible(self, personnage: Personnage|list[Personnage]):
		'''
		Ajoute le/s personnage/s ciblé/s dans la liste des personnages ciblés
		ou
		Enlève le/s personnage/s ciblé/s de la liste des personnages ciblés si ils sont déjà dans la liste
		'''

		if (type(personnage) != list) :		#test si la cible est une liste de Personages ou un Personnage directement
			personnage = [personnage]		#transforme la cible (de type Personnage) en liste de Personnages

		if (len(personnage) == 0):
			return

		for p in personnage:
			if(p in self.cibles):
				self.cibles.remove(p)
			else:
				self.cibles.append(p)

	def selection_personnage(self, personnage : Personnage):
		'''
		Séléctionne le personnage
		'''
		self.selection_personnage = personnage

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
		if classe not in liste_personnages_classes :
			classe = r.choice(liste_personnages_classes)
		personnage = classe(personnage_nom)

		#ajout du personnage à la liste de personnages du joueur
		joueur.personnages.append(personnage)

	def action(self, joueur : Joueur, type_action : str):
		'''
		Effectue une action (attaque ou soin) du personnage selectionné, affecte les cibles séléctionnées
		'''
		#test si c'est bien le tour du joueur
		if (self.__tour%(Joueur.nombre_de_joueurs) == joueur.numero_joueur):
			print("Ce n'est pas le tour du joueur séléctionné")
			return 0

		#test si le personnage selectionné appartient au joueur
		if (self.__personnage_selectionne not in joueur.personnages):
			print("Le personnage séléctionné n'appartient pas au joueur")
			return 0

		#teste si le personnage selectionné est paralysé
		if (self.__personnage_selectionne.effets["paralyse"]):
			print("Le personnage selectionné ne peut pas faire d'actions car il est paralysé")
			return 0

		#teste si le personnage possède bien l'action attaquer
		if (type_action == 'attaquer'):
			try : 
				self.__personnage_selectionne.attaquer(self.__cibles)
				return 1
			except AttributeError :
				print("Le personnage selectionné est un soigneur en ne peut pas attaquer")
				return 0

		#teste si le personnage possède bien l'action soigner
		if (type_action == 'soigner'):
			try : 
				self.__personnage_selectionne.soigner(self.__cibles)
				return 1
			except AttributeError :
				print("Le personnage selectionné est un guerrier en ne peut pas soigner")
				return 0

'''
		#AUTRE METHODE : MEILLEURE MAIS N'UTILISE PAS D'EXCEPTIONS :

		#teste si le personnage possède bien l'action voulue
		if hasattr(self.__personnage_selectionne, type_action):
			action = getattr(self.__personnage_selectionne, type_action)
			action(self.__cibles)
'''	



if __name__ == "__main__":

	jeu = Jeu()


	app = Application(jeu)
	app.mainloop()
	print("ba")

	'''
	#TESTS :

	bob = Barbare(color_string("Bob le courageux","green",couleurs_autorise_bool))
	fred = Archer("Fred l'oeuil de faucon")
	michael = Assassin("Michael le vicieux")
	john = Pretre("John le croyant")
	marc = Mage("Marc l'incendiaire")
	chuni = SorcierDeChaos("Chuni l'impredictible")
	sylvain = Druide("Sylvain le soigneur")
	gerald = Gardien("Gerald le protecteur")
	jean = Chevalier("Jean le preux")
	rname1 = TODO_FIND_NAME(color_string(random_name(),"green",couleurs_autorise_bool))


	print(michael.all_info())
	fred.attaquer(bob)
	michael.attaquer(bob)
	print(bob.all_info())

	cibles = [bob, fred, john, marc, michael]

	john.soigner(cibles)
	john.soigner(bob)
	print(bob.all_info())

	marc.attaquer(cibles)
	marc.attaquer(bob)
	print(bob.all_info())
	print(fred.all_info())
	print(michael.all_info())
	print(john.all_info())
	print(marc.all_info())
	print(chuni.all_info())

	sylvain.soigner(bob)
	gerald.attaquer(cibles)

	jean.attaquer(cibles)
	jean.soigner(marc)
	
	rname1.soigner(marc)

	print(rname1.all_info())
	'''

	'''
	J1 = Joueur(3)
	J2 = Joueur(2)
	J3 = Joueur(1)

	J1.creer_personnage()
	J1.creer_personnage("Nyan Nyan le chat",Barbare)
	J1.afficher_personnages()
	J1.action(J1.personnages[3], 'attaquer', cibles)
	'''
	'''
	jeu = Jeu()

	jeu.creer_personnage(jeu.joueurs[0],"",Assassin)
	jeu.creer_personnage(jeu.joueurs[0],"Nyan Nyan le chat",Barbare)
	jeu.joueurs[0].afficher_personnages()

	jeu.cibles = cibles
	jeu.personnage_selectionne = jeu.joueurs[0].personnages[0]

	jeu.action(jeu.joueurs[0], 'attaquer')


	joueur_1_personnages = [str(bob), str(fred), michael, john, marc]
	joueur_2_personnages = [chuni, sylvain, gerald, jean, rname1]

	app = Application(joueur_1_personnages, joueur_2_personnages)
	app.mainloop()



	#	gerald.soigner(bob)		not implemented yet



				#IDEA : JESTER : BUFFER/DEBUFFER


#	bob.attaquer(fred)
#	fred.attaquer(bob)
#	print(bob.all_info())
#	print(fred.all_info())


#	print(str(reduction_lineaire(5, 50, 75, 15, 0)))

'''
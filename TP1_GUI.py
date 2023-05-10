bg_color = "#333333"

import tkinter as tk
from tkinter import messagebox
import random
import math
from TP1_global_variables import *
from tkinter import ttk

class Application(tk.Tk):

	def __init__(self, jeu):
		'''initialisation de l'app : '''
		# on crée la fenêtre principale
		tk.Tk.__init__(self)
		self.title("Victor_Fleiser_POO")
		height = 600
		width = 800
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		self.configure(bg = bg_color)
		self.geometry(f"{width}x{height}+{(screen_width - width) // 2}+{(screen_height - height) // 2}")
		self.resizable(1, 1)		#allow resizing the window
		self.minsize(575,215)

		self.jeu = jeu

		# variables utilisées pour les modes de jeu secrets changeant le visuel de la fenêtre (cf : DVD et Rainbow tout en bas de ce fichier)
		self.secret_bouncing_dvd_animation_bool = False
		self.secret_rainbow_bg_bool = False
		self.color_index = 0

		# variables utilisées lors de la création de nouveaux personnages pour transférer les valeurs entre 2 fenêtres
		self.perso_custom_nom = ""
		self.perso_custom_classe = ""

		# liste des noms des personnages de chaque joueurs
		self.joueur_1_noms_personnages = [p.nom for p in jeu.joueurs[0].personnages]
		self.joueur_2_noms_personnages = [p.nom for p in jeu.joueurs[1].personnages]
		# on met les noms dans une tk.Variable pour les afficher dans une listebox
		self.joueur_1_noms_personnages_var = tk.Variable(value=self.joueur_1_noms_personnages)
		self.joueur_2_noms_personnages_var = tk.Variable(value=self.joueur_2_noms_personnages)

		# string stockant les informations à afficher dans les textbox
		self.info_personnage_joueur_1 = ""
		self.info_personnage_joueur_2 = ""
		self.info_jeu = ""

		#liste des personnages selectionnés
		self.selected_list_joueur_1 = []
		self.selected_list_joueur_2 = []

		# on crée les widgets
		self.creer_widgets()

		self.bind("<Escape>", self.stop)

	
	def move_resize_window(self, final_position=(0, 0), move_type="none", final_size=(0, 0), resize_type="none", duration=1000, step_length=10):
		'''Cette fonction permet de déplacer et redimensionner la fenêtre.
		Il y a 3 types d'accélérations : ease_in (commence lent et accélère avant de s'arréter), ease_out (commence rapide et ralentit à la fin), ease_in_out (combinaison des deux).
		Plus step_length est faible, plus il y aura d'étapes dans le mouvement, à calibrer en relation à duration (la durée)
		La durée est censée être en milisecondes mais ne fonctionne pas correctement et dure plus longtempt
		'''
		# DISCLAIMER : cette fonction ainsi que celle associée (get_easing_function) on étées crées en partie grâce à ChatGPT

		if (move_and_resize_window_with_actions_bool) :

			# on récupère la position et la taille actuelles de la fenêtre
			current_x, current_y = self.winfo_x(), self.winfo_y()
			current_width, current_height = self.winfo_width(), self.winfo_height()

			# on calcule la position et la taille finales relatives à la position et la taille initiales
			final_x, final_y = current_x + final_position[0], current_y + final_position[1]
			final_width, final_height = current_width + final_size[0], current_height + final_size[1]

			# on calcule la fonction d'accélération à utiliser pour le mouvement et le redimensionnement
			move_easing = self.get_easing_function(move_type)
			resize_easing = self.get_easing_function(resize_type)

			# on calcule la durée du mouvement et du redimensionnement en fonction de la fonction d'accélération
			move_duration = duration if move_type == "none" else int(move_easing(1.0) * duration)
			resize_duration = duration if resize_type == "none" else int(resize_easing(1.0) * duration)

			# on déplace et redimensionne la fenêtre en utilisant la fonction d'accélération et la durée
			for t in range(0, max(move_duration, resize_duration) + 1, step_length):
				# on calcule la position et la taille à l'étape de temps actuelle
				x = int(current_x + (final_x - current_x) * move_easing(t / move_duration))
				y = int(current_y + (final_y - current_y) * move_easing(t / move_duration))
				width = int(current_width + (final_width - current_width) * resize_easing(t / resize_duration))
				height = int(current_height + (final_height - current_height) * resize_easing(t / resize_duration))
				self.geometry("{}x{}+{}+{}".format(width, height, x, y))
				self.update()
				self.after(step_length)


	def get_easing_function(self, easing_type):
		'''retourne la fonction d'accélération associée à l'argument'''
		# DISCLAIMER : cette fonction ainsi que celle associée (move_resize_window) on étées crées en partie grâce à ChatGPT
		if easing_type == "ease_in":
			return lambda t: t * t
		elif easing_type == "ease_out":
			return lambda t: 1 - (1 - t) * (1 - t)
		elif easing_type == "ease_in_out":
			return lambda t: (3 - 2 * t) * t * t
		else:
			return lambda t: t


	def move_window_in_a_circle(self, duration=50, radius=15, steps=20):
		'''fonction bougeant la fenêtre en forme de cercle
		note : la durée ne fonctionne pas correctement, et des valeurs extrèmes pour les arguments peuvent avoir des conséquences imprévues'''
		# on génére tous les points à visiter
		points = []
		for i in range(steps) :
			n_x = int(radius * math.cos(i * (2 * math.pi)/steps))
			n_y = int(radius * math.sin(i * (2 * math.pi)/steps))
			points.append((n_x,n_y))
		points.append((radius,0))

		# on déplace la fenêtre à travers tous les points à visiter
		for i in range(1,steps+1) :
			# on calcul le vecteur du prochain déplacement
			vector = (points[i][0]-points[i-1][0],points[i][1]-points[i-1][1])
			self.move_resize_window(final_position=vector, move_type="none", duration=int(duration/steps), step_length=int(duration/steps))


	def enlarge_window(self, duration=500, enlarge_amount=(0,0)):
		'''Cette fonction est similaire à move_resize_window() mais reste centrée'''
		# on récupère la position et la taille actuelles de la fenêtre
		start_width, start_height = self.winfo_width(), self.winfo_height()
		start_x, start_y = self.winfo_x(), self.winfo_y()

		# on calcule la position et la taille finales relatives à la position et la taille initiales
		new_width = start_width + enlarge_amount[0]
		new_height = start_height + enlarge_amount[1]
		new_x = start_x - enlarge_amount[0] // 2
		new_y = start_y - enlarge_amount[1] // 2

		# on déplace et redimensionne la fenêtre
		self.move_resize_window(final_position=(new_x - start_x, new_y - start_y), move_type="none", final_size=(new_width - start_width, new_height - start_height), resize_type="none", duration=duration)


	def get_personnage_from_name(self, name) :
		'''La fonction cherche le personnage dont le nom correspond à celui en paramètre et renvoie le personnage si il existe'''
		r = [p for p in self.jeu.joueurs[0].personnages if p.nom == name] + [p for p in self.jeu.joueurs[1].personnages if p.nom == name]
		if (len(r)) :
			return r[0]		#on retourne la première occurence
		else :
			return None		#on ne retourne rien si le personnage n'est pas présent
		

	def update_info_box_content(self):
		'''Cette fonction permet de mettre à jour le contenu des textbox avec les infos sur les derniers personnages séléctionnés
		ainsi que la textbox avec les informations sur le dernier tour'''
		#On met à jour les 2 string contenant le texte à afficher des 2 textbox
		if (len(self.selected_list_joueur_1)) :
			try : 
				self.info_personnage_joueur_1 = self.get_personnage_from_name(self.selected_list_joueur_1[-1]).all_info()
			except :	#peut se produire si le personnage mort durant le tour du joueur le possèdant, mais n'a aucune influence
				self.info_personnage_joueur_1 = "Aucun personnage selectionné\n" + str(len(self.jeu.joueurs[0].personnages)) + " personnages restants.\n"
		else :
			self.info_personnage_joueur_1 = "Aucun personnage selectionné\n" + str(len(self.jeu.joueurs[0].personnages)) + " personnages restants.\n"

		if (len(self.selected_list_joueur_2)) :
			try : 
				self.info_personnage_joueur_2 = self.get_personnage_from_name(self.selected_list_joueur_2[-1]).all_info()
			except :	#peut se produire si le personnage mort durant le tour du joueur le possèdant, mais n'a aucune influence
				self.info_personnage_joueur_2 = "Aucun personnage selectionné\n" + str(len(self.jeu.joueurs[1].personnages)) + " personnages restants.\n"
		else :
			self.info_personnage_joueur_2 = "Aucun personnage selectionné\n" + str(len(self.jeu.joueurs[1].personnages)) + " personnages restants.\n"

		#on supprime le contenu des textbox pour insérer le nouveau texte
		self.info_joueur_1_text_widget.delete('1.0', 'end')
		self.info_joueur_1_text_widget.insert('end', self.info_personnage_joueur_1)

		self.info_joueur_2_text_widget.delete('1.0', 'end')
		self.info_joueur_2_text_widget.insert('end', self.info_personnage_joueur_2)			

		self.info_jeu_text_widget.delete('1.0', 'end')
		self.info_jeu_text_widget.insert('end', "Tour : " + str(self.jeu.tour) + "\n")
		self.info_jeu_text_widget.insert('end', self.info_jeu)		
		self.info_jeu_text_widget.insert('end', "C'est au tour du joueur : " + str((self.jeu.tour)%2+1) + "\n")	


	def update_listbox_content(self):
		'''Cette fonction met à jour le texte à l'intérieur des listbox avec les personnages des joueurs'''
		#on met à jour les listes des noms des personnages des joueurs
		self.joueur_1_noms_personnages = [p.nom for p in self.jeu.joueurs[0].personnages]
		self.joueur_2_noms_personnages = [p.nom for p in self.jeu.joueurs[1].personnages]
		
		#2 methodes pour remplacer le texte de la liste (je garde les 2 juste au cas où) :
		# on supprime le contenu des listbox pour insérer les nouveaux textes

		#methode 1
		self.joueur_1_personnages_listbox_widget.delete(0, tk.END)
		self.joueur_1_personnages_listbox_widget.insert(0, *[string for string in self.joueur_1_noms_personnages])

		#methode 2
		self.joueur_2_personnages_listbox_widget.delete(0, tk.END)
		for string in self.joueur_2_noms_personnages:
			self.joueur_2_personnages_listbox_widget.insert("end", string)


	def on_select(self, event):
		'''Cette fonction permet de trouver le dernier personnage séléctionné du widget correspondant à l'event et de l'ajoute/enlever de la liste des personnages séléctionnés'''
		# on récupère de dernier élément sélectionné
		widget = event.widget
		index = widget.nearest(event.y)
		selected_element = widget.get(index)

		# on determine à quel joueur appartient le personnage sélectionné
		if widget == self.joueur_1_personnages_listbox_widget:
			selected_list = self.selected_list_joueur_1
		else:
			selected_list = self.selected_list_joueur_2

		# on ajoute ou enlève l'élément de la liste des personnages séléctionnés
		if selected_element in selected_list:
			selected_list.remove(selected_element)
		else:
			selected_list.append(selected_element)

		# on met également à jour la textbox affichant les infos du dernier personnage séléctionné
		self.update_info_box_content()


	def deselect_all(self):
		'''Cette fonction permet de déselectionner tous les personnages dans la listbox ainsi que les enlever de la liste des personnages sélections'''
		#list box du joueur 1
		for i in range(self.joueur_1_personnages_listbox_widget.size()):
			element1 = self.joueur_1_personnages_listbox_widget.get(i)
			if element1 in self.selected_list_joueur_1:
				self.selected_list_joueur_1.remove(element1)
#				self.joueur_1_personnages_listbox_widget.itemconfig(i, bg="white", fg="black")
		#list box du joueur 2
		for i in range(self.joueur_2_personnages_listbox_widget.size()):
			element2 = self.joueur_2_personnages_listbox_widget.get(i)
			if element2 in self.selected_list_joueur_2:
				self.selected_list_joueur_2.remove(element2)
#				self.joueur_2_personnages_listbox_widget.itemconfig(i, bg="white", fg="black")


	def creer_widgets(self):
		'''Cette fonction permet d'intialiser les widgets'''
		# on définie l'architecture de la grid
		self.columnconfigure(0, minsize=200, weight=3)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, minsize=200, weight=3)
		self.rowconfigure(0, minsize=65, weight=1)
		self.rowconfigure(1, minsize=150, weight=1)
		self.rowconfigure(2, minsize=150, weight=1)

		#Info box du personnage sélectionné en dernier du joueur 1
		self.info_joueur_1_text_widget=tk.Text(self, height=40, bg="#222222", foreground=default_text_color)
		self.info_joueur_1_text_widget.insert('insert',self.info_personnage_joueur_1)
		self.info_joueur_1_text_widget.grid(column=0, row=1, columnspan = 2, sticky=tk.NW, padx=3, pady=3)

		#Info box du personnage sélectionné en dernier du joueur 2
		self.info_joueur_2_text_widget=tk.Text(self, height=40, bg="#222222", foreground=default_text_color)
		self.info_joueur_2_text_widget.insert('insert',self.info_personnage_joueur_2)
		self.info_joueur_2_text_widget.grid(column=2, row=1, columnspan = 2, sticky=tk.NE, padx=3, pady=3)

		#Info box du jeu 
		self.info_jeu_text_widget=tk.Text(self, height=40, bg="#222222", foreground=default_text_color)
		self.info_jeu_text_widget.insert('insert',self.info_jeu)
		self.info_jeu_text_widget.grid(column=0, row=2, columnspan = 4, sticky=tk.S, padx=3, pady=3)

		# on met à jour les info box
		self.update_info_box_content()

		# Liste des personnages du joueur 1
		self.joueur_1_personnages_listbox_widget = tk.Listbox(self, 
			height=100, 
			listvariable=self.joueur_1_noms_personnages_var, 
			bg="#222", 
			selectbackground="blue", 
			selectmode=tk.MULTIPLE, 	#permet de selectionner plusieurs élements
			exportselection=False,		#empeche d'autres listbox d'enlever les selections de cette listbox
			foreground=default_text_color
			)
		self.joueur_1_personnages_listbox_widget.grid(column=0, row=0, sticky=tk.EW, padx=5, pady=5, ipadx=5, ipady=5)
		self.joueur_1_personnages_listbox_widget.bind("<ButtonPress-1>", self.on_select)

		# Liste des personnages du joueur 2
		self.joueur_2_personnages_listbox_widget = tk.Listbox(self, 
			height=100, 
			listvariable=self.joueur_2_noms_personnages_var, 
			bg="#222", 
			selectbackground="green",
			selectmode=tk.MULTIPLE, 	#permet de selectionner plusieurs élements
			exportselection=False,		#empeche d'autres listbox d'enlever les selections de cette listbox
			foreground=default_text_color
			)
		self.joueur_2_personnages_listbox_widget.grid(column=3, row=0, sticky=tk.EW, padx=5, pady=5, ipadx=5, ipady=5)
		self.joueur_2_personnages_listbox_widget.bind("<ButtonPress-1>", self.on_select)

		# Bouton attaquer
		self.attaquer_button_widget = tk.Button(self, text="attaquer", highlightbackground=bg_color, activeforeground = "red", foreground="black", command=lambda: [self.action("attaquer"), self.deselect_all(), self.update_listbox_content(), self.update_info_box_content(), self.change_bg_color("#F00", bg_color, 500),self.enlarge_window(duration=50, enlarge_amount=(10,10)),self.enlarge_window(duration=50, enlarge_amount=(-10,-10))])
		self.attaquer_button_widget.grid(column=1, row=0, sticky=tk.EW, padx=2)

		# Bouton soigner
		self.soigner_button_widget = tk.Button(self, text="soigner", highlightbackground=bg_color, activeforeground = "yellow", foreground="black", command=lambda: [self.action("soigner"), self.update_listbox_content(), self.deselect_all(), self.update_info_box_content(), self.change_bg_color("#FF0", bg_color, 500),self.move_window_in_a_circle()])
		self.soigner_button_widget.grid(column=2, row=0, sticky=tk.EW, padx=2)

		# Bouton pour passer son tour
		self.passer_tour_button_widget = tk.Button(self, text="passer le tour", highlightbackground=bg_color, activeforeground = "white", foreground="black", command=lambda: [self.activate_secret_options(), self.action("nothing"), self.update_listbox_content(), self.deselect_all(), self.update_info_box_content(), self.change_bg_color("#FFF", bg_color, 500), self.enlarge_window(duration=200, enlarge_amount=(-20,-20)), self.enlarge_window(duration=200, enlarge_amount=(20,20))])
		self.passer_tour_button_widget.grid(column=1, row=0, columnspan = 2, sticky=tk.S, padx=2)

		# Bouton de Tests [IGNORER]
#		self.change_color_button_widget = tk.Button(self, text="tests", command= lambda: [self.bouncing_dvd_animation(), self.change_bg_color("#FF0", bg_color, 500), self.deselect_all(), self.move_window_in_a_circle(), self.enlarge_window(enlarge_amount=(10,10)),self.move_resize_window(final_position=(200,0), move_type="ease_in_out", final_size=(-10,-10), resize_type="ease_in_out", duration=2000)])
#		self.change_color_button_widget.grid(column=1, row=1, sticky=tk.EW, padx=2)

		# Bouton ajouter personnage pour joueur 1 [IGNORER]
#		self.ajouter_personnage_J1_button_widget = tk.Button(self, text="Ajouter Personnage", highlightbackground=bg_color, activeforeground = "blue", command=lambda: [self.jeu.creer_personnage(self.jeu.joueurs[0]), self.update_listbox_content(), self.deselect_all(), self.update_info_box_content(), self.change_bg_color("#00F", bg_color, 500), self.move_resize_window(duration=100, final_position=(0,20)), self.move_resize_window(duration=100, final_position=(0,-20))])
#		self.ajouter_personnage_J1_button_widget.grid(column=0, row=2, sticky=tk.SW, padx=2)

		# Bouton ajouter personnage pour joueur 2 [IGNORER]
#		self.ajouter_personnage_J2_button_widget = tk.Button(self, text="Ajouter Personnage", highlightbackground=bg_color, activeforeground = "green", command=lambda: [self.jeu.creer_personnage(self.jeu.joueurs[1]), self.update_listbox_content(), self.deselect_all(), self.update_info_box_content(), self.change_bg_color("#0F0", bg_color, 500), self.move_resize_window(duration=100, final_position=(0,-20)), self.move_resize_window(duration=100, final_position=(0,20))])
#		self.ajouter_personnage_J2_button_widget.grid(column=3, row=2, sticky=tk.SE, padx=2)

		# Bouton ajouter personnage pour joueur 1 VERSION 2
		self.ajouter_personnage_J1_button_widget = tk.Button(self, text="Ajouter Personnage", highlightbackground=bg_color, activeforeground = "blue", foreground="black", command=lambda: [self.creer_personnage(0), self.update_listbox_content(), self.deselect_all(), self.update_info_box_content(), self.change_bg_color("#00F", bg_color, 500), self.move_resize_window(duration=100, final_position=(0,20)), self.move_resize_window(duration=100, final_position=(0,-20))])
		self.ajouter_personnage_J1_button_widget.grid(column=0, row=2, sticky=tk.SW, padx=2)

		# Bouton ajouter personnage pour joueur 2 VERSION 2
		self.ajouter_personnage_J2_button_widget = tk.Button(self, text="Ajouter Personnage", highlightbackground=bg_color, activeforeground = "green", foreground="black", command=lambda: [self.creer_personnage(1), self.update_listbox_content(), self.deselect_all(), self.update_info_box_content(), self.change_bg_color("#0F0", bg_color, 500), self.move_resize_window(duration=100, final_position=(0,-20)), self.move_resize_window(duration=100, final_position=(0,20))])
		self.ajouter_personnage_J2_button_widget.grid(column=3, row=2, sticky=tk.SE, padx=2)


	def change_bg_color(widget, start_color, end_color, duration):
		'''Cette fonction permet de changer la couleur de fond de la fenêtre'''
		# nombre d'étapes ainsi que délai entre les étapes
		steps = 30					#nombre d'étapes du changement de couleur
		delay = duration // steps	#délai entre les étapes

		# on récupère les valeurs RGB de la couleur d'origine et de fin
		r1, g1, b1 = widget.winfo_rgb(start_color)
		r2, g2, b2 = widget.winfo_rgb(end_color)
		# on change la couleur par étapes
		r_step = (r2 - r1) / steps
		g_step = (g2 - g1) / steps
		b_step = (b2 - b1) / steps
		for i in range(steps):
			r = int(r1 + i * r_step)
			g = int(g1 + i * g_step)
			b = int(b1 + i * b_step)
			color = f"#{r:04x}{g:04x}{b:04x}"
			widget.after(delay * i, widget.config, {"bg": color})
		widget.after((steps+1)*delay, widget.config, {"bg" : end_color})


	def action(self,type_action) :
		'''Cette fonction effectue l'action donnée du dernier personnage du joueur actif, elle met à jour également le texte d'information du jeu'''
		if (type_action == "nothing"): 
			action_sucess = True
			self.info_jeu = 'Le joueur n\'a rien fait.\n'
		else :
			personnage_actif = None
			allied_targets = None
			enemy_targets = None
			#on récupère le personnage faisant l'action et les cibles de son action
			if (self.jeu.tour%2 == 0) :	#tour du Joureur 1
				if (len(self.selected_list_joueur_1)) :
					personnage_actif = self.get_personnage_from_name(self.selected_list_joueur_1[-1])
				enemy_targets = [self.get_personnage_from_name(p) for p in self.selected_list_joueur_2]
				allied_targets = [self.get_personnage_from_name(p) for p in self.selected_list_joueur_1]
			else :						#tour du joueur 2
				if (len(self.selected_list_joueur_2)) :
					personnage_actif = self.get_personnage_from_name(self.selected_list_joueur_2[-1])
				enemy_targets = [self.get_personnage_from_name(p) for p in self.selected_list_joueur_1]
				allied_targets = [self.get_personnage_from_name(p) for p in self.selected_list_joueur_2]

			#on effectue l'action et on met à jour la textbox d'informations sur le jeu
			action_sucess = False
			self.info_jeu = 'something went wrong ?'	#texte par default qui ne devrai jamais être affiché
			if type_action == "attaquer" :
				if (personnage_actif and  personnage_actif.effets["paralyse"] > 0) :	#personnage paralysé
					self.info_jeu = "Le personnage selectionné est paralysé et ne peut pas attaquer\n"
				else :
					if (len(enemy_targets)) :	#on vérifie si au moins une cible est séléctionnée
						try : 
							self.info_jeu = personnage_actif.attaquer(enemy_targets)
							action_sucess = True
						except AttributeError as e:
							if personnage_actif is None:		#aucun personnage n'est séléctionné pour attaquer
								messagebox.showinfo("Aucun personnage selectionné pour attaquer", str(e))
								self.info_jeu = "Aucun personnage selectionné pour attaquer\n"
							elif not hasattr(personnage_actif, 'attaquer'):		#le personnage séléctionné n'a pas de méthode attaquer
								messagebox.showinfo("Ce personnage (" + personnage_actif.nom + ") ne possède pas l'action attaquer", str(e))
								self.info_jeu = "Ce personnage (" + personnage_actif.nom + ") ne possède pas l'action attaquer\n"
							else :
								raise e
							action_sucess = False
					else :	# Aucun ennemi séléctionné à attaquer
						messagebox.showinfo("aucun ennemi séléctionné à attaquer", str("aucun ennemi séléctionné à attaquer"))
						self.info_jeu = "aucun ennemi séléctionné à attaquer\n"
						action_sucess = False

			if type_action == "soigner" :
				try :
					if (personnage_actif.effets["paralyse"] > 0) :	#personnage paralysé
						self.info_jeu = "Le personnage selectionné est paralysé et ne peut pas soigner\n"
					else :
						if (len(allied_targets)) :	#on vérifie si au moins une cible est séléctionnée
							try :
								self.info_jeu = personnage_actif.soigner(allied_targets)
								action_sucess = True
							except AttributeError as e:
								if personnage_actif is None:		#aucun personnage n'est séléctionné pour attaquer
									messagebox.showinfo("Aucun personnage selectionné pour soigner", str(e))
									self.info_jeu = "Aucun personnage selectionné pour soigner\n"
								elif not hasattr(personnage_actif, 'soigner'):		#le personnage séléctionné n'a pas de méthode attaquer
									messagebox.showinfo("Ce personnage (" + personnage_actif.nom + ") ne possède pas l'action soigner", str(e))
									self.info_jeu = "Ce personnage (" + personnage_actif.nom + ") ne possède pas l'action soigner\n"
								else :
									raise e
								action_sucess = False
						else :	#Impossible en principe car peut se soigner soit même
							self.info_jeu = "aucun allié séléctionné pour soigner"
							action_sucess = False
				except AttributeError as e:
					if personnage_actif is None:		#aucun personnage n'est séléctionné pour attaquer
						messagebox.showinfo("Aucun personnage selectionné pour soigner", str(e))
						self.info_jeu = "Aucun personnage selectionné pour soigner\n"
					else :
						raise e

		#Si l'action est un succès, alors on passe au tour suivant :
		if (action_sucess) :
			self.jeu.tour += 1
			#met à jour les effets et morts des personnages adversaires
			self.info_jeu += self.jeu.joueurs[(self.jeu.tour)%2].update_personnages()
			#test si le jeu est fini
			if (len(self.jeu.joueurs[(self.jeu.tour)%2].personnages)==0):
				self.win()

	def win(self) :
		'''Cette fonction permet de mettre fin au jeu, au lieu de fermer la fenêtre elle désactive les éléments interactifs
		Elle ajoute également un bouton changeant la couleur du background continuellement et bougeant la fenêtre tel un screensaver'''
		# on met à jour le message à afficher
		self.info_jeu += "Le joueur " + str((self.jeu.tour)%2+1) + " n'a plus de personnages\nLE JEU EST FINI, bravo au joueur " + str((self.jeu.tour+1)%2+1) + "\n"
		messagebox.showinfo("WIN", "Le joueur " + str((self.jeu.tour)%2+1) + " n'a plus de personnages\nLE JEU EST FINI, bravo au joueur " + str((self.jeu.tour+1)%2+1))

		# on enleve la possiblité au joueur d'intéragir avec les boutons/listes
		self.attaquer_button_widget.config(state="disabled")
		self.soigner_button_widget.config(state="disabled")
		self.ajouter_personnage_J1_button_widget.config(state="disabled")
		self.ajouter_personnage_J2_button_widget.config(state="disabled")
		self.passer_tour_button_widget.config(state="disabled")
		self.joueur_1_personnages_listbox_widget.unbind("<ButtonPress-1>")
		self.joueur_2_personnages_listbox_widget.unbind("<ButtonPress-1>")

		# Bouton secret : active/désactive le mode dvd screensaver ainsi que rainbow background (où la fenêtre rebondit sur les bords et change de couleur continuellement)
		self.dvd_screensaver_secret_button = tk.Button(self, 
						 text="Activer/Desactiver le mode DVD screensaver et Rainbow\n(note : le bouton escape risque de ne plus\n fonctionner pour fermer la fenêtre\ntant que vous n'avez pas reclické sur ce bouton\nLe jeu est fini vous pouvez fermer cette fenêtre\nune fois que le fun que ce bouton amène ce termine)", 
						 highlightbackground=bg_color, activeforeground = "red", foreground="black", 
						 command=lambda: [
							 setattr(self, 'secret_rainbow_bg_bool', 
							 not self.secret_rainbow_bg_bool),
							 setattr(self, 'secret_bouncing_dvd_animation_bool', 
							 not self.secret_bouncing_dvd_animation_bool), 
							 self.enlarge_window(duration=200, enlarge_amount=(-100, -100) if self.secret_bouncing_dvd_animation_bool else (100, 100)), 
							 self.color_loop(),
							 self.bouncing_dvd_animation()
							 ]
						 )
		self.dvd_screensaver_secret_button.grid(column=0, row=0, columnspan=4, rowspan=3, padx=2)


	def activate_secret_options(self):
		'''Cette fonction permet d'utiliser des fonctionnalitées secrettes :
		- activer/desactiver le mode dvd screensaver pour faire rebondir la fenêtre
		- activer le mode rainbow background
		- faire des dégats ou soigner tous les personnages d'un joueurs
		Pour activer ces commandes secrètes il faut que l'infobox contiene une des écritures possibles des codes secrets
		Puis il faut passer le tour pour valider
		ATTENTION : utiliser ces codes secrets peuvent amener des erreurs non prises en charges'''
		# on récupère le contenu de l'info text box (on enlève le character final)
		input = self.info_jeu_text_widget.get("1.0",'end-1c')
		#liste des codes secrets :
		rainbow_secret_codes = ["Rainbow", "rainbow", "Rainbow\n", "rainbow\n"]
		dvd_secret_codes = ["Dvd", "dvd", "Dvd\n", "dvd\n", "DVD", "DVD\n"]
		damage_all_J1_secret_codes = ["DJ1A", "dj1a", "DJ1A\n", "dj1a\n"]	#DJ1A = Damage Joueur 1 All
		damage_all_J2_secret_codes = ["DJ2A", "dj2a", "DJ2A\n", "dj2a\n"]
		heal_all_J1_secret_codes = ["HJ1A", "hj1a", "HJ1A\n", "hj1a\n"]		#HJ1A = Heal Joueur 1 All
		heal_all_J2_secret_codes = ["HJ2A", "hj2a", "HJ2A\n", "hj2a\n"]

		#test des codes secrets
		if str(input) in rainbow_secret_codes :
			self.secret_rainbow_bg_bool = not self.secret_rainbow_bg_bool
			self.color_loop()
		if str(input) in dvd_secret_codes :
			self.secret_bouncing_dvd_animation_bool = not self.secret_bouncing_dvd_animation_bool
			self.bouncing_dvd_animation()
		if str(input) in damage_all_J1_secret_codes :
			for p in self.jeu.joueurs[0].personnages :
				p.pv -= 10
		if str(input) in damage_all_J2_secret_codes :
			for p in self.jeu.joueurs[1].personnages :
				p.pv -= 10
		if str(input) in heal_all_J1_secret_codes :
			for p in self.jeu.joueurs[0].personnages :
				p.pv += 10
		if str(input) in heal_all_J2_secret_codes :
			for p in self.jeu.joueurs[1].personnages :
				p.pv += 10


	def creer_personnage(self, joueur):
		'''Cette fonction crée un nouveau personnage pour le joueur dont le numéro est en paramètre (0 pour le J1 et 1 pour le J2)
		La fonction crée une nouvelle fenêtre pour séléctionner la classe et entrer le nom, ne rien mettre permet de choisir aléatoirement'''
		# on crée d'une nouvelle fenêtre de dialogue
		dialog_window = tk.Toplevel(self)
#		dialog_window.transient(self)
		width = 220
		height = 290
		dialog_window.geometry(f"{width}x{height}+{(self.winfo_screenwidth() - width) // 2}+{(self.winfo_screenheight() - height) // 2}")

		label = tk.Label(dialog_window, text="creation d'un nouveau personnage")
		label.pack(side=tk.TOP, padx=5, pady=5)

		# on crée une zone texte où l'utilisateur peut rentrer le nom du personnage
		nom_box = tk.Entry(dialog_window)
		nom_box.pack(side=tk.TOP, padx=5, pady=5)

		# on crée une listbox avec les classes
		liste_classes = ["Barbare", "Archer", "Assassin", "Mage", "MaitreDesPoisons", "Pretre", "Druide", "Medecin", "Gardien", "Templier", "Chevalier"]
		listbox = tk.Listbox(dialog_window, foreground=default_text_color)
		for classe in liste_classes:
			listbox.insert(tk.END, classe)
		listbox.pack(side=tk.TOP, padx=5, pady=5)

		# on crée la fonction du bouton confirmer
		def confirm():
			self.perso_custom_nom = nom_box.get()
			self.perso_custom_classe = listbox.curselection()
			if self.perso_custom_classe:
				self.perso_custom_classe = listbox.get(self.perso_custom_classe[0])
			else:	#aucune séléction : classe choisie aléatoirement
				self.perso_custom_classe = None
			dialog_window.destroy()  # on ferme la fenêtre
		
		# on crée le bouton confirmer
		button = tk.Button(dialog_window, text="confirmer", foreground="black", command=confirm)
		button.pack(side=tk.BOTTOM, padx=5, pady=5)

		# on attend que l'utilisateur confirme
		self.wait_window(dialog_window)

		# on crée le nouveau personnage
		self.jeu.creer_personnage(self.jeu.joueurs[joueur], self.perso_custom_nom, self.perso_custom_classe)


	def stop(self, esc):
		"""Quitte l'application."""
		self.quit()


	def bouncing_dvd_animation(self):
		'''Cette fonction permet de faire la fenêtre se déplacer à la facon d'un screensaver,
		c'est possible de l'activer/désactiver lorsque le jeu est fini, ou si on entre le message "DVD" dans l'infobox et qu'on passe son tour'''
		if (move_and_resize_window_with_actions_bool) :
			x_direction = random.choice([-1, 1])
			y_direction = random.choice([-1, 1])
			x_speed = 5
			y_speed = 5
			width = self.winfo_width() 
			height = self.winfo_height()
			screen_width = self.winfo_screenwidth()
			screen_height = self.winfo_screenheight()

			while self.secret_bouncing_dvd_animation_bool :
				# on obtient la position actuelle
				current_x, current_y = self.winfo_x(), self.winfo_y()

				# on calcule la position suivante
				new_x = current_x + x_speed * x_direction
				new_y = current_y + y_speed * y_direction

				# on vérifie les collisions avec les bords, note : on laisse un peu de marge car les fenêtres ne peuvent pas aller sur le bandeau supérieur sur mac 
				if new_x <= 0:
					new_x = 5
					x_direction = 1
				elif new_x + width >= screen_width:
					new_x = screen_width - width - 5
					x_direction = -1
				if new_y <= 25:
					new_y = 25
					y_direction = 1
				elif new_y + height >= screen_height - 25:
					new_y = screen_height - height - 25
					y_direction = -1

				# on déplace la fenêtre
				self.move_resize_window(final_position=(new_x - current_x, new_y - current_y), duration=30, step_length=10)


	def color_loop(self):
		'''Cette fonction permet de changer constament la couleur du background de la fenêtre,
		c'est possible de l'activer/désactiver lorsque le jeu est fini, ou si on entre le message "rainbow" dans l'infobox et qu'on passe son tour'''
		if(self.secret_rainbow_bg_bool):
			colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
			self.configure(bg=colors[self.color_index])
			self.color_index = (self.color_index + 1) % len(colors)
			self.after(1000, self.color_loop)
bg_color = "#333333"

import tkinter as tk
import math
import random

class Application(tk.Tk):

	def __init__(self, jeu):
		tk.Tk.__init__(self)
		self.title("app_name")
		self.height = 800
		self.width = 600
		self.configure(bg = bg_color)
		self.geometry(str(self.height)+"x"+str(self.width))
		self.resizable(1, 1)		#allow resizing the window
		self.minsize(575,215)
		self.jeu = jeu

		#TODO : porbablement enlever :
		self.joueur_1_noms_personnages = [p.nom for p in jeu.joueurs[0].personnages]	#TODO: probablement a changer plus tard pour utiliser que tk.Variables
		self.joueur_2_noms_personnages = [p.nom for p in jeu.joueurs[1].personnages]
		#on met les noms dans une tk.Variable pour les afficher dans une listebox
		self.joueur_1_noms_personnages_var = tk.Variable(value=self.joueur_1_noms_personnages)
		self.joueur_2_noms_personnages_var = tk.Variable(value=self.joueur_2_noms_personnages)

		print(self.joueur_1_noms_personnages[0])
		print(str(self.joueur_1_noms_personnages[0]))
		print(self.jeu.joueurs[0].personnages[0].all_info())
		print(str(self.jeu.joueurs[0].personnages[0].all_info()))

		self.info_personnage_joueur_1 = "hello world 1hello world 1hello world 1hello world 1hello world 1\nhello world 1hello world 1hello world 1hello world 1\nhello world 1"
		self.info_personnage_joueur_2 = "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n"

		#liste des personnages selectionnés par le joueur
		self.selected_list_joueur_1 = []
		self.selected_list_joueur_2 = []

		print("\033[94m hello \033[0m")

		self.creer_widgets()

		self.bind("<Escape>", self.stop)
	#	self.bind("<Configure>", self.resize)	#Doesn't work currently


	


	def move_resize_window(self, final_position=(0, 0), move_type="none", final_size=(0, 0), resize_type="none", duration=1000, step_length=10):
		'''Cette fonction permet de déplacer et redimensionner la fenêtre.
		Il y a 3 types d'accélérations : ease_in (commence lent et accélère avant de s'arréter), ease_out (commence rapide et ralentit à la fin), ease_in_out (combinaison des deux).
		Plus step_length est faible, plus il y aura d'étapes dans le mouvement, à calibrer en relation à duration (la durée)
		La durée est censée être en milisecondes mais ne fonctionne pas correctement et dure plus longtempt
		'''
		# DISCLAIMER : fonction crée en partie grâce à ChatGPT

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
		# DISCLAIMER : fonction crée en partie grâce à ChatGPT
		if easing_type == "ease_in":
			return lambda t: t * t
		elif easing_type == "ease_out":
			return lambda t: 1 - (1 - t) * (1 - t)
		elif easing_type == "ease_in_out":
			return lambda t: (3 - 2 * t) * t * t
		else:
			return lambda t: t

	def move_window_in_a_circle(self, duration=50, radius=15, steps=20):
		'''fonction bougeant la fenêtre en forme de cercle, la durée ne fonctionne pas correctement, et des valeurs extrèmes pour les arguments peuvent avoir des conséquences imprévues'''
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
		'''Cette fonction permet de mettre à jour le contenu de la textbox avec les infos sur le dernier personnage séléctionné'''
		#On met à jour les 2 string contenant le texte à afficher des 2 textbox
		if (len(self.selected_list_joueur_1)) :
			self.info_personnage_joueur_1 = self.get_personnage_from_name(self.selected_list_joueur_1[-1]).all_info()
		else :
			self.info_personnage_joueur_1 = "Aucun personnage selectionné\n" + str(len(self.jeu.joueurs[0].personnages)) + " personnages restants.\n"
		if (len(self.selected_list_joueur_2)) :
			self.info_personnage_joueur_2 = self.get_personnage_from_name(self.selected_list_joueur_2[-1]).all_info()
		else :
			self.info_personnage_joueur_2 = "Aucun personnage selectionné\n" + str(len(self.jeu.joueurs[1].personnages)) + " personnages restants.\n"

		#on supprime le contenu des textbox pour insérer le nouveau texte
		self.info_joueur_1_text_widget.delete('1.0', 'end')
		self.info_joueur_1_text_widget.insert('end', self.info_personnage_joueur_1)

		self.info_joueur_2_text_widget.delete('1.0', 'end')
		self.info_joueur_2_text_widget.insert('end', self.info_personnage_joueur_2)			


	def update_listbox_content(self):
		'''Cette fonction met à jour le texte à l'intérieur des listbox avec les personnages des joueurs'''
		#2 methodes pour remplacer le texte de la liste :

		# on supprime le contenu des listbox pour insérer les nouveaux textes
		self.joueur_1_personnages_listbox_widget.delete(0, tk.END)
		self.joueur_1_personnages_listbox_widget.insert(0, *[string for string in self.joueur_1_noms_personnages])

		self.joueur_2_personnages_listbox_widget.delete(0, tk.END)
		for string in self.joueur_2_noms_personnages:
			self.joueur_2_personnages_listbox_widget.insert("end", string)


	def on_select(self, event):
		'''Cette fonction permet de trouver le dernier élément séléctionné du widget correspondant à l'event et de l'ajoute/enlever de la liste des personnages séléctionnés'''
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

		for i in range(self.joueur_1_personnages_listbox_widget.size()):
			element1 = self.joueur_1_personnages_listbox_widget.get(i)
			if element1 in self.selected_list_joueur_1:
				self.selected_list_joueur_1.remove(element1)
#				self.joueur_1_personnages_listbox_widget.itemconfig(i, bg="white", fg="black")
		for i in range(self.joueur_2_personnages_listbox_widget.size()):
			element2 = self.joueur_2_personnages_listbox_widget.get(i)
			if element2 in self.selected_list_joueur_2:
				self.selected_list_joueur_2.remove(element2)
#				self.joueur_2_personnages_listbox_widget.itemconfig(i, bg="white", fg="black")


	def creer_widgets(self):
		'''Cette fonction permet d'intialiser les widgets'''

		self.columnconfigure(0, minsize=200, weight=3)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, minsize=200, weight=3)
		self.rowconfigure(0, minsize=65, weight=1)
		self.rowconfigure(1, minsize=150, weight=1)

		#Info box du personnage sélectionné en dernier du joueur 1
		self.info_joueur_1_text_widget=tk.Text(self, height=40, bg="#222222")
		self.info_joueur_1_text_widget.insert('insert',self.info_personnage_joueur_1)
		self.info_joueur_1_text_widget.grid(column=0, row=1, columnspan = 2, sticky=tk.NW, padx=3, pady=3)

		#Info box du personnage sélectionné en dernier du joueur 2
		self.info_joueur_2_text_widget=tk.Text(self, height=40, bg="#222222")
		self.info_joueur_2_text_widget.insert('insert',self.info_personnage_joueur_2)
		self.info_joueur_2_text_widget.grid(column=2, row=1, columnspan = 2, sticky=tk.NE, padx=3, pady=3)

		# Liste des personnages du joueur 1
		self.joueur_1_personnages_listbox_widget = tk.Listbox(self, 
			height=100, 
			listvariable=self.joueur_1_noms_personnages_var, 
			bg="#222", 
			selectbackground="blue", 
			selectmode=tk.MULTIPLE, 	#permet de selectionner plusieurs élements
			exportselection=False		#empeche d'autres listbox d'enlever les selections de cette listbox
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
			exportselection=False		#empeche d'autres listbox d'enlever les selections de cette listbox
			)
		self.joueur_2_personnages_listbox_widget.grid(column=3, row=0, sticky=tk.EW, padx=5, pady=5, ipadx=5, ipady=5)
		self.joueur_2_personnages_listbox_widget.bind("<ButtonPress-1>", self.on_select)

		# Bouton attaquer
		self.attaquer_button_widget = tk.Button(self, text="Attaquer", highlightbackground=bg_color, activeforeground = "red", command=lambda: [self.update_listbox_content(), self.deselect_all(), self.update_info_box_content(), self.change_bg_color("#F00", bg_color, 500)])
		self.attaquer_button_widget.grid(column=1, row=0, sticky=tk.EW, padx=2)

		# Bouton soigner
		self.soigner_button_widget = tk.Button(self, text="Soigner", highlightbackground=bg_color, activeforeground = "yellow", command=lambda: [self.update_listbox_content(), self.deselect_all(), self.update_info_box_content(), self.change_bg_color("#FF0", bg_color, 500)])
		self.soigner_button_widget.grid(column=2, row=0, sticky=tk.EW, padx=2)

		# Bouton de Tests
		self.change_color_button_widget = tk.Button(self, text="tests", command= lambda: [self.change_bg_color("#FF0", bg_color, 500), self.deselect_all(), self.move_window_in_a_circle(), self.enlarge_window(enlarge_amount=(10,10)),self.move_resize_window(final_position=(200,0), move_type="ease_in_out", final_size=(-10,-10), resize_type="ease_in_out", duration=2000)])
		self.change_color_button_widget.grid(column=1, row=1, sticky=tk.EW, padx=2)


	def change_bg_color(widget, start_color, end_color, duration):
		'''Cette fonction permet de changer la couleur de fond de la fenêtre'''
		steps = 30					#nombre d'étapes du changement de couleur
		delay = duration // steps	#délai entre les étapes
		r1, g1, b1 = widget.winfo_rgb(start_color)
		r2, g2, b2 = widget.winfo_rgb(end_color)
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


	def stop(self, esc):
		"""Quitte l'application."""
		self.quit()





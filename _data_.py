#coding: utf-8

'''
Tables des correspondances

	Le rang 0 correspond à la position de l'information dans la trame MAESTRO
	Le rang 1 correspond a l'intitulé publié sur le broker
	Le rang 2 (optionnel) permet de remplacer le code de la trame par une information texte correspondante

'''
RecuperoInfo=[
	[1,"Etat du poêle",[
						[0, "Eteint"],
						[2, "Contrôle du poêle froid / chaud"],
						[3, "Load Froid"],
						[4, "Start 1 froid"],
						[5, "Start 2 froid"],
						[10, "Stabilisation"],
						[11, "Puissance 1"],
						[12, "Puissance 2"],
						[13, "Puissance 3"],
						[14, "Puissance 4"],
						[15, "Puissance 5"],
						[30, "Mode diagnostique"],
						[31, "Marche"],
						[40, "Extinction"],
						[41, "Refroidissement en cours"],
						[42, "Nettoyage basse.p"],
						[46, "Standby"],
						[50, "Erreur A01 - Allumage raté"],
						[51, "Erreur A02 - Pas de flamme"],
						[52, "Erreur A03 - Surchauffe du réservoir"],
						[53, "Erreur A04 - Température des fumées trop haute"],
						[54, "Erreur A05 - Obstruction conduit - Vent"],
						[55, "Erreur A06 - Mauvais tirage"],
						]],
	[2,"Etat du ventilateur d'ambiance",[
										[0, "Désactivé"],
										[1, "Niveau 1"],
										[2, "Niveau 2"],
										[3, "Niveau 3"],
										[4, "Niveau 4"],
										[5, "Niveau 5"],
										[6, "Automatique"],
										]],
	[5,"Température des fumées"],
	[6,"Température ambiante"],
	[10,"Etat de la bougie"],
	[11,"ACTIVE - Set"],
	[12,"RPM - Ventilateur fummées"],
	[13,"RPM - Vis sans fin - SET"],
	[14,"RPM - Vis sans fin - LIVE"],
	[20,"Etat du mode Active"],  #0: Désactivé, 1: Activé
	[21,"ACTIVE - Live"],
	[22,"Mode de régulation",[
								[0, "Manuelle"],
								[1, "Dynamique"],
								]],
	[23,"Mode ECO"],
	[25,"Mode Chronotermostato"],
	[26,"TEMP - Consigne"],
	[28,"TEMP - Carte mère"],
	[29,"Puissance Active",[
							[11, "Puissance 1"],
							[12, "Puissance 2"],
							[13, "Puissance 3"],
							[14, "Puissance 4"],
							[15, "Puissance 5"],
							]],
	[32,"Heure du poêle (0-23)"],
	[33,"Minutes du poêle (0-29)"],
	[34,"Jour du poêle (1-31)"],
	[35,"Mois du poêle (1-12)"],
	[36,"Année du poêle"],
	[37,"Heures de fonctionnement total (s)"],
	[38,"Heures de fonctionnement en puissance 1 (s)"],
	[39,"Heures de fonctionnement en puissance 2 (s)"],
	[40,"Heures de fonctionnement en puissance 3 (s)"],
	[41,"Heures de fonctionnement en puissance 4 (s)"],
	[42,"Heures de fonctionnement en puissance 5 (s)"],
	[43,"Heures avant entretien"],
	[44,"Minutes avant extinction"],
	[45,"Nombre d'allumages"],
	[49,"Etat effets sonores"],
	[51,"Mode",[
				[0, "Hiver"],
				[1, "Eté"],
				]],
	]
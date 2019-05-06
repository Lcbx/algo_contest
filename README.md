This was done in a contest in algorithm design held for the INF8775 (analysis of algorithms) course of Polytechnique Montreal      



Comme le veut la tradition, je vous présente les trois meilleurs algorithmes pour le concours du TP3. Les exemplaires choisis sont les suivants :  
- LEGO_50_50_1000  
- LEGO_50_100_2000  
- LEGO_100_100_2000    


#1. Antoine Daigneault-Demers et James Lok  
Scores : 1294, 698, 3119  
Cet algorithme trouve une solution de base avec un algorithme glouton, puis utilise un mélange de recherche par voisinage variable et de recherche tabou afin d’améliorer la solution initiale.    


#2. Kim Piché et Abderahmane Bouziane  
Scores : 1293, 719, 3225  
Algorithme génétique classique prenant en compte plusieurs paramètres.    


#3. Grégoire Dervaux et Marc Lanovaz  
Scores : 1371, 939, 3314  
Un algorithme glouton est utilisé pour trouver une solution initiale, qui est ensuite améliorée avec une heuristique d'amélioration locale. L'algorithme est parallélisé.      


#Moi (original)  
Scores : 2147, 2197, 6749  
Un algorithme d'approximation (algorithme NNLS de Lawson-Hanson) est utilisé puis affiné par recherche par voisinage aléatoire.    

#Moi (modifie)  
Scores : 1364, 1050, 3734  
Un algorithme d'approximation (algorithme NNLS de Lawson-Hanson) est utilisé puis affiné par recherche par voisinage aléatoire avec tabou et temperature.  


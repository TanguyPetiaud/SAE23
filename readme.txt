Pour utiliser l'application, simplement lancer main.py à travers un interpreteur python.
Il faut s'assurer que la base de données MySQL est lancée avant d'executer une commande.
Il sera nécessaire lors de la première exécution du programme d'utiliser la commande "Restore Database" (R).

L'application permet de consulter le contenu de la base de données en mode CLI et à travers le site web.
Il est également possible de modifier le contenu de la base en mode CLI seulement.

La fonctionalité de gestion des parties jouées qui était originalement prévue n'a pas été réalisée par manque de temps.
Les tables correspondant (game et gameplayer) ont été supprimées de la base de données.

L'archive contient l'arborescence suivante:
    - DB backup: les fichiers CSV contenant le jeu d'essai
    - DB sources: le fichier .sql contenant le dump de la base de données
    - sources: toutes les ressources du site web
        - autres: la police d'écriture utilisée à travers le site
        - css: les fichiers CSS de toutes les pages
        - medias/images: les images utilisées à travers le site
        - index.html: le template du site
    - dbUtils.py: les fonctions CRUD sur la base de données et d'interface CLI
    - main.py: la boucle d'execution principale et les fonctions liées au site web
    - readme.txt: le présent fichier texte
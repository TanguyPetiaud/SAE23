Pour faire fonctionner le programme, il suffit de lancer main.py dans un interpreteur python.

Quelques remarques:
    - Il est impératif de lancer le serveur avant le programme.
    - Si le nom d'utilisateur / mot de passe ne sont pas les bons, il est possible de les changer en modifiant très simplement main.py. Des variables (_dbUser, _dbPass et _dbName) permettent de spécifier le login, mot de passe et nom de la base de données à utiliser.
    - Attention dans le choix du nom de la base de données. Si une base avec le même nom existe déjà localement, elle sera supprimée sans remors de la part du programme.
    - La partie concernant la gestion des parties entre utilisateurs n'a pas encore été implementée.
    - Il faut faire attention si on choisit d'utiliser des filtres dans l'affichage des unités. En effet, ces filtres sont très sensibles à la casse.


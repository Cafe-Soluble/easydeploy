# EasyDeploy
Script de déploiement automatique de mes web apps Flask. 
## Étapes d'utilisation

1. Cloner le dépôt actuel dans le dossier utilisateur.
2. Démarrer le script : `python3 easydeploy.py`.
3. Remplissez les informations demandées par le script.
4. Attendez la fin de la procédure.

## Problèmes courants

Erreurs fréquemment rencontrées et comment les éviter :

- **Fichier `requirements.txt` vide ou inexistant** : S'assurer que le fichier `requirements.txt` existe dans le répertoire projet.
- **Nom de l'application avec l'extension `.py`** : Lors de la spécification du nom de de l'application, ne pas inclure l'extension `.py`. Par exemple, utiliser `main` au lieu de `main.py`.
- **Conflit de dossier pour l'application** : Si l'application est dans un sous-dossier portant le même nom (par exemple `MON_APP/MON_APP`), cela peut poser des problèmes, notamment avec le dossier `static`.

## Fonctionnalités à implanter

Implémentations futures :

- **Vérification de disponibilité du port** : Ajouter une vérification pour s'assurer que le port nécessaire n'est pas déjà utilisé.
- **Validation du fichier `requirements.txt`** : S'assurer que le fichier `requirements.txt` est présent et correctement formaté avant de procéder au déploiement.
- **Gestion des dossiers imbriqués** : Améliorer la gestion des applications situées dans des sous-dossiers pour éviter les bugs liés aux chemins d'accès.

---

import subprocess
import os
import time

test = False


def input_user(question, exemple): # cette fonction permet un input avec une correction
    while True:
        value=input(f">>> {question} (ex: {exemple}) \n")
        print(f"Voici votre entrée : {value}")
        confirmer_value=input("Voulez-vous valider ? Y/n ")
        if confirmer_value.lower() == "y":
            return value


script_name="EasyDeploy"
version="0.1"
print("Ce script facilite le déploiement en production d'une web app Python en utilisant Flask/Nginx/Gunicorn/Supervisorctl")
continuer=input("Voulez-vous continuer ? Y/n ")
if continuer.lower() != "y":
    print(f"Exiting {script_name} v{version}")
else:
    commandes = ["","","","",""]


    # # on change le répertoire de travail du processus principal dans le bon dossier
    
    if test == True:
        user= "jc"
        git_projet= "genfact_check"
        git_url="https://github.com/Cafe-Soluble/genfact_check.git"
        password_user = ""
        server_name="prout.jucidful.fr"
        port="3004"
        app_name = "prout"

    else:
        user=input_user("Utilisateur Linux qui deploiera la web app", "webmaster")
        git_url=input_user("Adresse git à cloner", "git@github.com:Cafe-Soluble/NEWPROJECT.git")
        git_projet=input_user("Nom du projet Github", "plexhelper")
        password_user=input_user(f"Entrez votre mot de passe pour {user}", "password123")
        server_name=input_user("Nom du serveur ou adresse ip", "prout.jucidulf.fr")
        port=input_user("Port","3004")
        app_name = input_user("Nom de l'application (venant de application.py)", "main")


    #Copie du repository de la web app
    os.chdir(f"/home/{user}")
    subprocess.check_output(f'git clone {git_url}', shell=True, text=True)


    #Création d'un environnement de travail
    time.sleep(1)
    os.chdir(f"/home/{user}/{git_projet}")

    commande = f"echo {password_user} | sudo -S chmod u+x /home/{user}/{git_projet}/startEnv.sh"
    subprocess.run(commande, shell=True, input=f"{password_user}\n", text=True)
    subprocess.call(f"/home/{user}/{git_projet}/startEnv.sh")

    #Création du fichier de config Nginx
    contenu = f"""server {{
    listen 80;
    server_name {server_name};

    location /static {{
        alias /home/{user}/{git_projet}/static;
    }}
    location / {{
        proxy_pass http://localhost:{port};
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }}
    }}"""

    with open(f"{git_projet}", "w") as fichier:
        fichier.write(contenu)
    print(f"Fichier '{git_projet}' créé avec succès.")

    #Déplacement du fichier de config dans /etc/supervisor/conf.d/
    print("Copie du fichier à /etc/supervisor/conf.d/")
    commande = f"echo {password_user} | sudo -S mv {git_projet} /etc/nginx/sites-enabled/"
    subprocess.run(commande, shell=True, input=f"{password_user}\n", text=True)
    
    #Création du fichier de configuration supervirsoctl
    contenu = f"""[program:{git_projet}]
directory=/home/{user}/{git_projet}
command=/home/{user}/{git_projet}/env/bin/gunicorn -w 3 -b 0.0.0.0:{port} {app_name}:app
user={user}
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/{git_projet}/{git_projet}.err.log
stdout_logfile=/var/log/{git_projet}/{git_projet}.out.log"""

    with open(f"{git_projet}.conf", "w") as fichier:
        fichier.write(contenu)
    print(f"Fichier '{git_projet}.conf' créé avec succès.")

    #Déplacement du fichier .conf dans /etc/supervisor/conf.d/
    print("Copie du fichier à /etc/supervisor/conf.d/")
    commande = f"echo {password_user} | sudo -S mv {git_projet}.conf /etc/supervisor/conf.d/"
    subprocess.run(commande, shell=True, input=f"{password_user}\n", text=True)
    
    #Création des logs
    print('Création des fichiers de logs ...')
    commande = f"echo {password_user} | sudo -S mkdir -p /var/log/{git_projet}"
    subprocess.run(commande, shell=True, input=f"{password_user}\n", text=True)
    
    commande = f"echo {password_user} | sudo -S touch /var/log/{git_projet}/{git_projet}.err.log"
    subprocess.run(commande, shell=True, input=f"{password_user}\n", text=True)

    commande = f"echo {password_user} | sudo -S touch /var/log/{git_projet}/{git_projet}.out.log"
    subprocess.run(commande, shell=True, input=f"{password_user}\n", text=True)
    print("Done !\n\n")

    #Dernières actions manuelles à effectuer
    print("> Veuillez relancer les services Nginx et Supervisorctls avec :")
    print("sudo systemctl restart nginx")
    print("sudo supervisorctl reload")
    print("> Puis ajouter les certificats : ")
    print("sudo certbot --nginx")

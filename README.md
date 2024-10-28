# League of Legends Game Tracker 📈

Ce projet est un tracker de parties de League of Legends qui envoie des notifications personnalisées sur Discord, permettant de suivre et de chambrer vos amis avec des statistiques détaillées et un aspect compétitif.

## Fonctionnalités 🏆
- Suivi des parties de plusieurs joueurs en mode ARAM.
- Notifications Discord avec détails des performances, y compris :
  - Statut de victoire ou défaite 🎉 / 😢
  - Dégâts infligés, position du joueur dans l’équipe 👑 (top) ou 💀 (dernier).
  - Pourcentage de dégâts par rapport à l’équipe.
  - Kills/Deaths/Assists (KDA) et champion utilisé avec son icône.
- Notifications basées sur un fichier CSV contenant les informations des joueurs à suivre.

## Prérequis ⚙️
- Python 3.8 ou supérieur
- Un compte Riot Games Developer avec une API Key
- Un serveur Discord avec un ou plusieurs Webhooks configurés pour recevoir les notifications.

## Installation 💻

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/tonutilisateur/tonprojet.git
   cd tonprojet```

2. **Créer et activer un environnement virtuel** :

 ```bash
python3 -m venv venv
source venv/bin/activate    # Sur macOS/Linux
venv\Scripts\activate       # Sur Windows
```
3. **Installer les dépendances** :

```bash
pip install -r requirements.txt
```

4. **Configurer les variable dans un fichier .env** : 

Créez un fichier .env à la racine du projet et ajoutez-y votre clé API Riot Games :
```bash
RIOT_API_KEY=VotreCleAPI
```
5. **Mettre en place le fichier CSV des joueurs à suivre : Créez un fichier players.csv au format suivant :**
```csv
GAME_NAME,TAG_LINE,DISCORD_WEBHOOK
NomDuJoueur1,1234,https://discord.com/api/webhooks/...
NomDuJoueur2,EUW,https://discord.com/api/webhooks/...
```

**Structure du projet 📂**

- script_csv.py : Le script principal de suivi et d'envoi de messages Discord.
- players.csv : Fichier listant les joueurs à suivre (nom de l'invocateur, tag, lien du webhook Discord).
- .env : Fichier contenant les informations sensibles, non inclus dans le dépôt pour la sécurité.


**🤖🤖 Codé avec l'aide de  ChatGPT 🤖🤖**

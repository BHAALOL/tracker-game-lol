import os
from dotenv import load_dotenv
import requests
import time
import urllib.parse
import csv

load_dotenv() 

API_KEY = os.getenv('API_KEY')
BASE_URL_ACCOUNT = 'https://europe.api.riotgames.com'

# Fonction pour récupérer le PUUID du compte via le gameName et le tagLine
def get_summoner_puuid(game_name, tag_line):
    game_name_encoded = urllib.parse.quote(game_name)
    tag_line_encoded = urllib.parse.quote(tag_line)

    url = f"{BASE_URL_ACCOUNT}/riot/account/v1/accounts/by-riot-id/{game_name_encoded}/{tag_line_encoded}"
    headers = {"X-Riot-Token": API_KEY}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('puuid')

# Fonction pour obtenir les parties récentes à partir du PUUID
def get_recent_matches(puuid):
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1'
    headers = {'X-Riot-Token': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la récupération des parties : {response.status_code}, {response.text}")
        return None

# Fonction pour obtenir les détails d'une partie
def get_match_details(match_id):
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}'
    headers = {'X-Riot-Token': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la récupération des détails de la partie : {response.status_code}, {response.text}")
        return None

# Fonction pour envoyer un message sur Discord
def send_discord_message(webhook_url, content, embed=None):
    data = {"content": content}
    if embed:
        data['embeds'] = [embed]
    requests.post(webhook_url, json=data)

# Fonction pour obtenir le nom du champion et son logo
def get_champion_info(champion_id):
    url = 'https://ddragon.leagueoflegends.com/cdn/12.18.1/data/fr_FR/champion.json'
    response = requests.get(url)
    if response.status_code == 200:
        champions_data = response.json()['data']
        for champion in champions_data.values():
            if champion['key'] == str(champion_id):
                logo_url = f"https://ddragon.leagueoflegends.com/cdn/12.18.1/img/champion/{champion['id']}.png"
                return champion['name'], logo_url
    return "Unknown Champion", ""

# Fonction pour obtenir les dégâts de l'équipe
def get_team_damage(match_details, player_team_id):
    return [
        participant['totalDamageDealtToChampions']
        for participant in match_details['info']['participants']
        if participant['teamId'] == player_team_id
    ]

# Fonction pour calculer le ratio des dégâts infligés par le joueur par rapport au total de l'équipe
def calculate_damage_ratio(player_damage, team_damage_total):
    damage_ratio = (player_damage / team_damage_total) * 100
    return f"{damage_ratio:.1f} %"

# Fonction principale pour le suivi
def track_players_from_csv(csv_file):
    players_data = []

    # Charger les informations des joueurs à partir du CSV
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            puuid = get_summoner_puuid(row['GAME_NAME'], row['TAG_LINE'])
            if puuid:
                players_data.append({
                    'GAME_NAME': row['GAME_NAME'],
                    'TAG_LINE': row['TAG_LINE'],
                    'DISCORD_WEBHOOK': row['DISCORD_WEBHOOK'],
                    'PUUID': puuid,
                    'last_match_id': None  # Initialiser l'ID de la dernière partie traitée
                })
            else:
                print(f"Erreur lors de la récupération du PUUID pour {row['GAME_NAME']}#{row['TAG_LINE']}")

    # Boucle de suivi
    while True:
        for player in players_data:
            matches = get_recent_matches(player['PUUID'])
            if matches:
                match_id = matches[0]

                # Vérifier si la partie n'a pas déjà été traitée
                if match_id != player['last_match_id']:
                    match_details = get_match_details(match_id)

                    # Analyser les détails de la partie
                    for participant in match_details['info']['participants']:
                        if participant['puuid'] == player['PUUID']:
                            win = participant['win']
                            damage_dealt = participant['totalDamageDealtToChampions']
                            champion_id = participant['championId']
                            kills = participant['kills']
                            deaths = participant['deaths']
                            assists = participant['assists']
                            team_id = participant['teamId']

                            # Récupérer les dégâts de l'équipe pour comparaison
                            team_damages = get_team_damage(match_details, team_id)

                            # Calcul du symbole de performance
                            damage_symbol = ''
                            if damage_dealt == max(team_damages):
                                damage_symbol = '👑'
                            elif damage_dealt == min(team_damages):
                                damage_symbol = '💀'

                            # Formater les dégâts avec séparateurs de milliers
                            damage_display = f"{damage_dealt:,}".replace(',', ' ')

                            # Informations sur le champion
                            champion_name, champion_logo = get_champion_info(champion_id)
                            kda = f"{kills}/{deaths}/{assists}"

                             # Déterminer l'équipe du joueur
                            player_team_id = participant['teamId']
        
                            # Calculer les dégâts totaux de l'équipe
                            team_damage_total = sum(p['totalDamageDealtToChampions'] for p in match_details['info']['participants'] if p['teamId'] == player_team_id)
        
                             # Calculer le ratio des dégâts
                            damage_ratio = calculate_damage_ratio(damage_dealt, team_damage_total)


                            team_damages = [p['totalDamageDealtToChampions'] for p in match_details['info']['participants'] if p['teamId'] == player_team_id]
                            max_damage = max(team_damages)
                            min_damage = min(team_damages)
                            
                            if damage_dealt == max_damage:
                                damage_symbol = "👑"
                            elif damage_dealt == min_damage:
                                damage_symbol = "💀"
                            else:
                                damage_symbol = ""

                             # Formatage des dégâts avec séparateur d'espaces pour les milliers
                            damage_dealt_formatted = f"{damage_dealt:,}".replace(",", " ")

                            # Message de victoire ou défaite
                            message = "✅✅✅WIN✅✅✅" if win else "❌💀❌LOOSE❌💀❌"
                            embed = {
                                "title": champion_name,
                                "description": f"KDA: {kda}\nDégâts infligés : {damage_dealt_formatted} {damage_symbol}\nRatio des dégâts : {damage_ratio}",
                                "thumbnail": {"url": champion_logo}
                            }

                            # Envoi du message sur Discord
                            send_discord_message(player['DISCORD_WEBHOOK'], message, embed)

                            # Mettre à jour l'ID de la dernière partie traitée
                            player['last_match_id'] = match_id
                            break
            else:
                print(f"Aucune partie trouvée ou réponse invalide pour {player['GAME_NAME']}#{player['TAG_LINE']}")

        time.sleep(60)  # Pause de vérification



if __name__ == "__main__":
    track_players_from_csv('players.csv')


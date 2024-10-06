# https://fixturedownload.com/results/la-liga-2018
import pandas as pd
import argparse
from collections import Counter

ROOT_PATH = "csv_files"
# Función para filtrar por equipo y obtener el resultado más repetido
def get_most_frequent_results(team_name, df):
    # Filtrar partidos como Home Team
    home_matches = df[df['Home Team'] == team_name]
    # Filtrar partidos como Away Team
    away_matches = df[df['Away Team'] == team_name]
    
    # Obtener los resultados más repetidos
    most_common_home = Counter(home_matches['Result']).most_common(1)
    most_common_away = Counter(away_matches['Result']).most_common(1)
    
    # Extraer el resultado más común o manejar si no hay datos
    home_result = most_common_home[0][0] if most_common_home else "No data"
    away_result = most_common_away[0][0] if most_common_away else "No data"
    
    return home_result, away_result

# Nueva función para filtrar partidos específicos entre dos equipos
def get_most_frequent_result_between_teams(home_team, away_team, df):
    # Filtrar partidos donde el equipo local y visitante coincidan
    specific_matches = df[(df['Home Team'] == home_team) & (df['Away Team'] == away_team)]
    
    # Contar la frecuencia de resultados
    most_common_result = Counter(specific_matches['Result']).most_common(1)
    
    # Extraer el resultado más común o manejar si no hay datos
    return most_common_result[0][0] if most_common_result else "No data"

# Función para el nuevo comando "complete" que combina todos los resultados
def complete_analysis(team_a, team_b, df):
    print(f"\nAnálisis completo para {team_a} y {team_b}:\n")

    print(f"Resultados en casa {team_a}:")
    matches_in_home = df[(df['Home Team'] == team_a)]
    print(f"  matches_in_home: {matches_in_home}")
    print(f"Resultados visitante {team_b}:")
    matches_in_visit = df[(df['Away Team'] == team_b)]
    print(f"  matches_in_visit: {matches_in_visit}")

    # 1. Resultados más repetidos como Home Team y Away Team para ambos equipos
    # print(f"Resultados más repetidos de {team_a}:")
    # home_result_a, away_result_a = get_most_frequent_results(team_a, df)
    # print(f"  Como Home Team: {home_result_a}")
    # print(f"  Como Away Team: {away_result_a}\n")
    
    # print(f"Resultados más repetidos de {team_b}:")
    # home_result_b, away_result_b = get_most_frequent_results(team_b, df)
    # print(f"  Como Home Team: {home_result_b}")
    # print(f"  Como Away Team: {away_result_b}\n")
    
    # 2. Resultados de enfrentamientos entre ambos equipos
    print(f"Resultados más repetidos entre {team_a} y {team_b}:")
    match_result_ab = get_most_frequent_result_between_teams(team_a, team_b, df)
    match_result_ba = get_most_frequent_result_between_teams(team_b, team_a, df)
    print(f"  {team_a} vs {team_b}: {match_result_ab}")
    print(f"  {team_b} vs {team_a}: {match_result_ba}\n")

# Función principal para procesar múltiples archivos
def process_files(file_path_list, args):
    for file_path in file_path_list:
        # Título del archivo que se está procesando
        print(f"\nProcesando archivo: {file_path}")
        
        # Cargar el archivo CSV
        df = pd.read_csv(f"csv_files/{file_path}")

        # Verificar qué comando se ha usado
        if args.command == 'team':
            # Obtener los resultados más repetidos para el equipo especificado
            home_result, away_result = get_most_frequent_results(args.team_name, df)
            print(f"Resultado más repetido como Home Team: {home_result}")
            print(f"Resultado más repetido como Away Team: {away_result}")
        
        elif args.command == 'match':
            # Obtener el resultado más repetido entre dos equipos
            result = get_most_frequent_result_between_teams(args.home, args.away, df)
            print(f"Resultado más repetido entre {args.home} y {args.away}: {result}")

        elif args.command == 'complete':
            # Hacer análisis completo de ambos equipos
            complete_analysis(args.teama, args.teamb, df)            

# Programa principal con argparse
if __name__ == "__main__":
    # Argument parser para recibir opciones desde la línea de comandos
    parser = argparse.ArgumentParser(description="Encuentra el resultado más repetido de un equipo como Home y Away team o entre dos equipos específicos.")
    
    # Subcomando para el análisis de un equipo
    subparsers = parser.add_subparsers(dest="command")
    
    # Subcomando para el análisis general por equipo
    team_parser = subparsers.add_parser('team')
    team_parser.add_argument("team_name", type=str, help="Nombre del equipo")
    
    # Subcomando para el análisis de partidos específicos entre dos equipos
    match_parser = subparsers.add_parser('match')
    match_parser.add_argument("--home", type=str, required=True, help="Nombre del equipo local")
    match_parser.add_argument("--away", type=str, required=True, help="Nombre del equipo visitante")
    
    # Nuevo subcomando para el análisis completo de dos equipos
    complete_parser = subparsers.add_parser('complete')
    complete_parser.add_argument("--teama", type=str, help="Nombre del equipo local")
    complete_parser.add_argument("--teamb", type=str, help="Nombre del equipo visitante")
        
    # Parsear los argumentos
    args = parser.parse_args()

    # Lista de archivos a procesar
    #file_path_list = ['bundesliga-2018-UTC.csv','bundesliga-2019-UTC.csv', 'bundesliga-2020-UTC.csv', 'bundesliga-2021-UTC.csv',  'bundesliga-2022-UTC.csv', 'bundesliga-2023-UTC.csv','bundesliga-2024-UTC.csv']
    file_path_list = ['la-liga-2018-UTC.csv','la-liga-2019-UTC.csv', 'la-liga-2020-UTC.csv', 'la-liga-2021-UTC.csv',  'la-liga-2022-UTC.csv', 'la-liga-2023-UTC.csv','la-liga-2024-UTC.csv']
    #file_path_list = ['europa-league-2019-UTC.csv', 'europa-league-2020-UTC.csv', 'europa-league-2021-UTC.csv',  'europa-league-2022-UTC.csv', 'europa-league-2023-UTC.csv','europa-league-2024-UTC.csv']
    #file_path_list = ['serie-a-2017-UTC.csv','serie-a-2018-UTC.csv','serie-a-2019-UTC.csv', 'serie-a-2020-UTC.csv', 'serie-a-2021-UTC.csv',  'serie-a-2022-UTC.csv', 'serie-a-2023-UTC.csv','serie-a-2024-UTC.csv']
    #file_path_list = ['ligue-1-2018-UTC.csv','ligue-1-2019-UTC.csv', 'ligue-1-2020-UTC.csv', 'ligue-1-2021-UTC.csv',  'ligue-1-2022-UTC.csv', 'ligue-1-2023-UTC.csv','ligue-1-2024-UTC.csv']
    #file_path_list = ['epl-2016-UTC.csv','epl-2017-UTC.csv','epl-2018-UTC.csv','epl-2019-UTC.csv', 'epl-2020-UTC.csv', 'epl-2021-UTC.csv',  'epl-2022-UTC.csv', 'epl-2023-UTC.csv','epl-2024-UTC.csv']
    #file_path_list = ['mls-2023-UTC.csv','mls-2024-UTC.csv']
    #file_path_list = ['primeira-liga-2020-UTC.csv','primeira-liga-2023-UTC.csv','primeira-liga-2024-UTC.csv']

    # Procesar cada archivo
    process_files(file_path_list, args)

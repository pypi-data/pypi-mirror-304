import unicodedata
from LionAPI.services.database import create_connection
import requests
import pandas as pd
from mysql.connector import Error

def get_shots(home_team, away_team, match_date):
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor(dictionary=True)
        try:
            # Query to get the event_id for the match
            query = """
                SELECT event_id
                FROM events
                WHERE home_team = %s AND away_team = %s AND event_date = %s;
            """
            cursor.execute(query, (home_team, away_team, match_date))
            result = cursor.fetchone()

            if result is None:
                print("No game found for the given parameters")
                return None
            
            event_id = result['event_id']

            # Fetch the shot data from the SofaScore API
            url = f"https://sofascore.com/api/v1/event/{event_id}/shotmap"
            response = requests.get(url)

            if response.status_code == 200:
                # Parse the JSON response and normalize it into a DataFrame
                shots = response.json()
                df = pd.json_normalize(shots['shotmap'])

                # Filter out shootout shots
                df = df[df['situation'] != 'shootout']

                # Define the selected columns
                selected_columns = [
                    'isHome', 'shotType', 'situation', 'bodyPart', 'goalMouthLocation',
                    'xg', 'id', 'time', 'addedTime', 'timeSeconds', 'reversedPeriodTime',
                    'reversedPeriodTimeSeconds', 'incidentType', 'player.name', 'player.position', 
                    'player.jerseyNumber', 'player.id', 'playerCoordinates.x', 'playerCoordinates.y', 
                    'playerCoordinates.z', 'goalMouthCoordinates.x', 'goalMouthCoordinates.y', 
                    'goalMouthCoordinates.z', 'blockCoordinates.x', 'blockCoordinates.y', 'blockCoordinates.z', 
                    'draw.start.x', 'draw.start.y', 'draw.block.x', 'draw.block.y', 'draw.end.x', 'draw.end.y', 
                    'draw.goal.x', 'draw.goal.y', 'goalType', 'xgot'
                ]

                # Filter the DataFrame to include only the selected columns
                result_df = df[selected_columns]
                return result_df

            else:
                print(f"Failed to fetch shot data. Status code: {response.status_code}")
                return None

        except Error as e:
            print(f"Error querying data: {e}")
            return None

        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to create the database connection.")
        return None

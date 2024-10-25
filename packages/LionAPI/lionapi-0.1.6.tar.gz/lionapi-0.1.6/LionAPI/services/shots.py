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
            query = """
                SELECT event_id
                FROM events
                WHERE home_team = %s AND away_team = %s AND event_date = %s;
            """
            cursor.execute(query, (home_team, away_team, match_date))
            result = cursor.fetchone()

            if result is None:
                print("No game found for the given paramaters")
                return None
            
            event_id = result['event_id']

            url = f"https://sofascore.com/api/v1/event/{event_id}/shotmap"
            response = requests.get(url)

            if response.status_code == 200:
                shot_data = response.json()
                shots = shot_data.get('shots',[])
                return pd.DataFrame(shots)
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
        print("Failed to create the database connection")
        return None

    
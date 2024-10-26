from LionAPI.services.database import create_connection
from mysql.connector import Error
import pandas as pd
import requests

def get_stats(home_team, away_team, match_date):
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
                print("No game found for the given parameters.")
                return None
            
            event_id = result['event_id']
            url = f"https://sofascore.com/api/v1/event/{event_id}/statistics"

            try:
                response = requests.get(url)
                response.raise_for_status()  
                
                match_data = response.json().get('statistics')[0].get('groups')
                match_overview = next((group for group in match_data if group.get('groupName') == "Match overview"), None)

                if match_overview is None:
                    print("No stats found in 'Match overview'.")
                    return None
                
                statistics_items = match_overview.get('statisticsItems')
                df = pd.DataFrame(statistics_items)

                return df
            
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                return None
            
        except Error as e:
            print(f"Database query error: {e}")
            return None
        
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to create database connection")
        return None

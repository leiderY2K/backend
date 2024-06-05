import mysql.connector

class MostPlayedGamesByCategory:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Error de conexión a MySQL: {err}")
            raise

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def get_top_played_categories(self):
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)

            query = """
            SELECT c.category, SUM(ug.time_played) AS total_jugado
            FROM User_Game ug
            JOIN Game_Category gc ON ug.id_game = gc.id_game
            JOIN Category c ON gc.id_category = c.id_category
            GROUP BY c.category
            HAVING total_jugado > 0 
            ORDER BY total_jugado DESC;
            """

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as err:
            print(f"Error al obtener los juegos más jugados por categoría: {err}")
            return None

        finally:
            self.close()

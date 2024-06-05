import mysql.connector

class GamesByCategory:
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

    def get_games_by_category(self):
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)

            query = """
            SELECT c.category, COUNT(g.id_game) AS total_games
            FROM Game g
            JOIN Game_Category gc ON g.id_game = gc.id_game
            JOIN Category c ON gc.id_category = c.id_category
            GROUP BY c.category
            ORDER BY total_games DESC;
            """

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as err:
            print(f"Error al obtener la cantidad de juegos por categoría: {err}")
            return None

        finally:
            self.close()

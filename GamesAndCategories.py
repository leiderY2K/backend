import mysql.connector

class GamesAndCategories:
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

    def get_games_and_categories(self):
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)

            query = """
            SELECT g.game_name, c.category 
            FROM game g
            JOIN game_category gc ON gc.id_game = g.id_game
            JOIN category c ON c.id_category = gc.id_category;
            """

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as err:
            print(f"Error al obtener los juegos y categorías: {err}")
            return None

        finally:
            self.close()

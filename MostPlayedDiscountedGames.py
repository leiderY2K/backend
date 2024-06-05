import mysql.connector

class MostPlayedDiscountedGames:
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

    def get_top_played_discounted_games(self):
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)

            query = """
            SELECT t.country_code, t.game_name, t.total_jugado
            FROM (
            SELECT u.country_code, g.game_name, SUM(ug.time_played) AS total_jugado,
                    ROW_NUMBER() OVER (PARTITION BY u.country_code ORDER BY SUM(ug.time_played) DESC) AS rn
            FROM User_Game ug
            JOIN Game g ON ug.id_game = g.id_game
            JOIN User u ON ug.id_user = u.id_user
            WHERE g.have_discount = 127
            GROUP BY u.country_code, g.game_name
            HAVING total_jugado > 0   -- Filtrar por total_jugado > 0
            ) t
            WHERE t.rn = 1
            ORDER BY t.total_jugado DESC;
            """

            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as err:
            print(f"Error al obtener los juegos con descuento más jugados: {err}")
            return None

        finally:
            self.close()


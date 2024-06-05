import mysql.connector

class MostPlayedGamesDates:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            print("Conexión exitosa a MySQL")
        except mysql.connector.Error as err:
            print(f"Error de conexión a MySQL: {err}")
            raise

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def get_top_played_games_between_dates(self, start_date, end_date):
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)

            query = """
            SELECT ug.id_game, g.game_name, SUM(ug.time_played) AS total_jugado
            FROM User_Game ug
            JOIN Game g ON ug.id_game = g.id_game
            WHERE ug.data_date BETWEEN %s AND %s
            GROUP BY ug.id_game, g.game_name
            ORDER BY total_jugado DESC
            LIMIT 10;
            """

            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            cursor.close()
            return results

        except mysql.connector.Error as err:
            print(f"Error al obtener los juegos más jugados entre fechas: {err}")
            return None

        finally:
            self.close()

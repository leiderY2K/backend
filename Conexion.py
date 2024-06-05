from flask import Flask, jsonify, request
from GamesAndCategories import GamesAndCategories
from GamesByCategory import GamesByCategory
from MostPlayedDiscountedGames import MostPlayedDiscountedGames
from MostPlayedGamesByCategory import MostPlayedGamesByCategory
from MostPlayedGamesByCountry import MostPlayedGamesByCountry
from game_stats_model import GameStatsModel
from most_played_games_dates import MostPlayedGamesDates

app = Flask(__name__)

db_config = {
    "user": "root",
    "password": "1234",
    "host": "localhost",
    "database": "proyectotend",
    "port": 3306
}

@app.route('/')
def home():
    return jsonify({"mensaje": "¡Bienvenido a la API del Proyecto de Tendencias!"})

@app.route('/juegos/mas-jugados')
def obtener_juegos_mas_jugados():
    try:
        model = GameStatsModel(db_config)
        juegos = model.get_top_played_games()
        
        if juegos is not None:
            return jsonify(juegos)
        else:
            return jsonify({"error": "No se pudieron obtener los juegos"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/juegos/mas-jugados-por-fecha', methods=['GET'])  # Corrige la ruta
def obtener_mas_jugados_por_fecha():
    try:
        data = request.get_json()
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']

        # Utiliza MostPlayedGamesDates
        model = MostPlayedGamesDates(db_config) 
        resultados = model.get_top_played_games_between_dates(fecha_inicio, fecha_fin)

        if resultados is not None:
            return jsonify(resultados)
        else:
            return jsonify({'error': 'No se pudieron obtener los datos'}), 500

    except KeyError:
        return jsonify({'error': 'Faltan campos en la solicitud (fecha_inicio, fecha_fin)'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/juegos/mas-jugados-por-pais', methods=['GET'])
def obtener_mas_jugados_por_pais():
    try:
        country_code = request.args.get('pais')

        if not country_code:
            return jsonify({'error': 'Falta el parámetro pais'}), 400

        model = MostPlayedGamesByCountry(db_config)
        resultados = model.get_top_played_games_by_country(country_code)

        if resultados is not None:
            return jsonify(resultados)
        else:
            return jsonify({'error': 'No se pudieron obtener los datos'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/juegos/mas-jugados-con-descuento', methods=['GET']) #uno por pais
def obtener_mas_jugados_con_descuento():
    try:
        model = MostPlayedDiscountedGames(db_config)
        resultados = model.get_top_played_discounted_games()

        if resultados is not None:
            return jsonify(resultados)
        else:
            return jsonify({'error': 'No se pudieron obtener los datos'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/juegos/tiempo-jugado-por-categoria', methods=['GET'])
def obtener_tiempo_jugado_por_categoria():
    try:
        model = MostPlayedGamesByCategory(db_config)
        resultados = model.get_top_played_categories()

        if resultados is not None:
            return jsonify(resultados)
        else:
            return jsonify({'error': 'No se pudieron obtener los datos'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/juegos/cantidad-por-categoria', methods=['GET'])
def obtener_cantidad_juegos_por_categoria():
    try:
        model = GamesByCategory(db_config)
        resultados = model.get_games_by_category()

        if resultados is not None:
            return jsonify(resultados)
        else:
            return jsonify({'error': 'No se pudieron obtener los datos'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/juegos/juegos-y-categorias', methods=['GET'])
def obtener_juegos_y_categorias():
    try:
        model = GamesAndCategories(db_config)
        resultados = model.get_games_and_categories()

        if resultados is not None:
            return jsonify(resultados)
        else:
            return jsonify({'error': 'No se pudieron obtener los datos'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from config.database import db
from models.challenge import DateTime, DataAggregate, Geolocation
from pydantic import ValidationError
from datetime import datetime
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa a aplicação Flask com base na variável FLASK_ENV do .env
app = Flask(os.environ["FLASK_ENV"])

# Configura o banco de dados usando a URL do banco vinda das variáveis de ambiente
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

# Desativa o recurso de rastreamento de modificações do SQLAlchemy (economiza recursos)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa a aplicação com o banco de dados
db.init_app(app)

CORS(app)


# Cria uma rota GET para retornar dados meteorológicos
@app.route("/", methods=["GET"])
def get_weather():
    # Obtém a data atual no formato "YYYY-MM-DD"
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Obtém o parâmetro de query "neighborhood" (bairro)
    neighborhood = request.args.get("neighborhood")

    try:
        # Realiza a query para obter dados agregados com base na data e no bairro
        results = DataAggregate.query.filter(
            DateTime.target_date == current_date,  # Filtra pela data atual
            Geolocation.neighborhood == neighborhood,  # Filtra pelo bairro fornecido
        ).all()

        # Converte os resultados da query para uma lista de dicionários
        result_list = [
            {
                "id": data_aggregate_obj.date_time_id,  # ID do registro de data e hora
                "target_time": data_aggregate_obj.date_time.target_time,  # Hora específica
                "content": {
                    "geo_id": data_aggregate_obj.geo_id,  # ID geográfico
                    "temperature": data_aggregate_obj.mid_temp,  # Temperatura média
                    "wind_speed": data_aggregate_obj.mid_wind_speed,  # Velocidade média do vento
                    "wind_direction": data_aggregate_obj.mid_wind_direction,  # Direção média do vento
                    "real_feal": data_aggregate_obj.mid_real_feal,  # Sensação térmica
                    "humidity": data_aggregate_obj.mid_humidity,  # Umidade média
                },
            }
            for data_aggregate_obj in results
        ]

        # Monta a resposta com os dados e metadados, incluindo o total de resultados
        response = {"data": result_list, "metadata": {"total": len(result_list)}}

        # Retorna a resposta como JSON
        return jsonify(response)

    # Caso ocorra um erro de validação, retorna os erros com status 400 (bad request)
    except ValidationError as err:
        return jsonify(err.errors()), 400


# Executa a aplicação em modo debug se estiver em ambiente de desenvolvimento
if os.environ["FLASK_ENV"] == "development":
    app.run(debug=True)
# Executa a aplicação em modo normal se estiver em outro ambiente
else:
    app.run()

from .database_client import DatabaseClient
from flask import Flask
from flask import render_template
from .graph_lib import (create_chart_avg_discount_platform,
                        create_pie_chart_platform,
                        create_chart_avg_price_platform,
                        create_line_chart_avg_price,
                        create_bar_chart_review)

# Création de l'application Flask
app = Flask(__name__, static_url_path='/static')

# Instanciation de l'objet de connexion à la base de données
client = DatabaseClient()

# Récupération des données sous forme de dataframe
data = client.get_data_as_dataframe()


@app.route("/")
def accueil():
    """
    :return: Retourne la template page d'accueil et les graphiques
    """
    return render_template('index.html',
                           nb_data=len(data),
                           plot_avg_price=create_line_chart_avg_price(data),
                           plot_review=create_bar_chart_review(data),
                           plot_selling_platform=create_pie_chart_platform(data),
                           plot_avg_platform_price=create_chart_avg_price_platform(data),
                           plot_avg_discount=create_chart_avg_discount_platform(data))


@app.route("/display_data/<int:num_page>")
def display_data(num_page):
    """
    Retourne une liste de données depuis le dataframe séquencée en fonction du numéro de la page.
    :param num_page: numéro de la page actuelle
    :return: la template html
    """
    nb_data_par_page = 60
    debut = (num_page - 1) * nb_data_par_page
    fin = debut + nb_data_par_page
    data_coupee = data.iloc[debut:fin]
    nb_pages_total = len(data) // nb_data_par_page + (0 if len(data) % nb_data_par_page == 0 else 1)
    return render_template("display_data.html",
                           nb_data=len(data),
                           tables=[data_coupee.to_html(classes='data')],
                           nb_pages_total=nb_pages_total,
                           current_page=num_page)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        debug=True)

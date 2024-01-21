from .database_client import DatabaseClient
from flask import Flask
from flask import render_template
from .graph_lib import (create_chart_avg_discount_platform,
                        create_pie_chart_platform,
                        create_chart_avg_price_platform,
                        create_line_chart_avg_price,
                        create_bar_chart_review)

app = Flask(__name__, static_url_path='/static')
client = DatabaseClient()

data = client.get_data_as_dataframe()



@app.route("/")
def hello_world():
    # return render_template('index.html', plot=fig_date.to_html(), tables=[data_date.to_html(classes='data')])
    return render_template('index.html',
                           plot_avg_price=create_line_chart_avg_price(data),
                           plot_review=create_bar_chart_review(data),
                           plot_selling_platform=create_pie_chart_platform(data),
                           plot_avg_platform_price=create_chart_avg_price_platform(data),
                           plot_avg_discount=create_chart_avg_discount_platform(data))


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        debug=True)

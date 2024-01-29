import pandas as pd
import plotly
import plotly_express as px

# Collection de fonctions servant à générer des graphiques depuis les données
def create_line_chart_avg_price(data):
    """
    :param data:
    :return: Un linechart du prix moyen par année
    """
    data_date = data[~data["tags"].astype(str).str.contains("DLC", na=False)]
    data_date = data_date.dropna(subset=["date_published"]).reset_index(drop=True)
    data_date["date_published"] = data_date["date_published"].str.replace('-PC', '')
    data_date.loc[:, "date_published"] = data_date["date_published"].str[-4:]
    data_date = data_date[data_date["date_published"].astype(str).str.match(r'\d{4}$')]
    new_dataframe = pd.concat([data_date["date_published"], data_date["final_price"]], axis=1)
    average_prices_by_year = new_dataframe.groupby("date_published")["final_price"].mean().reset_index()

    #Graph autre

    fig_date = px.line(average_prices_by_year, x='date_published', y='final_price', title='Prix moyen par année d\'un jeu (année de référence: 2024)',
                  labels={'date_published': 'Année de publication', 'final_price': 'Prix du moyen d\'un jeu (euros)'},
                  markers=True, line_shape='linear')

    return fig_date.to_html()


def create_bar_chart_review(data):
    """
    :param data:
    :return: Un bar chart des notes des utilisateurs en moyenne
    """
    data['ig_review_average'] = data['ig_review_average'].replace(-1, None)
    data = data.dropna(subset=['ig_review_average'])
    occurrences_series = data['ig_review_average'].value_counts()
    occurrences_note = pd.DataFrame({'valeur': occurrences_series.index, 'occurrence': occurrences_series.values})
    fig_review = px.bar(occurrences_note, x="valeur", y="occurrence",
                        labels={'valeur': "Note des jeux", 'occurrence': "Nombre de note"},
                        category_orders={"valeur": occurrences_note['valeur'].sort_values().unique()})

    return fig_review.to_html()


def create_pie_chart_platform(data):
    """
    :param data:
    :return: Un pie chart de la proportion des plateformes de vente à l'origine
    """
    occurrences_series = data['original_selling_platform'].value_counts()
    occurrences_platform = pd.DataFrame(
        {'original_selling_platform': occurrences_series.index, 'occurrence': occurrences_series.values})

    fig_selling_platform = px.pie(occurrences_platform,
                                  values="occurrence",
                                  names="original_selling_platform",
                                  labels={'occurrence': 'Nombre de jeux vendus', 'original_selling_platform': "Plateforme d'origine"})
    return fig_selling_platform.to_html()

def create_chart_avg_price_platform(data):
    """
    :param data:
    :return: Un bar chart du prix moyen par plateforme de vente à l'origine
    """
    df = data.dropna(subset=['final_price']).copy()
    df['final_price'] = pd.to_numeric(df['final_price'], errors='coerce')
    average_prices = df.groupby('original_selling_platform')['final_price'].mean().reset_index()
    price_platform = average_prices[['original_selling_platform', 'final_price']]
    price_platform.columns = ['platform', 'average_price']
    price_platform = price_platform.sort_values(by='average_price', ascending=True)

    fig_avg_price_platform = px.bar(price_platform,
                                    x="platform",
                                    y="average_price",
                                    labels={'average_price': 'Prix moyens (après réduction)', 'platform': 'Plateforme'})
    return fig_avg_price_platform.to_html()


def create_chart_avg_discount_platform(data):
    """
    :param data:
    :return: Un bar chart des réductions effectuées en moyenne
    """
    df = data.dropna(subset=['discounted'])
    df['discounted'] = pd.to_numeric(df['discounted'], errors='coerce')
    average_discounted = df.groupby('original_selling_platform')['discounted'].mean().reset_index()
    platform_discount = average_discounted[['original_selling_platform', 'discounted']]
    platform_discount.columns = ['platform', 'average_discounted']
    platform_discount = platform_discount.sort_values(by='average_discounted', ascending=False)

    fig_discount = px.bar(platform_discount,
                          x="average_discounted",
                          y="platform",
                          labels={'average_discounted': 'Moyenne des réductions', 'platform': 'Plateforme'},
                          orientation='h')
    return fig_discount.to_html()

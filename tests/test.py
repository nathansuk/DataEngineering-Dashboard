from database_client import DatabaseClient


def executer_test_db():
    client = DatabaseClient()

    print(client.get_client())
    print(client.get_instantgaming_series())
    print(client.get_nb_document())
    print(client.is_database_empty())
    print(client.get_data_as_dataframe().head(50))
from connector import CustomMySQLConnector
import json


if __name__ == "__main__":

    with open("../../config.json", 'r', encoding='utf-8') as file:
        config = json.load(file)

    db_config = config["database"]
    mysql_connector = CustomMySQLConnector(db_config)
    mysql_connector.connect()
    mysql_connector.insert_articles_from_json("../new_generated_articles.json")
    mysql_connector.close()
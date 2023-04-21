import psycopg2

host = "84.201.135.211"
user = "ushops01"
password = "HSEP@ssword2022"
db = "shops01"


class DBProduct:
    def __init__(self):
        self.connection = self.connect_db()

    @staticmethod
    def connect_db():
        connection = None
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                port=5430,
                password=password,
                database=db
            )
        except Exception:
            raise Exception("Bad Connection")

        return connection

    def get_products_by_name(self, product_name: str, page: int, offset=50) -> list:
        result = []
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT p.title, p.price, c.name as category, p.id, p.images from product as p "
                    f"left outer join category c on c.id = p.app_category_id WHERE p.title LIKE '%{product_name}%' "
                    f"LIMIT {offset + 1} OFFSET {(page - 1) * offset};")
                result = cursor.fetchall()
        except Exception as ex:
            print(ex)

        return result

    def get_all_high_level_categories(self) -> list:
        result = []
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT c.name as category from product as p "
                           "left outer join category c on c.id = p.app_category_id;")
            result = list(map(lambda x: x[0], cursor.fetchall()))

        return result

    def __del__(self):
        if self.connection:
            self.connection.close()

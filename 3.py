import csv
import json
from dataclasses import dataclass
from typing import Final


SALES_FILE: Final[str] = "sales.json"
PRODUCTS_FILE: Final[str] = "products.csv"


@dataclass
class Sale:
    sale_id: int
    amount: int


@dataclass
class Product:
    product_id: int
    product_name: str
    sales: list[Sale] | None = None

    def __post_init__(self):
        if isinstance(self.product_id, str) and self.product_id.isdigit():
            self.product_id = int(self.product_id)
        else:
            raise Exception("Поле product_id должно быть числом")


def get_sales() -> dict[int, list[dict]]:
    with open(SALES_FILE, "r") as file:
        data = json.load(file)
    sales: dict[int, list[dict]] = {}
    for sale in data:
        product_id = sale.pop("product_id")
        if product_id in sales:
            sales[product_id].append(sale)
        else:
            sales[product_id] = [sale]
    return sales


def get_products() -> list[Product]:
    with open(PRODUCTS_FILE) as file:
        lines = csv.DictReader(file, delimiter=";")
        return [Product(**line) for line in lines]


def merge(products: list[Product], sales: dict[int, list[dict]]) -> list[Product]:
    for product in products:
        if product_sales := sales.get(product.product_id):
            product.sales = [Sale(**sale) for sale in product_sales]
    return products


def represent(products: list[Product]) -> None:
    print("product_id", "\t" * 2, "product_name", "\t" * 2, "sale_id", "\t" * 2, "amount")
    print("-" * 60)
    for product in products:
        for sale in product.sales:
            print(
                product.product_id,
                "\t" * 4,
                product.product_name,
                "\t" * 3,
                sale.sale_id,
                "\t" * 4,
                sale.amount,
            )
            print("-" * 60)


def main():
    products = merge(get_products(), get_sales())
    represent(products)


if __name__ == "__main__":
    main()

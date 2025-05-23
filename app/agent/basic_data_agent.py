import csv
from collections import defaultdict, Counter


class CSVDataAgent:
    def __init__(self, filepath):
        self.data = []
        self.customers_products = defaultdict(list)
        self.product_customers = defaultdict(set)
        self.customer_purchase_count = Counter()
        self.load_csv(filepath)

    def load_csv(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer = row['CustomerName'].strip()
                product = row['Product'].strip()
                quantity = int(row.get('Quantity', 1))
                self.data.append(row)
                self.customers_products[customer].append(product)
                self.product_customers[product].add(customer)
                self.customer_purchase_count[customer] += quantity

    def handle_query(self, query: str) -> str:
        query = query.lower()

        if "top 5 customers" in query:
            top = self.customer_purchase_count.most_common(5)
            return "\n".join(f"{c}: {q} purchases" for c, q in top)

        elif "how many customers bought" in query:
            for product in self.product_customers:
                if product.lower() in query:
                    return f"{len(self.product_customers[product])} customers bought {product}"
            return "Product not found."

        elif "list all products purchased by" in query:
            for customer in self.customers_products:
                if customer.lower() in query:
                    return f"{customer} purchased: {', '.join(set(self.customers_products[customer]))}"
            return "Customer not found."

        elif "who purchased" in query:
            for product in self.product_customers:
                if product.lower() in query:
                    return f"Customers who purchased {product}: {', '.join(self.product_customers[product])}"
            return "Product not found."

        elif "total unique products" in query:
            unique_products = {row['Product'] for row in self.data}
            return f"Total unique products purchased: {len(unique_products)}"

        else:
            return "Sorry, I didn't understand that query."

if __name__ == "__main__":
    agent = CSVDataAgent("data/customer_data.csv")
    while True:
        q = input("Ask a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        print(agent.handle_query(q))

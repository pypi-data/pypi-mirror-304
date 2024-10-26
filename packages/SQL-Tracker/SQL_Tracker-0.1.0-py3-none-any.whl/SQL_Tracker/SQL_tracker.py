import time
import sqlparse
from prettytable import PrettyTable

class RealTimeDataLineageTracker:
    def __init__(self):
        """Initialize the lineage tracker."""
        self.lineage = {}

    def intercept_sql_query(self, query):
        """Intercept and process the SQL query with error handling."""
        try:
            parsed_query = sqlparse.format(query, keyword_case='upper', reindent=True)
            print(f"\nIntercepted Query:\n{parsed_query}")
            self.track_lineage(parsed_query)
        except Exception as e:
            print(f"Error processing query: {e}")

    def track_lineage(self, query):
        """Track table transformations dynamically at row and column levels."""
        try:
            query_lower = query.lower()
            source_table, columns = self.extract_table_and_columns(query_lower)

            # Determine the type of transformation
            if "where" in query_lower:
                target_table = f"{source_table}_filtered"
            elif "group by" in query_lower:
                target_table = f"{source_table}_aggregated"
            else:
                target_table = source_table

            # Store the transformation and visualize it
            self.add_transformation(source_table, target_table, columns, query)
        except Exception as e:
            print(f"Error tracking lineage: {e}")

    def extract_table_and_columns(self, query):
        """Extract the source table and columns from the SQL query."""
        try:
            source_table = query.split("from")[1].split()[0]
            select_part = query.split("select")[1].split("from")[0].strip()
            columns = [col.strip() for col in select_part.split(",")]

            return source_table, columns
        except IndexError:
            raise ValueError("Invalid SQL query format. Please try again.")

    def add_transformation(self, source_table, target_table, columns, query):
        """Store and visualize the transformation."""
        if source_table not in self.lineage:
            self.lineage[source_table] = {"type": "source", "transformations": []}

        self.lineage[target_table] = {
            "type": "transformation",
            "source": source_table,
            "query": query,
            "columns": columns,
            "transformations": []
        }
        self.lineage[source_table]["transformations"].append(target_table)

        print(f"Lineage Updated: {source_table} → {target_table}")
        self.visualize_transformation(source_table, target_table, columns)

    def visualize_transformation(self, source, target, columns):
        """Display the transformation using PrettyTable."""
        before = PrettyTable()
        after = PrettyTable()

        before.field_names = columns
        after.field_names = columns

        for i in range(1, 4):
            before.add_row([f"{col}_val{i}" for col in columns])
            if "filtered" in target:
                if i % 2 == 0:  # Simulate filtering
                    after.add_row([f"{col}_val{i}" for col in columns])
            else:
                after.add_row([f"{col}_val{i}" for col in columns])

        print(f"\nSource Table: {source}")
        print(before)
        print(f"\nTarget Table: {target} (After Transformation)")
        print(after)

    def visualize_lineage(self):
        """Print the full lineage information."""
        print("\n--- Real-Time Lineage ---")
        for table, details in self.lineage.items():
            print(f"Table: {table}")
            print(f"  Type: {details['type']}")
            if "source" in details:
                print(f"  Source: {details['source']}")
            if "query" in details:
                print(f"  Query: {details['query']}")
            if details["transformations"]:
                print(f"  Next Transformations: {details['transformations']}")
            print()

def dynamic_query_execution(tracker):
    """Continuously accept SQL queries from the user."""
    print("Enter your SQL queries below (type 'exit' to quit):\n")
    while True:
        query = input("SQL Query: ").strip()
        if query.lower() == 'exit':
            print("Exiting program...")
            break
        tracker.intercept_sql_query(query)
        tracker.visualize_lineage()
        time.sleep(1)  # Simulate a short delay between queries

# Initialize the tracker and start dynamic query execution
tracker = RealTimeDataLineageTracker()
dynamic_query_execution(tracker)

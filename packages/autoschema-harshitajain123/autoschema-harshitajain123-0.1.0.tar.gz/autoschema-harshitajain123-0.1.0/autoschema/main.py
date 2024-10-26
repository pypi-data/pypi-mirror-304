import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutoSchemaMigrator:
    def __init__(self, source_db_url, target_db_url):
        """
        Initializes the AutoSchemaMigrator with dynamic database URLs.
        :param source_db_url: The URL of the source (any) database.
        :param target_db_url: The URL of the target (any) database.
        """
        self.source_db_url = source_db_url
        self.target_db_url = target_db_url
        
        # Initialize engines for both databases
        self.source_engine = sqlalchemy.create_engine(self.source_db_url)
        self.target_engine = sqlalchemy.create_engine(self.target_db_url)

    def fetch_schema(self, engine):
        """Fetches the schema (tables, columns, indexes) from the database."""
        try:
            with engine.connect() as conn:
                inspector = sqlalchemy.inspect(conn)
                return {
                    'tables': inspector.get_table_names(),
                    'columns': {table: inspector.get_columns(table) for table in inspector.get_table_names()},
                    'indexes': {table: inspector.get_indexes(table) for table in inspector.get_table_names()},
                }
        except SQLAlchemyError as e:
            logging.error(f"Error fetching schema: {e}")
            return None

    def compare_schemas(self, source_schema, target_schema):
        """Compares the schemas of two databases and identifies differences."""
        differences = {}
        for table in source_schema['tables']:
            if table not in target_schema['tables']:
                differences[table] = 'missing in target'
            else:
                # Compare columns
                source_columns = {col['name']: col['type'] for col in source_schema['columns'][table]}
                target_columns = {col['name']: col['type'] for col in target_schema['columns'][table]}
                
                missing_columns = {col: str(source_columns[col]) for col in source_columns if col not in target_columns}
                if missing_columns:
                    differences[table] = f'missing columns in target: {missing_columns}'
                
                # Compare indexes
                source_indexes = set(idx['name'] for idx in source_schema['indexes'][table])
                target_indexes = set(idx['name'] for idx in target_schema['indexes'][table])
                missing_indexes = source_indexes - target_indexes
                if missing_indexes:
                    if table in differences:
                        differences[table] += f"; missing indexes in target: {missing_indexes}"
                    else:
                        differences[table] = f'missing indexes in target: {missing_indexes}'
        return differences

    def generate_migration_script(self, differences):
        """Generates a SQL migration script based on the differences."""
        script = []
        for table, status in differences.items():
            if status == 'missing in target':
                columns = self.source_schema['columns'][table]
                column_definitions = [f"{col['name']} {str(col['type'])}" for col in columns]
                columns_sql = ", ".join(column_definitions)
                script.append(f'CREATE TABLE {table} ({columns_sql});')
            elif 'missing columns' in status:
                # Manually parse the missing columns from the status string
                missing_columns_str = status.split("missing columns in target: ")[-1].strip()
                missing_columns_str = missing_columns_str.strip("{}")
                missing_columns_pairs = missing_columns_str.split(',')
                
                missing_columns = {}
                for pair in missing_columns_pairs:
                    if ':' in pair:
                        col_name, col_type = pair.split(':')
                        missing_columns[col_name.strip().strip("'")] = col_type.strip().strip("'")
                
                for col_name, col_type in missing_columns.items():
                    script.append(f'ALTER TABLE {table} ADD COLUMN {col_name} {col_type};')
            elif 'missing indexes' in status:
                # Manually parse the missing indexes from the status string
                missing_indexes_str = status.split("missing indexes in target: ")[-1].strip()
                missing_indexes = missing_indexes_str.strip("{}").split(',')
                
                for index in missing_indexes:
                    index = index.strip()
                    indexed_columns = [col['name'] for col in self.source_schema['indexes'][table] if col['name'] == index]
                    script.append(f'CREATE INDEX {index} ON {table} ({", ".join(indexed_columns)});')
        return '\n'.join(script)

    def migrate(self):
        """Fetches the schemas from both databases, compares them, and generates a migration script."""
        source_schema = self.fetch_schema(self.source_engine)
        target_schema = self.fetch_schema(self.target_engine)

        if source_schema is None or target_schema is None:
            logging.error("Schema fetch failed. Migration cannot proceed.")
            return ""

        self.source_schema = source_schema  # Store source schema for later use
        differences = self.compare_schemas(source_schema, target_schema)
        migration_script = self.generate_migration_script(differences)
        return migration_script

if __name__ == '__main__':
    # Example usage, accepting any database URLs dynamically
    source_url = input("Enter the source database URL: ").strip()
    target_url = input("Enter the target database URL: ").strip()
    
    migrator = AutoSchemaMigrator(source_url, target_url)
    migration_script = migrator.migrate()
    
    if migration_script:
        logging.info(f"Generated Migration Script:\n{migration_script}")
    else:
        logging.error("No migration script generated.")

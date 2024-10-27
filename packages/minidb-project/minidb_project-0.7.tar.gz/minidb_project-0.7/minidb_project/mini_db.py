class Database:
    def __init__(self):
        self.tables = {}
        self.current_table = None

    def create_table(self, name):
        self.tables[name] = []
        self.current_table = name

    def insert(self, record):
        if self.current_table is not None:
            self.tables[self.current_table].append(record)

    def select(self):
        return self.tables.get(self.current_table, [])

    def navigate(self, table_name):
        self.current_table = table_name

    def delete(self, record_id):
        """ Deleta o registro pelo campo 'id' """
        if self.current_table is not None:
            self.tables[self.current_table] = [
                record for record in self.tables[self.current_table] if record.get('id') != record_id
            ]
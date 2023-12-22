import db


class CRUDService:

    def __init__(self, tableName):
        self.primaryKey = None
        self.schema = None
        self.tableName = tableName

        self.initSchema()

    def initSchema(self):
        conn = db.get_db()
        sql = 'PRAGMA table_info({0})'.format(self.tableName)
        cursor = conn.execute(sql)
        rows = cursor.fetchall()

        schema = {}
        for row in rows:
            name = row['name']
            type = row['type']
            schema[name] = type
            if row['pk']:
                self.primaryKey = name
        self.schema = schema

    def getEmpty(self):
        empty = {}
        for key in self.schema:
            empty[key] = ''
        return empty

    def create(self, data):
        conn = db.get_db()

        placeholders = []
        insertKeys = []
        for key in self.schema.keys():
            if key is self.primaryKey:
                continue
            if key in data:
                insertKeys.append(key)
                # we are using named placeholders here for the query building
                placeholders.append(':' + key)

        sql = 'INSERT INTO {0} ({1}) VALUES ({2});'.format(
            self.tableName, ', '.join(insertKeys), ', '.join(placeholders)
        )
        conn.execute(sql, data)
        conn.commit()
        return True

    def readAll(self):
        conn = db.get_db()
        sql = 'SELECT * FROM {0}'.format(self.tableName)
        results = conn.execute(sql).fetchall()
        return results

    def readByPK(self, id):
        conn = db.get_db()
        sql = 'SELECT * FROM {0} WHERE {1} = ?;'.format(
            self.tableName, self.primaryKey)
        el = conn.execute(sql, (str(id),)).fetchone()
        return el

    def readBy(self, key, value):
        conn = db.get_db()
        sql = 'SELECT * FROM {0} WHERE {1} = ?;'.format(
            self.tableName, key)
        el = conn.execute(sql, (str(value),)).fetchall()
        return el

    def read(self, id=False):
        if id is False:
            return self.readAll()
        return self.readByPK(id)

    def update(self, data):
        conn = db.get_db()

        keysAndPlaceholders = []
        for key in self.schema.keys():
            if key is self.primaryKey:
                continue
            if key in data:
                keysAndPlaceholders.append('{0} = :{1}'.format(key, key))

        sql = 'UPDATE {0} SET {1} WHERE {2} = :{2};'.format(
            self.tableName, ', '.join(keysAndPlaceholders), self.primaryKey
        )
        conn.execute(sql, data)
        conn.commit()
        return True

    def delete(self, id):
        conn = db.get_db()
        sql = 'DELETE FROM {0} WHERE {1} = ?;'.format(
            self.tableName, self.primaryKey)
        conn.execute(sql, (id,))
        conn.commit()
        return True

from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:
    # Dictionary of objects saved to the database.

    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @property
    def employee_id(self):
        return self._employee_id 
    
    @employee_id.setter
    def employee_id(self, employee_id):
        if not employee_id in Employee.all:
            raise ValueError('NOT  VALID')
        else:
            self._employee_id = employee_id

    
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO reviews (year, summary, employee_id)
            VALUES (?, ?, ?)
        """
        try:
            CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        except:
            raise ValueError('Save Failed')



    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        if not isinstance(year, int):
            raise ValueError('Year must be an int')
        elif not year >= 2000:
            raise ValueError('Year length must larger than or equal  to 2000')
        elif not len(summary) > 0:
            raise ValueError('Summary must be included')
        elif not employee_id in Employee.all:
            raise ValueError('Employee Id must be valid')
        else:
            new_obj = cls(year,summary,employee_id)
            new_obj.save()
            return new_obj
        
        
        
        
        
        
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
        # Check the dictionary for  existing instance using the row's primary key
        review = cls.all.get(row[0])

        if review:
            review.year = row[1]
            review.summary = row[2]
            review.employee_id = row[3]
        else:
            review = cls(row[1],row[2],row[3])
            review.id = row[0]
            cls.all[review.id] = review
        return review
   


    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        sql = """
            SELECT *
            FROM reviews
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None


    def update(self):
        """Update the table row corresponding to the current Review instance."""
        sql ="""
            UPDATE reviews
            SET year = ?, summary = ?, employee_id = ?
            WHERE id = ?
        """
        if not self.employee_id in Employee.all:
            print('TRIGGERED')
            raise ValueError('MUST BE VALID EMPLOYEE')
        else:
            CURSOR.execute(sql, (self.year,self.summary, self.employee_id, self.id))
            CONN.commit()
            type(self).all[self.id] = self



    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        sql = """
            DELETE FROM reviews
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]

        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        
        sql = """
            SELECT *
            FROM reviews
        """

        rows = CURSOR.execute(sql).fetchall()

        return [ cls.instance_from_db(row) for row in rows]

 
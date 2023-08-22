import sqlite3

# connect to the database
connection = sqlite3.connect("garage_system.db", check_same_thread=False)

# get the cursor that is used for
# communication with the database
cursor = connection.cursor()

# if the cars table does not exist
# make sure that it is created
cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS
        cars
        (
            id              INTEGER PRIMARY KEY,
            first_name      VARCHAR(64),
            last_name       VARCHAR(128),
            licence_plate   VARCHAR(128)
        )
    """
)

# commit all the changes to the database
connection.commit()


def get_users():
    return cursor.execute(
        """
            SELECT * FROM cars
        """
    ).fetchall()


def check_user(first_name, last_name, licence_plate):
    # execute the query that adds the user
    # to the database
    return len(cursor.execute(
        """
            SELECT * FROM cars WHERE first_name=? AND last_name=? AND licence_plate=?
        """, (first_name, last_name, licence_plate)
    ).fetchall()) > 0


def create_user(first_name, last_name, licence_plate):
    # if the user exists
    # return out of the method
    if check_user(first_name, last_name, licence_plate):
        return False

    # execute the query that adds the user
    # to the database
    cursor.execute(
        """
            INSERT INTO 
                cars(id, first_name, last_name, licence_plate)
            VALUES
                (NULL, ?, ?, ?) 
        """, (first_name, last_name, licence_plate)
    )

    # after the query has executed commit
    # the changes to the database
    connection.commit()

    # return true meaning that
    # user has been added
    return True


def check_licence_plate(licence_plate):
    return cursor.execute(
        """
            SELECT first_name, last_name FROM cars WHERE licence_plate=?
        """, [licence_plate]
    ).fetchall()

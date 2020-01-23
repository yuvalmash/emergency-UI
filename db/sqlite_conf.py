tables =   ["""
            CREATE TABLE IF NOT EXISTS Incidents (
                id integer PRIMARY KEY AUTOINCREMENT,
                lat float NOT NULL,
                lon float NOT NULL,
                category text,
                start_time datetime default current_timestamp
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Media (
                id integer PRIMARY KEY AUTOINCREMENT,
                incident_id integer,
                data text NOT NULL,
                FOREIGN KEY (incident_id) REFERENCES incidents (id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Users (
                id integer PRIMARY KEY AUTOINCREMENT,
                phone_number text NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS incident_user (
                id integer PRIMARY KEY AUTOINCREMENT,
                incident_id integer NOT NULL,
                user_id integer NOT NULL,
                token text NOT NULL,
                FOREIGN KEY (incident_id) REFERENCES incidents (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
            ]
insert_queries = {'incidents': "INSERT INTO incidents (lat, lon, category) VALUES (?, ?, ?)",
                  'media': "INSERT INTO media (data, incident_id) VALUES (?, ?)",
                  'users': "INSERT INTO users (phone_number) VALUES (?)",
                  'incident_user': "INSERT INTO incident_user (incident_id, user_id, token) VALUES (?, ?, ?)"
                  }
update_queries = {'incidents': "UPDATE incidents SET lat=?, lon=? WHERE id LIKE ?"}

queries = {'id_from_token': "SELECT incident_id FROM incident_user WHERE token=?"}

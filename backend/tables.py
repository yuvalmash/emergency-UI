tables =   ["""
            CREATE TABLE IF NOT EXISTS Incidents (
                id integer PRIMARY KEY,
                lat float NOT NULL,
                lon float NOT NULL,
                category text,
                start_time datetime default current_timestamp,
                end_time datetime default current_timestamp
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Media (
                id integer PRIMARY KEY,
                path text NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Users (
                id integer PRIMARY KEY,
                phone_number text UNIQUE NOT NULL
            );
            """
            ]
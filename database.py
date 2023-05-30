import sqlite3

connection = sqlite3.connect("knotifier.db", check_same_thread=False)
cursor = connection.cursor()

class knotifier:
    def initiate() -> None:
        """Creates all tables if they do not exist"""
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS monitored (
            uid INTEGER,
            seriesId INTEGER,
            lastChapter INTEGER,
            friendlyName TEXT
            )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS emails (
            uid INTEGER,
            email TEXT
            )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS telegram_channels (
            uid INTEGER,
            channel_id int
            )"""
        )

        connection.commit()

    class db:
        def track(uid, seriesId, lastChapter, friendlyName):
            """Inserts a series into the database"""
            cursor.execute(
                """INSERT INTO monitored VALUES (?, ?, ?, ?)""",
                (uid, seriesId, lastChapter, friendlyName),
            )
            connection.commit()
            return True

        def get_email(uid):
            """Retrieves the email associated with a UID"""
            cursor.execute(
                "SELECT email FROM emails WHERE uid=?", (uid,)
            )
            result = cursor.fetchone()

            if result is not None:
                return result[0]  # Extract the email from the result tuple
            else:
                return None  # Return None if no email is found

        def save_email(uid, email):
            """Saves the email and UID into the database"""
            # Check if the UID already exists in the table
            cursor.execute("SELECT uid FROM emails WHERE uid=?", (uid,))
            result = cursor.fetchone()

            if result is not None:
                # Update the email if the UID already exists
                cursor.execute("UPDATE emails SET email=? WHERE uid=?", (email, uid))
            else:
                # Insert a new row if the UID doesn't exist
                cursor.execute(
                    "INSERT INTO emails (uid, email) VALUES (?, ?)", (uid, email)
                )

            # Commit the changes and close the connection
            connection.commit()
            return True

        def get_tracked_series(uid):
            """Retrieves series IDs and their friendly names tracked by a user from the database"""
            cursor.execute(
                "SELECT seriesId, friendlyName FROM monitored WHERE uid=?", (uid,)
            )
            results = cursor.fetchall()

            if results:
                tracked_series = [(result[0], result[1]) for result in results]
                return tracked_series
            else:
                return []

        def save_telegram_chat_id(uid, channel_id):
            """Saves the Telegram channel ID with the Discord user ID"""
            # Check if the UID already exists in the table
            cursor.execute(
                "SELECT uid FROM telegram_channels WHERE uid=?", (uid,)
            )
            result = cursor.fetchone()

            if result is not None:
                # Update the channel ID if the UID already exists
                cursor.execute(
                    "UPDATE telegram_channels SET channel_id=? WHERE uid=?", (channel_id, uid)
                )
            else:
                # Insert a new row if the UID doesn't exist
                cursor.execute(
                    "INSERT INTO telegram_channels (uid, channel_id) VALUES (?, ?)", (uid, channel_id)
                )

            # Commit the changes and close the connection
            connection.commit()
            return True

        def get_telegram_chat_id(uid):
            """Retrieves the Telegram channel ID associated with a Discord user ID"""
            cursor.execute(
                "SELECT channel_id FROM telegram_channels WHERE uid=?", (uid,)
            )
            result = cursor.fetchone()

            if result is not None:
                return result[0]  # Extract the channel ID from the result tuple
            else:
                return None  # Return None if no channel ID is found

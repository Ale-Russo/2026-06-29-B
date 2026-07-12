from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country
                from customer c
                where c.Country is not null
                order by c.Country
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct a.* 
from album a, track t
where a.AlbumId = t.AlbumId 
                """

        cursor.execute(query)

        for row in cursor:
            results.append(Album(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAlbumTracks():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select a.AlbumId, t.TrackId  
from album a, track t
where a.AlbumId = t.AlbumId
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct t1.AlbumId as a1, t2.AlbumId as a2
from track t1, track t2
where t1.Albumid < t2.AlbumId
and t1.GenreId = t2.GenreId
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

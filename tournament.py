from itertools import izip
import psycopg2


def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<p>Something Happened :(</p>")


def close(db, cursor):
    try:
        db.close()
        cursor.close()
    except:
        print("<p style=\"color:red\">Something Happened :(</p>")


def deleteMatches():
    db, c = connect()
    c.execute("delete from matches")
    db.commit()
    close(db, c)


def deletePlayers():
    db, c = connect()
    c.execute("TRUNCATE players CASCADE")
    db.commit()
    close(db, c)


def countPlayers():
    db, c = connect()
    c.execute("select count(id) from players")
    count = c.fetchone()[0]
    close(db, c)
    return count


def registerPlayer(name):
    db, c = connect()
    query = "insert into players (name) values (%s)"
    c.execute(query, (name, ))
    db.commit()
    close(db, c)


def playerStandings():
    # connect to database
    db, c = connect()
    # get list of players with win count sorted by wins
    query = """
      select pr.id,pr.name,winners.wins,count(pr.matches) as matches
      from player_records as pr
      left join winners on pr.id = winners.id group by
      pr.id,pr.name,winners.wins order by winners.wins;
            """

    # execute the query
    c.execute(query)

    # get results back
    standing = c.fetchall()
    close(db, c)

    # return the list of players
    return standing


def reportMatch(winner, loser):
    # connect to database
    db, c = connect()
    # query to insert matches
    query = "insert into matches (winner,loser) values(%s,%s)"
    # bind values to query and execute
    c.execute(query, (winner, loser))
    # commit changes
    db.commit()
    close(db, c)


# create pairs of two from single list
# stackoverflow link : https://goo.gl/wH22xJ
def split(list):
    return zip(list[0::2], list[1::2])


def swissPairings():
    # get players list ordered by wins
    standing = playerStandings()
    # split list in 2 groups, 4 in each group in case of 8 players
    splitted = split(standing)
    # list to return
    matched_pair = list()
    # loop through group of 2
    for pair in splitted:
        # temporary list
        pairing = list()
        # for each player in the group
        for player in pair:
            # get id
            pairing.append(player[0])
            # get name
            pairing.append(player[1])
        # add the player to new list
        matched_pair.append(pairing)
    return matched_pair

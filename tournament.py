#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

from itertools import izip
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches");
    db.commit()
    c.close()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from users");
    db.commit()
    c.close()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select * from users");
    count = c.rowcount;
    db.commit()
    c.close()
    db.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    query = "insert into users (name) values (%s)";
    c.execute(query,(name,));
    db.commit()
    c.close()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # connect to database
    db = connect()

    # get cursor from databse
    c = db.cursor()

    # query with subquery and view (name=winners) to get list of players with win count sorted by wins
    query = """
             select temp.id,temp.name,winners.wins as wins,count(temp.winner) as matches
      from (select users.id,users.name,matches.winner as winner
      from users left join matches on users.id = matches.winner or users.id = matches.loser) as temp
      left join winners on temp.id = winners.id group by temp.id,temp.name,winners.wins order by winners.wins;
            """;

    # execute the query
    c.execute(query);

    # get results back
    standing = c.fetchall();

    # close cursor
    c.close()

    # close databse connection
    db.close()

    # return the list of players
    return standing;


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # connect to database
    db = connect()
    # get the cursor 
    c = db.cursor()
    # query to insert matches
    query = "insert into matches (winner,loser) values(%s,%s)";
    # bind values to query and execute
    c.execute(query,(winner,loser));
    # commit changes
    db.commit()
    #close cursor
    c.close()
    #close connection
    db.close()
 

# create pairs of two from single list
# stackoverflow link : http://stackoverflow.com/questions/4647050/collect-every-pair-of-elements-from-a-list-into-tuples-in-python
def split(list): 
    return zip(list[0::2], list[1::2]);

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    #get players list ordered by wins
    standing = playerStandings();
    #split list in 2 groups, 4 in each group in case of 8 players
    splitted = split(standing);
    # list to return 
    matched_pair = list()

    #loop through group of 2
    for pair in splitted:
    	# temporary list
    	pairing = list()
    	# for each player in the group
    	for player in pair:
    		#get id
    		pairing.append(player[0])
    		#get name
    		pairing.append(player[1])
    	# add the player to new list
    	matched_pair.append(pairing)

    return matched_pair;


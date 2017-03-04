# tournament-results
full stack web developer course on udacity project

## Initialization
Log into your web server via SSH and be sure to have **Python** and **PostgreSQL** installed.

To initialize the required tables, run:

```
$ psql
```

```
$ \i tournament.sql
```

To run a suite of unit tests, quit **PostgreSQL** with `\q` and then:

```
$ python tournament_test.py
```

## Tables available

**USERS**

Includes the player's name and Auto Generated ID number.

**MATCHES**

ALL match results are recorded here with a match ID numer and the resulting winner or loser.

**winners** _(view)_

Keeps track of the number of wins for each player.


## Running a tournament

Use the available Python functions, in this recommended order, to coordinate a game:

METHOD | ACCEPTS | PURPOSE
--- | --- | ---
registerPlayer(name) | _name as string_ | Adds a player to the database to be calculated in pairings and standings.
countPlayers() | _(no input)_ | Counts all registered players.
swissPairings() | _(no input)_ | Returns a list of players grouped into pairs, arranged according to their current standings. Players are paired with those with about the same number of wins.
reportMatch(winner, loser) | _winner as string_, _loser as string_ | Records the result of any given match. 
playerStandings() | _(no input)_ | Returns the number of wins from all players. 


## Environment

Ubuntu machine using vagrant
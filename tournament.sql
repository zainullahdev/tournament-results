-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- if database exists then delete it
DROP DATABASE IF EXISTS tournament;

-- create the database
CREATE DATABASE tournament;

-- connect to the database
\c tournament;

-- CREATE players TABLE
create table players ( id serial primary key,name varchar(500));

-- CREATE MATCHES TABLE
create table matches ( id serial primary key,winner int references players(id),loser int references players(id));


-- CREATE VIEW TO RETURN Matches won count 
CREATE VIEW winners as
select players.id as id,players.name as name,count(matches.winner) as wins
      from players left join matches on players.id = matches.winner group by players.id,matches.winner;

-- CREATE VIEW TO RETURN All records from matches table 
CREATE VIEW player_records as 
select players.id,players.name,matches.winner as matches
      from players left join matches on players.id = matches.winner or players.id = matches.loser
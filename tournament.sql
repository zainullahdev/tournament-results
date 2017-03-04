-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create the database
CREATE DATABASE tournament;

-- connect to the database
\c tournament;

-- CREATE USERS TABLE
create table users ( id serial primary key,name varchar(500));

-- CREATE MATCHES TABLE
create table matches ( id serial primary key,winner int references users(id),loser int references users(id));


-- CREATE VIEW TO RETURN Matches won count 
CREATE VIEW winners as
select users.id as id,users.name as name,count(matches.winner) as wins
      from users left join matches on users.id = matches.winner group by users.id,matches.winner;


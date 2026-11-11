-- ============================================================================
-- SQLZoo JOIN exercises (source: sqlzoo.net)
-- Completed and annotated by me.
-- ============================================================================

-- Q1: Goals scored by Leandro Trossard
SELECT g.game, g.team, g.player, g.gtime
FROM goal g
WHERE g.player = 'Leandro Trossard';


-- Q2: Look up Belgium team details
SELECT t.id, t.teamname, t.coach
FROM team t
WHERE t.id = 'BEL';


-- Q3: Goals in the first 8 minutes, with the scoring team's name
SELECT g.player, g.gtime, t.teamname
FROM goal g 
JOIN team t ON g.team = t.id
WHERE g.gtime < 8;


-- Q4: Goals scored by teams managed by Sébastien
SELECT g.player, t.teamname, t.coach
FROM goal g 
JOIN team t ON g.team = t.id
WHERE t.coach LIKE 'Sébastien%';


-- Q5: Match locations for Harry Kane goals
SELECT g.player, ga.id, ga.city
FROM goal g 
JOIN game ga ON g.game = ga.id
WHERE g.player = 'Harry Edward Kane';


-- Q6: Goals scored in Vancouver (using short team code)
-- NOTE: goal.team stores the 3-letter team code (e.g., 'CAN', 'USA'). 
-- Q7 requires an extra join to the team table to retrieve full readable names like 'Canada'.
SELECT g.player, g.team
FROM goal g
JOIN game ga ON g.game = ga.id
WHERE ga.city = 'Vancouver';


-- Q7: Goals in Vancouver with full team names
SELECT g.player, t.teamname 
FROM goal g 
JOIN game ga ON g.game = ga.id 
JOIN team t ON g.team = t.id 
WHERE ga.city = 'Vancouver';


-- Q8: Teams playing on July 1st
-- EXPLANATION: Joining team ON team.id = game.team1 OR team.id = game.team2 tests 
-- each team code against both home (team1) and away (team2) columns for every game. 
-- Because every match has two distinct teams, the OR condition evaluates to TRUE 
-- twice per game, generating exactly 2 output rows per match (one for each team).
SELECT ga.city, t.teamname
FROM game ga
JOIN team t ON t.id = ga.team1 OR t.id = ga.team2
WHERE ga.played = '2026-07-01';


-- Q9: Goals scored on 2 July 2026, with the scoring team's name and the player
SELECT t.teamname, g.player 
FROM goal g 
JOIN game ga ON g.game = ga.id 
JOIN team t ON g.team = t.id 
WHERE ga.played = '2026-07-02';


-- Q10: Positions of players who scored in Mexico City
SELECT ga.played, g.player, p.pos
FROM goal g
JOIN game ga ON g.game = ga.id
JOIN player p ON g.player = p.playername
WHERE ga.city = 'Mexico City';


-- Q11: Goals scored by defenders
-- JUDGEMENT CALL (player.team vs goal.team):
-- I joined player.team to team.id to get the scorer's home country/club team rather 
-- than goal.team. While goal.team records the side credited with the goal, an own-goal 
-- credits goal.team to the opposing team. Linking via player.team ensures we display 
-- the defender's actual national squad.
SELECT g.player, t.teamname
FROM goal g
JOIN player p ON g.player = p.playername
JOIN team t ON p.team = t.id
WHERE p.pos = 'DEF';


-- Q12: Extra-time goals (91–120 minutes) with match details
-- JUDGEMENT CALL (player.team vs goal.team):
-- I linked team via player.team to represent the player's true team identity regardless 
-- of whether a late extra-time goal was an own goal credited to the opposing side.
SELECT g.player, p.pos, t.teamname, ga.city
FROM goal g
JOIN player p ON g.player = p.playername
JOIN team t ON p.team = t.id
JOIN game ga ON g.game = ga.id
WHERE g.gtime BETWEEN 91 AND 120;
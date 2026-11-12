-- SQLBolt exercise answers (lessons 1-12). Source: sqlbolt.com. Written by me; queries typed and tested in the browser.


-- ------------------------------------------
-- Exercise 1 — Tasks (SELECT Queries 101)
-- ------------------------------------------

-- 1. Find the title of each film
SELECT title FROM movies;

-- 2. Find the director of each film
SELECT director FROM movies;

-- 3. Find the title and director of each film
SELECT title, director FROM movies;

-- 4. Find the title and year of each film
SELECT title, year FROM movies;

-- 5. Find all the information about each film
SELECT * FROM movies;


-- ------------------------------------------
-- Exercise 2 — Tasks (Queries with Constraints Part 1)
-- ------------------------------------------

-- 1. Find the movie with a row id of 6
SELECT * FROM movies WHERE id = 6;

-- 2. Find the movies released in the years between 2000 and 2010
SELECT * FROM movies WHERE year BETWEEN 2000 AND 2010;

-- 3. Find the movies not released in the years between 2000 and 2010
SELECT * FROM movies WHERE year NOT BETWEEN 2000 AND 2010;

-- 4. Find the first 5 Pixar movies and their release year
SELECT title, year FROM movies WHERE id <= 5;


-- ------------------------------------------
-- Exercise 3 — Tasks (Queries with Constraints Part 2)
-- ------------------------------------------

-- 1. Find all the Toy Story movies
SELECT * FROM movies WHERE title LIKE 'Toy Story%';

-- 2. Find all the movies directed by John Lasseter
SELECT * FROM movies WHERE director = 'John Lasseter';

-- 3. Find all the movies (and director) not directed by John Lasseter
SELECT title, director FROM movies WHERE director != 'John Lasseter';

-- 4. Find all the WALL-* movies
SELECT * FROM movies WHERE title LIKE 'WALL-%';


-- ------------------------------------------
-- Exercise 4 — Tasks (Filtering and Sorting Query Results)
-- ------------------------------------------

-- 1. List all directors of Pixar movies (alphabetically), without duplicates
SELECT DISTINCT director 
FROM movies 
ORDER BY director ASC;

-- 2. List the last four Pixar movies released (ordered from most recent to least)
SELECT title 
FROM movies 
ORDER BY year DESC 
LIMIT 4;

-- 3. List the first five Pixar movies sorted alphabetically
SELECT title 
FROM movies 
ORDER BY title ASC 
LIMIT 5;

-- 4. List the next five Pixar movies sorted alphabetically
SELECT title 
FROM movies 
ORDER BY title ASC 
LIMIT 5 OFFSET 5;


-- ------------------------------------------
-- Exercise 5 — Tasks (Simple SELECT Queries Review - North American Cities)
-- ------------------------------------------

-- 1. List all the Canadian cities and their populations
SELECT city, population 
FROM north_american_cities 
WHERE country = 'Canada';

-- 2. Order all the cities in the United States by their latitude from north to south
SELECT city, latitude 
FROM north_american_cities 
WHERE country = 'United States' 
ORDER BY latitude DESC;

-- 3. List all the cities west of Chicago, ordered from west to east
SELECT city 
FROM north_american_cities 
WHERE longitude < (SELECT longitude FROM north_american_cities WHERE city = 'Chicago') 
ORDER BY longitude ASC;

-- 4. List the two largest cities in Mexico (by population)
SELECT city, population 
FROM north_american_cities 
WHERE country = 'Mexico' 
ORDER BY population DESC 
LIMIT 2;

-- 5. List the third and fourth largest cities (by population) in the United States and their population
SELECT city, population 
FROM north_american_cities 
WHERE country = 'United States' 
ORDER BY population DESC 
LIMIT 2 OFFSET 2;


-- ------------------------------------------
-- Exercise 6 — Tasks (Multi-table Queries with JOINs)
-- ------------------------------------------

-- 1. Find the domestic and international sales for each movie
SELECT title, domestic_sales, international_sales
FROM movies
INNER JOIN boxoffice 
  ON movies.id = boxoffice.movie_id;

-- 2. Show the sales numbers for each movie that did better internationally rather than domestically
SELECT title, domestic_sales, international_sales
FROM movies
INNER JOIN boxoffice 
  ON movies.id = boxoffice.movie_id
WHERE international_sales > domestic_sales;

-- 3. List all the movies by their ratings in descending order
SELECT title, rating
FROM movies
INNER JOIN boxoffice 
  ON movies.id = boxoffice.movie_id
ORDER BY rating DESC;


-- ------------------------------------------
-- Exercise 7 — Tasks (OUTER JOINs)
-- ------------------------------------------

-- 1. Find the list of all buildings that have employees
SELECT DISTINCT building 
FROM employees;

-- 2. Find the list of all buildings and their capacity
SELECT building_name, capacity 
FROM buildings;

-- 3. List all buildings and the distinct employee roles in each building (including empty buildings)
SELECT DISTINCT building_name, role 
FROM buildings 
LEFT JOIN employees 
  ON building_name = building;


-- ------------------------------------------
-- Exercise 8 — Tasks (A short note on NULLs)
-- ------------------------------------------

-- 1. Find the name and role of all employees who have not been assigned to a building
SELECT name, role 
FROM employees 
WHERE building IS NULL;

-- 2. Find the names of the buildings that hold no employees
SELECT building_name 
FROM buildings 
LEFT JOIN employees 
  ON building_name = building 
WHERE building IS NULL;


-- ------------------------------------------
-- Exercise 9 — Tasks (Queries with expressions)
-- ------------------------------------------

-- 1. List all movies and their combined sales in millions of dollars
SELECT title, (domestic_sales + international_sales) / 1000000.0 AS combined_sales_millions
FROM movies
INNER JOIN boxoffice 
  ON movies.id = boxoffice.movie_id;

-- 2. List all movies and their ratings in percent
SELECT title, rating * 10 AS rating_percent
FROM movies
INNER JOIN boxoffice 
  ON movies.id = boxoffice.movie_id;

-- 3. List all movies that were released on even number years
SELECT title, year 
FROM movies 
WHERE year % 2 = 0;


-- ------------------------------------------
-- Exercise 10 — Tasks (Queries with aggregates - Part 1)
-- ------------------------------------------

-- 1. Find the longest time that an employee has been at the studio
SELECT MAX(years_employed) AS longest_tenure 
FROM employees;

-- 2. For each role, find the average number of years employed by employees in that role
SELECT role, AVG(years_employed) AS average_years 
FROM employees 
GROUP BY role;

-- 3. Find the total number of employee years worked in each building
SELECT building, SUM(years_employed) AS total_years 
FROM employees 
GROUP BY building;


-- ------------------------------------------
-- Exercise 11 — Tasks (Queries with aggregates - Part 2)
-- ------------------------------------------

-- 1. Find the number of Artists in the studio (without a HAVING clause)
SELECT COUNT(*) AS total_artists 
FROM employees 
WHERE role = 'Artist';

-- 2. Find the number of Employees of each role in the studio
SELECT role, COUNT(*) AS employee_count 
FROM employees 
GROUP BY role;

-- 3. Find the total number of years employed by all Engineers
SELECT SUM(years_employed) AS total_engineer_years 
FROM employees 
WHERE role = 'Engineer';


-- ------------------------------------------
-- Exercise 12 — Tasks (Order of execution / Grouping with Joins)
-- ------------------------------------------

-- 1. Find the number of movies each director has directed
SELECT director, COUNT(*) AS movie_count 
FROM movies 
GROUP BY director;

-- 2. Find the total domestic and international sales that can be attributed to each director (total sales per director)
SELECT 
    director, 
    SUM(domestic_sales + international_sales) AS total_sales
FROM movies
INNER JOIN boxoffice 
    ON movies.id = boxoffice.movie_id
GROUP BY director;

-- ------------------------------------------
-- Bonus: HAVING and order of execution
-- ------------------------------------------

-- Roles with more than 2 employees (WHERE filters rows before grouping, HAVING filters groups after)
SELECT role, COUNT(*) AS employee_count
FROM employees
GROUP BY role
HAVING COUNT(*) > 2;

-- Order of execution, in my own words:
-- FROM / JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
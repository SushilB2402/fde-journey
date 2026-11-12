-- ============================================================================
-- SQLZoo SUM and COUNT exercises (source: sqlzoo.net). Written by me.
-- ============================================================================
-- NOTE ON NULLs:
-- - SUM() ignores NULL values in calculations.
-- - COUNT(name) counts only non-NULL entries in the specified column.
-- - COUNT(*) counts all rows regardless of NULL values.
-- ============================================================================

-- Q1: Total world population
SELECT SUM(w.population)
FROM world w;


-- Q2: List of continents
SELECT DISTINCT w.continent
FROM world w;


-- Q3: GDP of Africa
SELECT SUM(w.gdp)
FROM world w
WHERE w.continent = 'Africa';


-- Q4: Count the big countries
SELECT COUNT(w.name)
FROM world w
WHERE w.area >= 1000000;


-- Q5: Baltic states population
SELECT SUM(w.population)
FROM world w
WHERE w.name IN ('Estonia', 'Latvia', 'Lithuania');


-- Q6: Counting the countries of each continent
SELECT w.continent, COUNT(w.name) AS country_count
FROM world w
GROUP BY w.continent;


-- Q7: Counting big countries in each continent
SELECT w.continent, COUNT(w.name) AS big_country_count
FROM world w
WHERE w.population >= 10000000
GROUP BY w.continent;


-- Q8: Counting big continents
SELECT w.continent
FROM world w
GROUP BY w.continent
HAVING SUM(w.population) >= 100000000;
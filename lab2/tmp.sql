DROP TABLE IF EXISTS JOHNS;
DROP VIEW IF EXISTS AverageHeightWeight, AverageHeight;

/*QUESTION 0
EXAMPLE QUESTION
What is the highest salary in baseball history?
*/

SELECT MAX(salary) as Max_Salary
From Salaries;


/*QUESTION 1
Select the first name, last name, and given name of players who are taller than 6 ft
[hint]: Use "People"
*/
# the statistics of height in table people based on inches

SELECT nameFirst, nameLast, nameGiven, height from people 
Where height/12 > 6;

/*QUESTION 2
Create a Table of all the distinct players with a first name of John who were born in the United States and
played at Fordham university
Include their first name, last name, playerID, and birth state
[hint] Use a Join between People and CollegePlaying
*/
# schoolID == fordham

CREATE Table JOHNS as 
(SELECT distinct People.nameFirst, People.nameLast, People.playerID, People.birthState 
from  People JOIN collegeplaying ON People.playerID = collegeplaying.playerID
where People.nameFirst = 'John' and People.birthCountry = 'USA' and collegeplaying.schoolID = 'fordham');


/*QUESTION 3
Delete all Johns from the above table whose total career runs batted in is less than 2
[hint] use a subquery to select these johns from people by playerid
[hint] you may have to set sql_safe_updates = 1 to delete without a key
*/
# notes: the total career runs corresponding to the attribute

SET SQL_SAFE_UPDATES = 0;
Delete From JOHNS
WHERE EXISTS(
SELECT People.playerID
	FROM People join Batting
    ON People.playerID = Batting.playerID
    WHERE Batting.R < 2
    AND JOHNS.playerID = People.playerID
);
SET SQL_SAFE_UPDATES = 1;


/*QUESTION 4
Group together players with the same birth year, and report the year, 
 the number of players in the year, and average height for the year
 Order the resulting by year in descending order. Put this in a view
 [hint] height will be NULL for some of these years
*/

CREATE VIEW AverageHeight(birth_year, number_of_players, average_height)
AS
  (SELECT birthYear, Count(playerID), AVG(height) 
  FROM people 
  where height is not null 
  group by birthYear
  order by birthYear DESC);



/*QUESTION 5
Using Question 3, only include groups with an average weight >180 lbs,
also return the average weight of the group. This time, order by ascending
*/
# here providing two solutions
# solution1 by having clause
# solution2 by using join and nested subqueries: maybe more suitable to the question
# solution 1: using having clause

CREATE VIEW AverageHeightWeight(birth_year,number_of_players, avg_height, avg_weight)
AS
  (SELECT birthYear, Count(playerID) as number_of_players, AVG(height) as avg_height, AVG(weight) as avg_weight 
  FROM people 
  where height is not null 
  group by birthYear
  HAVING avg_weight > 180
  order by birthYear ASC)
;

#solution 2: using join and nested subqueries

CREATE VIEW AverageHeightWeight(birth_year,number_of_players, avg_height, avg_weight)
AS
	SELECT avg_weight_group.birthYear, number_of_players, average_height, avg_weight
    FROM
		(SELECT birthYear, AVG(weight) as avg_weight from people
		group by birthYear
		) as avg_weight_group JOIN AverageHeight ON avg_weight_group.birthYear = AverageHeight.birth_year
        where avg_weight_group.avg_weight > 180
        order by birthYear ASC
;

#select * from AverageHeightWeight;
#select * from schools where state = 'NY';


/*QUESTION 6
Find the players who made it into the hall of fame who played for a college located in NY
return the player ID, first name, last name, and school ID. Order the players by School alphabetically.
Update all entries with full name Columbia University to 'Columbia University!' in the schools table
*/
# solution 1: nested subqueries
# for eliminating the duplicate records, use distinct. However, if it is inconsistent with the question, it could be removed
# appreciate if you can consider this

select distinct(people.playerID),nameFirst, nameLast, schoolID
from people join 
	(select halloffame.playerID as playerID, schoolID 
	from halloffame join 
		(select collegeplaying.playerID as playerID, schools.schoolID as schoolID, schools.state as state
		from collegeplaying join schools on collegeplaying.schoolID = schools.schoolID
		where schools.state = 'NY') collegeplaying_school on halloffame.playerID = collegeplaying_school.playerID) collegeplaying_halloffame_school
    on people.playerID = collegeplaying_halloffame_school.playerID
    order by schoolID
;

#Update all entries with full name Columbia University to 'Columbia University!' in the schools table
SET SQL_SAFE_UPDATES = 0;
UPDATE Schools set name_full = 'Columbia University!' where name_full = 'Columbia University';
SET SQL_SAFE_UPDATES = 1;





/*QUESTION 7
Find the team id, yearid and average HBP for each team using a subquery.
Limit the total number of entries returned to 100
group the entries by team and year and order by descending values
[hint] be careful to only include entries where AB is > 0
*/

# solution 1: subquery
select teamID, yearID , avg(HBP) as avg_HBP
FROM
	(select teamID, yearID, HBP
    from teams
    where AB > 0 ) as teams_temp
group by teamID, yearID
order by avg_HBP DESC
limit 100;
















































































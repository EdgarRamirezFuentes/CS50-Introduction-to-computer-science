SELECT DISTINCT(people.name) FROM stars
INNER JOIN people
ON people.id = stars.person_id
INNER JOIN movies
ON movies.year = 2004 AND movies.id = stars.movie_id
ORDER BY people.birth;
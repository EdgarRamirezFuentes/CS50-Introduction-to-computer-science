SELECT movies.title FROM stars
INNER JOIN people
ON people.id = stars.person_id AND people.name = "Johnny Depp"
INNER JOIN movies
ON movies.id = stars.movie_id

INTERSECT

SELECT movies.title FROM stars
INNER JOIN people
ON people.id = stars.person_id AND name = "Helena Bonham Carter"
INNER JOIN movies
ON movies.id = stars.movie_id
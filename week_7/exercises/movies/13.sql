SELECT people.name FROM stars
INNER JOIN people
ON people.id = stars.person_id
WHERE stars.movie_id IN (
    SELECT movies.id FROM stars
    INNER JOIN people
    ON people.id = stars.person_id AND people.name = "Kevin Bacon" AND people.birth = 1958
    INNER JOIN movies
    ON movies.id = stars.movie_id
) AND people.name != "Kevin Bacon";

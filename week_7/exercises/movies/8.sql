SELECT people.name FROM stars
INNER JOIN people
ON stars.person_id = people.id
INNER JOIN movies
ON movies.title = "Toy Story" AND movies.id = stars.movie_id;
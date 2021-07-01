SELECT DISTINCT(people.name) FROM directors
INNER JOIN ratings
ON ratings.movie_id = directors.movie_id AND ratings.rating >= 9.0
INNER JOIN people
ON people.id = directors.person_id;

SELECT AVG(ratings.rating) FROM ratings
INNER JOIN movies
ON movies.id = ratings.movie_id AND movies.year = 2012;
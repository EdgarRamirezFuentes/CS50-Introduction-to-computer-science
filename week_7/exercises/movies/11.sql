SELECT movies.title
FROM stars
    INNER JOIN ratings
    ON ratings.movie_id = stars.movie_id
    INNER JOIN people
    ON people.id = stars.person_id AND people.name = "Chadwick Boseman"
    INNER JOIN movies
    ON movies.id = stars.movie_id
ORDER BY ratings.rating DESC LIMIT 5;
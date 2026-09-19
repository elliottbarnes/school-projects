Assignment 3

1.

SELECT LastName, City, Phone, Country
FROM customers
WHERE Country = 'Brazil';

2. 

SELECT max(CustomerID), City 
FROM Customers 
GROUP BY City;

3.

SELECT CustomerID, LastName, Country
FROM customers
ORDER BY LastName asc
LIMIT 40;

4.

SELECT CustomerId, LastName, Email, Company
From customers
Where Company IS NULL;

5. 

SELECT CustomerId, LastName, Email
FROM customers
WHERE Email LIKE '%@hotmail.com%';

6. 

SELECT title, COUNT(TrackId) AS numberOfTracks
FROM albums 
INNER JOIN tracks ON tracks.AlbumId = albums.AlbumId
GROUP BY title
HAVING COUNT(TrackId)>15
ORDER BY count(TrackId) desc;



7. 

SELECT max(milliseconds)
FROM tracks;

8. 

SELECT FirstName, LastName, HireDate
FROM employees
WHERE HireDate LIKE '%1973%';

9.

SELECT genres.Name, COUNT(TrackId) as TracksInGenre
FROM genres
INNER JOIN tracks ON tracks.GenreId = genres.GenreId
GROUP BY genres.Name
ORDER BY COUNT(TrackId) desc;

10.

SELECT CustomerId, customers.LastName, customers.FirstName, customers.Email, employees.LastName AS supportRepLastName
FROM customers
INNER JOIN employees ON employees.employeeid = customers.supportRepId
WHERE customers.country like '%Canada%';
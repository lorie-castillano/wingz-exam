# Wingz

A rideshare app focused on Non-Emergency Medical Transportation (NEMT).

## Description

This project is a booking application for a ride. This includes booking for a ride and tracking the booking status.

## Getting Started

### Dependencies

- Install Docker
- Install Postman

### Installing

- Clone this repository:

```
git clone https://github.com/lorie-castillano/wingz-exam.git
```

### Executing program

1. After cloning the repository, get in the project folder and run docker-compose command. This will setup everything in the machine.
   ```
   cd wingz
   docker-compose up --build
   ```
2. When this line appears, `Starting development server at http://0.0.0.0:8000/`, it means the server is now ready to accept requests.
3. Import file `Wingz.postman_collection.json` in to postman. The requests in the collection are the following:
   - Login
   - Ride CRUD
   - RideEvent CRUD (Please take note the PUT method is not allowed for data integrity)
   - Ride List

## Bonus - SQL

```sql
SELECT
    DATE_TRUNC('month', ride.pickup_time) AS "Month",
    users.first_name || ' ' || users.last_name AS "Driver",
    COUNT(*) AS "'Count of Trips > 1 hr'"
FROM public.core_ride ride
JOIN public.core_user users ON users.id_user = ride.id_driver_id
JOIN public.core_rideevent pickup ON ride.id_ride = pickup.id_ride_id AND pickup.description = 'Status changed to pickup'
JOIN public.core_rideevent dropoff ON ride.id_ride = dropoff.id_ride_id AND dropoff.description = 'Status changed to dropoff'
WHERE EXTRACT(EPOCH FROM (dropoff.created_at - pickup.created_at)) > 3600
GROUP BY "Month", "Driver"
ORDER BY "Month" ASC;
```

## Notes/Comments

- The most challenging part is the sorting of Geolocation. The two ways to get this done is by using `Haversine Formula` or `PostGIS`. I ended up using [`PostGIS`](https://github.com/openwisp/django-rest-framework-gis).

- This project is dockerized for convince of the developers.

- For the `Bonus - SQL` question, I have initialized or pre-loaded the database with data and included a `pgadmin` service in docker-compose for convinient testing.

## Authors

Lorie Anne Castillano

-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Get the crime scenes reports that match with the known clue
-- Information:
    -- Hour: 10:15
    -- Three witnesses
    -- each of their interview transcripts mentions the courthouse
SELECT description FROM crime_scene_reports
WHERE year= 2020 AND month = 7 AND day = 28 AND street = "Chamberlin Street";


-- Get the interviews of the three witnesses
-- Information:
    -- Whithin 10 minutes after the theft, the thief drove away from the courthouse parking lot
    -- The thief withdrew some money at the ATM on Fifer Street
    -- The thief talked to his accomplice with for less than 1 minute
    -- The thief's accomplice bought a ticket for the earliest flight out of Fiftyville tomorrow
SELECT transcript FROM interviews
WHERE year = 2020 AND month = 7 AND day = 28 AND transcript LIKE "%courthouse%";


-- Get the useful information from the courthouse parking lot logs that are exit activities from 10:10 to 10:25
-- year | month | day | hour | minute | license_plate
-- 2020 | 7 | 28 | 10 | 16 | 5P2BI95
-- 2020 | 7 | 28 | 10 | 18 | 94KL13X
-- 2020 | 7 | 28 | 10 | 18 | 6P58WS2
-- 2020 | 7 | 28 | 10 | 19 | 4328GD8
-- 2020 | 7 | 28 | 10 | 20 | G412CB7
-- 2020 | 7 | 28 | 10 | 21 | L93JTIZ
-- 2020 | 7 | 28 | 10 | 23 | 322W7JE
-- 2020 | 7 | 28 | 10 | 23 | 0NTHK55
SELECT year, month, day, hour, minute, license_plate FROM courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 10 AND minute <= 25 AND activity = "exit";


-- Get the useful information of people who withdrew money at ATM on Fifer Street in the crime date
-- Information:
-- name | phone_number | license_plate | passport_number
-- Ernest | (367) 555-5533 | 94KL13X *| 5773159633
-- Russell | (770) 555-1861 | 322W7JE | 3592750733
-- Roy | (122) 555-4581 | QX4YZN3 | 4408372428
-- Bobby | (826) 555-1652 | 30G67EN | 9878712108
-- Elizabeth | (829) 555-5269 | L93JTIZ * | 7049073643
-- Danielle | (389) 555-5198 | 4328GD8 | 8496433585
-- Madison | (286) 555-6063 | 1106N58 | 1988161715
-- Victoria | (338) 555-6650 | 8X428L0 | 9586786673
SELECT people.name, people.phone_number, people.license_plate, people.passport_number FROM bank_accounts
    INNER JOIN people
    ON people.id = bank_accounts.person_id
    INNER JOIN atm_transactions
    ON atm_transactions.account_number = bank_accounts.account_number
    AND atm_transactions.year = 2020
    AND atm_transactions.month = 7
    AND atm_transactions.day = 28
    AND atm_transactions.atm_location = "Fifer Street"
    AND atm_transactions.transaction_type = "withdraw";


-- Get the phone calls that match the description of the witness's interview.
-- Information:
-- id | caller | receiver | year | month | day | duration
-- 221 | (130) 555-0289 | (996) 555-8899 | 2020 | 7 | 28 | 51
-- 224 | (499) 555-9472 | (892) 555-8872 | 2020 | 7 | 28 | 36
-- 233 | (367) 555-5533 | (375) 555-8161 | 2020 | 7 | 28 | 45 *
-- 251 | (499) 555-9472 | (717) 555-1342 | 2020 | 7 | 28 | 50
-- 254 | (286) 555-6063 | (676) 555-6554 | 2020 | 7 | 28 | 43
-- 255 | (770) 555-1861 | (725) 555-3243 | 2020 | 7 | 28 | 49
-- 261 | (031) 555-6622 | (910) 555-3251 | 2020 | 7 | 28 | 38
-- 279 | (826) 555-1652 | (066) 555-9701 | 2020 | 7 | 28 | 55
-- 281 | (338) 555-6650 | (704) 555-2131 | 2020 | 7 | 28 | 54
SELECT * FROM phone_calls
WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60;


-- Having this information, my conclusion is that Ernest is the thief due to He has three appearances in the queries

-- Get the person information whose phone number is (375) 555-8161
-- Information
-- id | name | phone_number | passport_number | license_plate
-- 864400 | Berthold | (375) 555-8161 |  | 4V16VO0
SELECT * FROM people WHERE phone_number = "(375) 555-8161";

--Get the Ernest information
-- Information:
-- id | name | phone_number | passport_number | license_plate
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X
SELECT * FROM people WHERE phone_number = "(367) 555-5533";


-- Get the information of the fiftyville airport
-- Information:
-- id | abbreviation | full_name | city
-- 8 | CSF | Fiftyville Regional Airport | Fiftyville
SELECT * FROM airports WHERE city = "Fiftyville";

-- Get the destination airport city using the collected information
SELECT airports.city FROM passengers
INNER JOIN flights
ON flights.id = passengers.flight_id and passengers.passport_number = "5773159633" AND flights.year = 2020 AND flights.month = 7 AND flights.day = 29 AND flights.origin_airport_id = 8
INNER JOIN airports
ON  airports.id = flights.destination_airport_id;
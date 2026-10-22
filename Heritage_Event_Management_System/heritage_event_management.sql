-- MySQL reference schema for Heritage Event Management System
CREATE DATABASE IF NOT EXISTS heritage_event_db;
USE heritage_event_db;

CREATE TABLE visitors (
  visitor_id INT PRIMARY KEY AUTO_INCREMENT,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  city VARCHAR(60)
);

CREATE TABLE events (
  event_id INT PRIMARY KEY AUTO_INCREMENT,
  event_name VARCHAR(150) NOT NULL,
  venue VARCHAR(100) NOT NULL,
  event_date DATE NOT NULL,
  event_type VARCHAR(60) NOT NULL,
  capacity INT NOT NULL
);

CREATE TABLE registrations (
  registration_id INT PRIMARY KEY AUTO_INCREMENT,
  visitor_id INT NOT NULL,
  event_id INT NOT NULL,
  registered_on DATE NOT NULL,
  attendance_status ENUM('Registered','Attended','Cancelled') DEFAULT 'Registered',
  UNIQUE(visitor_id,event_id),
  FOREIGN KEY(visitor_id) REFERENCES visitors(visitor_id),
  FOREIGN KEY(event_id) REFERENCES events(event_id)
);

-- Registration count by event
SELECT e.event_name, e.venue, COUNT(r.registration_id) AS registrations
FROM events e LEFT JOIN registrations r ON e.event_id=r.event_id
GROUP BY e.event_id, e.event_name, e.venue
ORDER BY registrations DESC;

-- Attendance rate by event
SELECT e.event_name,
       COUNT(r.registration_id) AS registration_records,
       SUM(r.attendance_status='Attended') AS attended
FROM events e LEFT JOIN registrations r ON e.event_id=r.event_id
GROUP BY e.event_id, e.event_name;

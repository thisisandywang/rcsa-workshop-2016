GRANT INSERT, SELECT, DELETE, UPDATE ON rcs.* TO 'duckie'@'localhost' IDENTIFIED BY 'password'
use rcs;
show tables;
set foreign_key_checks = 0;
drops table Student, Event, Attendees, HousePointsOther;
show tables;
set foreign_key_checks = 1;
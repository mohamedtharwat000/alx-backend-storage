-- this file contains the SQL statements to create the tables and triggers


CREATE TRIGGER  decreas_quantity
AFTER INSERT ON orders
FOR EACH ROW UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;

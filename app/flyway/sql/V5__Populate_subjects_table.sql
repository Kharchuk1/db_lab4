INSERT INTO subject(name)
SELECT ukrTest FROM zno WHERE ukrTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT histTest FROM zno WHERE histTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT mathTest FROM zno WHERE mathTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT physTest FROM zno WHERE physTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT chemTest FROM zno WHERE chemTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT bioTest FROM zno WHERE bioTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT geoTest FROM zno WHERE geoTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT engTest FROM zno WHERE engTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT fraTest FROM zno WHERE fraTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT deuTest FROM zno WHERE deuTest IS NOT NULL LIMIT 1;

INSERT INTO subject(name)
SELECT spaTest FROM zno WHERE spaTest IS NOT NULL LIMIT 1;
-- Drop tables in dependency-safe order
DROP TABLE IF EXISTS constellation CASCADE;
DROP TABLE IF EXISTS planetary_body CASCADE;
DROP TABLE IF EXISTS distance CASCADE;
DROP TABLE IF EXISTS forecast CASCADE;

-- Constellation table
CREATE TABLE constellation (
    constellation_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    constellation_name TEXT NOT NULL,
    PRIMARY KEY (constellation_id)
);

-- Planetary body table
CREATE TABLE planetary_body (
    planetary_body_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    planetary_body_name TEXT NOT NULL,
    PRIMARY KEY (planetary_body_id)
);

-- Distance table
CREATE TABLE distance (
    distance_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    kilometres FLOAT NOT NULL,
    planetary_body_id INT NOT NULL,
    PRIMARY KEY (distance_id),
    FOREIGN KEY (planetary_body_id) REFERENCES planetary_body(planetary_body_id)
);

-- Forecast table
CREATE TABLE forecast (
    forecast_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    date TIMESTAMP NOT NULL,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    planetary_body_id INT NOT NULL,
    constellation_id INT,
    right_ascension_hours FLOAT,
    right_ascension_string TEXT,
    declination_degrees FLOAT,
    declination_string TEXT,
    altitude_degrees FLOAT,
    altitude_string TEXT,
    azimuth_degrees FLOAT,
    azimuth_string TEXT,
    PRIMARY KEY (forecast_id),
    FOREIGN KEY (planetary_body_id) REFERENCES planetary_body(planetary_body_id),
    FOREIGN KEY (constellation_id) REFERENCES constellation(constellation_id)
);


------------------------------------------------------------------
------------------- INSERTING STATIC DATA ------------------------
------------------------------------------------------------------

-- Insert constellations
INSERT INTO constellation (constellation_name) VALUES
    ('Andromeda'),
    ('Antlia'),
    ('Apus'),
    ('Aquarius'),
    ('Aquila'),
    ('Ara'),
    ('Aries'),
    ('Auriga'),
    ('Boötes'),
    ('Caelum'),
    ('Camelopardalis'),
    ('Cancer'),
    ('Canes Venatici'),
    ('Canis Major'),
    ('Canis Minor'),
    ('Capricornus'),
    ('Carina'),
    ('Cassiopeia'),
    ('Centaurus'),
    ('Cepheus'),
    ('Cetus'),
    ('Chamaeleon'),
    ('Circinus'),
    ('Columba'),
    ('Coma Berenices'),
    ('Corona Australis'),
    ('Corona Borealis'),
    ('Corvus'),
    ('Crater'),
    ('Crux'),
    ('Cygnus'),
    ('Delphinus'),
    ('Dorado'),
    ('Draco'),
    ('Equuleus'),
    ('Eridanus'),
    ('Fornax'),
    ('Gemini'),
    ('Grus'),
    ('Hercules'),
    ('Horologium'),
    ('Hydra'),
    ('Hydrus'),
    ('Indus'),
    ('Lacerta'),
    ('Leo'),
    ('Leo Minor'),
    ('Lepus'),
    ('Libra'),
    ('Lupus'),
    ('Lynx'),
    ('Lyra'),
    ('Mensa'),
    ('Microscopium'),
    ('Monoceros'),
    ('Musca'),
    ('Norma'),
    ('Octans'),
    ('Ophiuchus'),
    ('Orion'),
    ('Pavo'),
    ('Pegasus'),
    ('Perseus'),
    ('Phoenix'),
    ('Pictor'),
    ('Pisces'),
    ('Piscis Austrinus'),
    ('Puppis'),
    ('Pyxis'),
    ('Reticulum'),
    ('Sagitta'),
    ('Sagittarius'),
    ('Scorpius'),
    ('Sculptor'),
    ('Scutum'),
    ('Serpens Cauda'),
    ('Sextans'),
    ('Taurus'),
    ('Telescopium'),
    ('Triangulum'),
    ('Triangulum Australe'),
    ('Tucana'),
    ('Ursa Major'),
    ('Ursa Minor'),
    ('Vela'),
    ('Virgo'),
    ('Volans'),
    ('Vulpecula')
;

-- Insert planetary bodies
INSERT INTO planetary_body (planetary_body_name) VALUES
    ('Sun'),
    ('Moon'),
    ('Mercury'),
    ('Venus'),
    ('Earth'),
    ('Mars'),
    ('Jupiter'),
    ('Saturn'),
    ('Uranus'),
    ('Neptune'),
    ('Pluto')
;

CREATE STAGE s3_stage 
URL='s3://music-de/'
CREDENTIALS = (AWS_KEY_ID ='xxxxxxxxx', AWS_SECRET_KEY='xxxxx');


CREATE OR REPLACE TABLE artists (
    id INT AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(500),
    playcount int,
    listeners int,
    mbid VARCHAR(500),
    url VARCHAR(1000),
    streamable int,
    image VARCHAR(5000)
);

-- name,duration,playcount,listeners,mbid,url,image,streamable.#text,streamable.fulltrack,artist.name,artist.mbid,artist.url

CREATE OR REPLACE TABLE tracks(
    id INT AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(500),
    duration INT,
    playcount INT,
    listeners INT,
    mbid VARCHAR(500),
    url VARCHAR(1000),
    image VARCHAR(5000),
    streamable_text INT,
    streamable_fulltrack INT,
    artist_name VARCHAR(500),
    artist_mbid VARCHAR(500),
    artist_url VARCHAR(1000)
);

COPY INTO artists (name, playcount, listeners, mbid, url, streamable, image)
FROM @s3_stage
PATTERN = '.*artists.*[.]csv'
FILE_FORMAT = (TYPE ='CSV', SKIP_HEADER = 1, FIELD_OPTIONALLY_ENCLOSED_BY = '"')
TRUNCATECOLUMNS = TRUE
ON_ERROR = 'CONTINUE';

COPY INTO tracks (name, duration, playcount, listeners, mbid, url, image, streamable_text, streamable_fulltrack, artist_name, artist_mbid, artist_url)
FROM @s3_stage
PATTERN = '.*tracks.*[.]csv'
FILE_FORMAT = (TYPE ='CSV', SKIP_HEADER = 1, FIELD_OPTIONALLY_ENCLOSED_BY = '"')
TRUNCATECOLUMNS = TRUE
ON_ERROR = 'CONTINUE';
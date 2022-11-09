DROP DATABASE IF EXISTS lyrical;
CREATE DATABASE IF NOT EXISTS lyrical;

USE lyrical;

CREATE TABLE IF NOT EXISTS user (
    user_id         INT         NOT NULL    AUTO_INCREMENT,
    user_name	    VARCHAR(32) NOT NULL UNIQUE,
    user_password	VARCHAR(64)   NOT NULL,
    create_time	    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS audio_input (
    audio_id	    INT             NOT NULL    AUTO_INCREMENT,
    audio_file_name	VARCHAR(128)    NOT NULL,
    status	        INT             NOT NULL,
    user_id	        INT             NOT NULL,
    create_time	    TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (audio_id)
);

CREATE TABLE IF NOT EXISTS music_video (
    music_video_id	        INT             NOT NULL    AUTO_INCREMENT,
    music_video_file_name	VARCHAR(128)    NOT NULL,
    audio_id	            INT             NOT NULL,
    user_id	                INT             NOT NULL,
    create_time	            TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (music_video_id)
);
CREATE DATABASE IF NOT EXISTS lyrical;

USE lyrical;

CREATE TABLE IF NOT EXISTS user (
    user_id         INT         NOT NULL    AUTO_INCREMENT,
    user_name	    VARCHAR(32) NOT NULL,
    user_password	VARCHAR(64)   NOT NULL,
    create_time	    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS audio_input (
    audio_id	    INT             NOT NULL    AUTO_INCREMENT,
    audio_directory	VARCHAR(128)    NOT NULL,
    audio_file_name	VARCHAR(128)    NOT NULL,
    status	        INT             NOT NULL,
    user_id	        INT             NOT NULL,
    create_time	    TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (audio_id)
);

CREATE TABLE IF NOT EXISTS music_video (
    music_video_id	        INT             NOT NULL    AUTO_INCREMENT,
    music_video_directory	VARCHAR(128)    NOT NULL,
    music_video_file_name	VARCHAR(128)    NOT NULL,
    audio_id	            INT             NOT NULL,
    user_id	                INT             NOT NULL,
    format                  VARCHAR(16)     NOT NULL,
    create_time	            TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (music_video_id)
);
DROP TABLE IF EXISTS cracked_password;

CREATE TABLE cracked_password (
  md5_checksum TEXT PRIMARY KEY NOT NULL,
  filename TEXT NOT NULL,
  password TEXT NOT NULL
);
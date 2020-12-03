-- Create an accounts table
CREATE TABLE IF NOT EXISTS accounts (
  id        INT PRIMARY KEY NOT NULL,
  balance   INT NOT NULL DEFAULT 0
);

-- Create an accounts table
CREATE TABLE IF NOT EXISTS transactions (
  id        SERIAL PRIMARY KEY,
  id_from   INT NOT NULL,
  id_to     INT NOT NULL,
  amount    INT NOT NULL DEFAULT 0,
  datetime  timestamp NOT NULL
);

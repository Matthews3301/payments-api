-- Add some test accounts
INSERT INTO accounts (id, balance, locked) VALUES
(1, 123, FALSE),
(2, 234, FALSE);
-- And transactions
INSERT INTO transactions (id, id_from, id_to, amount, datetime) VALUES
(DEFAULT, 1, 2, 4, '2020-06-11 21:02:43'),
(DEFAULT, 2, 1, 2, '2020-01-08 04:05:06');
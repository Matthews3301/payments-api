-- Add some test accounts
INSERT INTO accounts (id, balance) VALUES
(1, 123),
(2, 234);
-- And transactions
INSERT INTO transactions (id, id_from, id_to, amount, datetime) VALUES
(1, 1, 2, 4, '2020-06-11 21:02:43'),
(2, 2, 1, 2, '2020-01-08 04:05:06');
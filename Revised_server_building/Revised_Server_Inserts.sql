-- Priorities
INSERT INTO Priorities (NAME) VALUES
('Critical'),
('High'),
('Medium'),
('Low');

-- Purposes
INSERT INTO Purposes (NAME) VALUES
('Daily Spending'),
('Emergency Fund'),
('Savings'),
('Travel'),
('Investments'),
('Education'),
('Bills'),
('Business'),
('Retirement'),
('Entertainment');

-- SavingGoals
INSERT INTO SavingGoals (NAME) VALUES
('New Car'),
('House Down Payment'),
('Vacation'),
('Emergency Fund'),
('Laptop'),
('Wedding'),
('University Tuition'),
('Investment Portfolio'),
('Motorcycle'),
('Home Renovation');

-- Directions
INSERT INTO Direction ([TYPE]) VALUES
('Income'),
('Expense');

-- Frequencies
INSERT INTO Frequencies (NAME) VALUES
('Daily'),
('Weekly'),
('Biweekly'),
('Monthly'),
('Quarterly'),
('Semiannual'),
('Annual');

-- Currency
INSERT INTO Currency (NAME) VALUES
('USD'),
('EUR'),
('RON'),
('GBP'),
('JPY'),
('CHF'),
('CAD'),
('AUD'),
('SEK'),
('HUF');

-- Categories
INSERT INTO Categories (NAME, PRIORITY_ID, DESCRIPTION) VALUES
('Housing',1,'Rent and utilities'),
('Food',1,'Groceries and dining'),
('Transportation',2,'Travel and fuel'),
('Healthcare',1,'Medical expenses'),
('Education',2,'Courses and books'),
('Entertainment',4,'Fun activities'),
('Savings',1,'Money set aside'),
('Investments',2,'Stocks and funds'),
('Personal Care',3,'Self care'),
('Utilities',1,'Electricity and internet');

-- Subcategories
INSERT INTO Subcategories (CATEGORY_ID, NAME) VALUES
(1,'Rent'),
(1,'Utilities'),
(2,'Groceries'),
(2,'Restaurants'),
(3,'Fuel'),
(3,'Public Transport'),
(4,'Medicine'),
(5,'Books'),
(6,'Movies'),
(7,'Emergency Savings');

-- Accounts
INSERT INTO Accounts (PURPOSE_ID, CURRENCY_ID, BALANCE, USER_ID) VALUES
(1, 3, 5000.00, 31),
(2, 3, 12000.00, 32),
(3, 1, 2500.00, 33),
(4, 2, 3200.00, 34),
(5, 1, 15000.00, 35),
(6, 2, 4200.00, 36),
(7, 3, 1800.00, 37),
(8, 1, 7500.00, 38),
(9, 2, 22000.00, 39),
(10, 3, 6000.00, 40);
GO


-- SavingPlans
INSERT INTO SavingPlans (YIELD, BUDGET, ACCOUNT_ID, SAVING_GOAL_ID) VALUES
(3.50, 5000.00, 5, 1),
(4.00, 8000.00, 6, 2),
(2.50, 2000.00, 7, 3),
(3.75, 10000.00, 8, 4),
(5.00, 3000.00, 9, 5),
(4.20, 7000.00, 10, 6),
(3.10, 4000.00, 11, 7),
(4.50, 9000.00, 12, 8),
(5.20, 6000.00, 13, 9),
(3.80, 5000.00, 14, 10);

-- Budgets
INSERT INTO Budgets (BALANCE, CATEGORY_ID, PERIOD_BEGIN, ACCOUNT_ID, PERIOD_END) VALUES
(1000.00, 1, '2026-01-01', 5, '2026-01-31'),
(800.00, 2, '2026-01-01', 6, '2026-01-31'),
(300.00, 3, '2026-01-01', 7, '2026-01-31'),
(200.00, 4, '2026-01-01', 8, '2026-01-31'),
(500.00, 5, '2026-01-01', 9, '2026-01-31'),
(250.00, 6, '2026-01-01', 10, '2026-01-31'),
(700.00, 7, '2026-01-01', 11, '2026-01-31'),
(900.00, 8, '2026-01-01', 12, '2026-01-31'),
(350.00, 9, '2026-01-01', 13, '2026-01-31'),
(400.00, 10, '2026-01-01', 14, '2026-01-31');

-- Loans
INSERT INTO Loans (INTEREST, VALUE, ACCOUNT_ID) VALUES
(5.50, 10000.00, 5),
(4.75, 20000.00, 6),
(6.10, 15000.00, 7),
(3.90, 25000.00, 8),
(5.00, 12000.00, 9),
(4.20, 8000.00, 10),
(6.50, 18000.00, 11),
(3.75, 30000.00, 12),
(4.90, 22000.00, 13),
(5.80, 14000.00, 14);
GO

-- RecurringPayments
INSERT INTO RecurringPayments (COMPANY_NAME, PRICE, SUBCATEGORY_ID, DUE_DATE, ACCOUNT_ID, FREQUENCY_ID, CURRENCY_ID) VALUES
('Netflix', 15.99, 9, '2026-06-01', 5, 4, 1),
('Spotify', 9.99, 9, '2026-06-05', 6, 4, 1),
('Electric Company', 120.50, 2, '2026-06-10', 7, 4, 3),
('Water Utility', 45.25, 2, '2026-06-12', 8, 4, 3),
('Internet Provider', 30.00, 2, '2026-06-15', 9, 4, 2),
('Gym Membership', 50.00, 9, '2026-06-18', 10, 4, 2),
('Cloud Storage', 4.99, 9, '2026-06-20', 11, 4, 1),
('Mobile Carrier', 25.00, 2, '2026-06-22', 12, 4, 1),
('Magazine Subscription', 12.50, 8, '2026-06-25', 13, 4, 1),
('Music Service', 7.99, 9, '2026-06-28', 14, 4, 1);

-- Transactions
INSERT INTO Transactions (TRANSACTION_TIME, SUBCATEGORY_ID, ACCOUNT_ID, DIRECTION_ID, AMOUNT, DESCRIPTION) VALUES
('2026-01-01 09:00:00', NULL, 5, 1, 3000.00, 'Salary'),
('2026-01-02 12:00:00', 3, 5, 2, -120.50, 'Groceries'),
('2026-01-03 08:00:00', 5, 6, 2, -60.00, 'Fuel'),
('2026-01-04 18:00:00', 4, 7, 2, -45.90, 'Restaurant'),
('2026-01-05 10:00:00', NULL, 8, 1, 2500.00, 'Freelance Work'),
('2026-01-06 11:00:00', 7, 9, 2, -30.00, 'Medicine'),
('2026-01-07 14:00:00', 8, 10, 2, -80.00, 'Books'),
('2026-01-08 17:00:00', 9, 11, 2, -20.00, 'Movie Ticket'),
('2026-01-09 09:00:00', NULL, 12, 1, 2800.00, 'Salary'),
('2026-01-10 13:00:00', 10, 13, 2, -500.00, 'Savings Deposit');
GO

INSERT INTO Budget_Transactions (BUDGET_ID, TRANSACTION_ID) VALUES
(9, 12),
(10, 13),
(10, 14),
(11, 15),
(12, 16),
(13, 17);
GO
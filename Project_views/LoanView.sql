CREATE VIEW LoanView
AS
SELECT [Loans].[INTEREST], [Loans].[VALUE], [Currency].[NAME],[Users].[EMAIL] FROM [Loans]
LEFT JOIN Accounts ON
[Loans].[ACCOUNT_ID] = [Accounts].[ACCOUNT_ID]
LEFT JOIN Users ON 
[Accounts].[USER_ID] = [Users].[USER_ID]
JOIN Currency ON
[Accounts].[CURRENCY_ID] = [Currency].[CURRENCY_ID]
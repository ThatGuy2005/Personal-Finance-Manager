CREATE VIEW TransactionView
AS
SELECT [Transactions].[TRANSACTION_TIME], 
ISNULL([Subcategories].[NAME],'Unknown') AS SUB_CAT, [Transactions].[AMOUNT],
[Direction].[TYPE], [Transactions].[DESCRIPTION], [Users].[EMAIL], [Currency].[NAME] FROM [Transactions]
LEFT JOIN [Subcategories] ON
[Transactions].[SUBCATEGORY_ID] = [Subcategories].[SUBCATEGORY_ID]
LEFT JOIN [Direction] ON
[Transactions].[DIRECTION_ID] = [Direction].[DIRECTION_ID]
JOIN [Accounts] ON
[Transactions].[ACCOUNT_ID] = [Accounts].[ACCOUNT_ID]
JOIN [Users] ON
[Accounts].[USER_ID] = [Users].[USER_ID]
JOIN [Currency] ON
[Accounts].[CURRENCY_ID] = [Currency].[CURRENCY_ID]
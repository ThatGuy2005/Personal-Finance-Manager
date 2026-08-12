CREATE VIEW BudgetView
AS
SELECT [Budgets].[BALANCE], [Budgets].[PERIOD_BEGIN],
[Budgets].[PERIOD_END], [Categories].[NAME] AS CategoryName, [Currency].[NAME], [Users].[EMAIL] FROM Budgets
LEFT JOIN Categories ON
[Budgets].[CATEGORY_ID] = [Categories].[CATEGORY_ID]
JOIN Accounts ON
[Budgets].[ACCOUNT_ID] = [Accounts].[ACCOUNT_ID]
JOIN Currency ON
[Accounts].[CURRENCY_ID] = [Currency].[CURRENCY_ID]
RIGHT JOIN Users ON
[Users].[USER_ID] = [Accounts].[USER_ID]

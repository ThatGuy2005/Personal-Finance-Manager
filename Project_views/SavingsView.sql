CREATE VIEW SavingsView
AS
SELECT [SavingPlans].[YIELD],[SavingPlans].[BUDGET],
[Currency].[NAME] AS CurrencyName, [SavingGoals].[NAME] AS SavingGoalName, [Users].[EMAIL] FROM [SavingPlans]
JOIN Accounts ON
[SavingPlans].[ACCOUNT_ID] = [Accounts].[ACCOUNT_ID]
JOIN Currency ON
[Accounts].[CURRENCY_ID] = [Currency].[CURRENCY_ID]
LEFT JOIN SavingGoals ON
[SavingPlans].[SAVING_GOAL_ID] = [SavingGoals].[SAVING_GOAL_ID]
RIGHT JOIN [Users] ON
[Accounts].[USER_ID] = [Users].[USER_ID]
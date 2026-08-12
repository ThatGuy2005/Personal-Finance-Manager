CREATE VIEW UserRecurringPayments
AS
SELECT [RecurringPayments].[RECURRING_PAYMENT_ID],[Users].[EMAIL], [Users].[NAME] AS UserName, [RecurringPayments].[COMPANY_NAME],
[RecurringPayments].[DUE_DATE], [RecurringPayments].[PRICE],
[Currency].[NAME], [Frequencies].[NAME] AS FREQ, [Subcategories].[NAME] AS SUB_CAT
FROM [RecurringPayments]
JOIN [Currency] ON
[RecurringPayments].[CURRENCY_ID] = [Currency].[CURRENCY_ID]
JOIN [Frequencies] ON
[RecurringPayments].[FREQUENCY_ID] = [Frequencies].[FREQUENCY_ID]
JOIN [Accounts] ON
[RecurringPayments].[ACCOUNT_ID] = [Accounts].[ACCOUNT_ID]
JOIN [Users] ON
[Users].[USER_ID] = [Accounts].[USER_ID]
LEFT JOIN [Subcategories] ON
[RecurringPayments].[SUBCATEGORY_ID] = [Subcategories].[SUBCATEGORY_ID]
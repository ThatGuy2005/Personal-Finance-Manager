-- ================================================
-- Template generated from Template Explorer using:
-- Create Procedure (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- This block of comments will not be included in
-- the definition of the procedure.
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Csongor Tamás>
-- Create date: <6/5/2026>
-- Description:	<Gets the savings of an account.>
-- =============================================
CREATE PROCEDURE GetSavings
	-- Add the parameters for the stored procedure here
	@EMAIL VARCHAR(255)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
	SELECT [YIELD],[BUDGET],
		[CURRENCYNAME] AS CURRENCY_NAME, [SavingGoalName] AS SAVING_GOAL_NAME FROM SavingsView
	WHERE [EMAIL] = @EMAIL
END
GO

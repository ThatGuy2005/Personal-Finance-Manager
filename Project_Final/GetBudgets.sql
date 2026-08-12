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
-- Description:	<A procedure that returns the budgets linked to an account.>
-- =============================================
CREATE PROCEDURE GetBudgets
	-- Add the parameters for the stored procedure here
	@EMAIL VARCHAR(255)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
	SELECT [BALANCE], [PERIOD_BEGIN],
			[PERIOD_END], [CATEGORYNAME], [NAME] FROM BudgetView
	WHERE EMAIL = @EMAIL
END
GO

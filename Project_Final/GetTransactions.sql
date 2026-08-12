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
-- Description:	<Given an email, it returns the transactions and the account that is bound to.>
-- =============================================
CREATE PROCEDURE GetTransactions 
	@EMAIL VARCHAR(255)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    SELECT [TRANSACTION_TIME], [SUB_CAT], [AMOUNT], [TYPE], [DESCRIPTION], [NAME] FROM [TransactionView]
	WHERE EMAIL = @EMAIL
END
GO

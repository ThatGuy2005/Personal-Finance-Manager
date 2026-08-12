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
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE GetAccountID
	@EMAIL VARCHAR(255), 
	@CURRENCY CHAR(3)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
	SELECT accounts.ACCOUNT_ID FROM Accounts
	JOIN Users ON
	Accounts.USER_ID = Users.USER_ID
	JOIN Currency ON
	Accounts.CURRENCY_ID = Currency.CURRENCY_ID
	WHERE Users.EMAIL = @EMAIL AND Currency.NAME = @CURRENCY

END
GO

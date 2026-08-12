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
CREATE PROCEDURE CreateAccount
	@EMAIL VARCHAR(255),
	@Purpose VARCHAR(255),
	@Currency CHAR(3),
	@Balance DECIMAL(10,5)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
	 
	INSERT INTO [Accounts] (PURPOSE_ID, CURRENCY_ID, BALANCE, [USER_ID])
	SELECT
		(SELECT PURPOSE_ID FROM Purposes WHERE NAME=@Purpose),
		(SELECT [CURRENCY_ID] FROM Currency WHERE NAME=@Currency),
		@Balance,
		(SELECT [USER_ID] FROM Users WHERE EMAIL = @EMAIL);
END
GO

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
-- Create date: <05/31/2026>
-- Description:	<A procedure for returning the current accounts of a user>
-- =============================================
CREATE PROCEDURE GetAccounts
	@EMAIL VARCHAR(255)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    SELECT [Purposes].[NAME], [Currency].[NAME],[Accounts].[BALANCE] FROM [Accounts]
	LEFT JOIN [Purposes] ON
		[Purposes].[PURPOSE_ID] = [Accounts].[PURPOSE_ID]
	LEFT JOIN [Currency] ON
		[Currency].[CURRENCY_ID] = [Accounts].[CURRENCY_ID]
	WHERE [USER_ID] = (
		SELECT [USER_ID] FROM [Users]
		WHERE [EMAIL] = @EMAIL
	)
	
END
GO

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
-- Description:	<A procedure executed for log in activity>
-- =============================================
CREATE PROCEDURE LogInUser
	@NAME VARCHAR(255),
	@EMAIL VARCHAR(255),
	@PASSWORD_HASH VARCHAR(255)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	SELECT [NAME] FROM Users
	WHERE [NAME] = @NAME AND
	[EMAIL] = @EMAIL AND
	[PASSWORD_HASH] = @PASSWORD_HASH
END
GO

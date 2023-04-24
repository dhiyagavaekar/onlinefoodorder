  WITH admRole      
  AS      
  (      
    select count(*) UsrRole from AspNetUserRoles usrRole join AspNetRoles r      
      on usrRole.RoleId = r.Id      
      and usrRole.UserId = dbo.funcGetUserIDForUserName(@UserName)      
      and Name in ('invoiceAdmin', 'superAdmin', 'CompanyAdmin', 'CompanyUser')      
  ),      
  StoreRole      
  AS      
  (      
    select count(*) UsrRole from AspNetUserRoles usrRole join AspNetRoles r      
      on usrRole.RoleId = r.Id      
      and usrRole.UserId = dbo.funcGetUserIDForUserName(@UserName)      
      and Name in ('StoreManager')      
  ),      
  ---select * from StoreLocation where CompanyID=17  
  Res      
  AS (      
    select s.*      
    from StoreLocation s      
    JOIN Company c ON s.CompanyID = c.CompanyID --Joined company table to get Isjobber column      
    where s.CompanyID = @CompanyID  and s.IsInPOSSyncStatus=1      
    --AND s.IsJobberOnly = 0 AND c.IsJobber = 0      
    and ( (select UsrRole from admRole) > 0)       
    UNION       
    select  s.*      
    from StoreLocation s join StoreUser su on s.StoreLocationID = su.StoreLocationID      
    JOIN Company c ON s.CompanyID = c.CompanyID --Joined company table to get Isjobber column      
    where s.CompanyID = @CompanyID   and s.IsInPOSSyncStatus=1      
    --AND s.IsJobberOnly = 0 AND c.IsJobber = 0      
    and su.appUserID= dbo.funcGetUserIDForUserName(@UserName)       
    --AND c.IsJobber = 0      
    UNION  -- Added this select statement to get the jobber related stores when logged in as Jobber Company.      
        -- And to get stores based on user role           
    SELECT  sl.*  from JobberStoreLocation jsl      
    JOIN StoreLocation sl ON jsl.StoreLocationID=sl.StoreLocationID      
    JOIN StoreUser su ON su.StoreLocationID=jsl.StoreLocationID      
    where jsl.CompanyID = @CompanyID  and sl.IsInPOSSyncStatus=1 and su.appUserID= dbo.funcGetUserIDForUserName(@UserName)      
    --AND c.IsJobber = 1       
          
    UNION -- This is for jobber admin level, to get all stores      
    SELECT sl.*  from JobberStoreLocation jsl      
    JOIN StoreLocation sl ON jsl.StoreLocationID=sl.StoreLocationID      
    JOIN Company c ON jsl.CompanyID=c.CompanyID      
    WHERE c.CompanyID=@CompanyID      
     and sl.IsInPOSSyncStatus=1      
    and ( (select UsrRole from admRole) > 0)       
  )      
  select * from Res 
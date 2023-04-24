declare @field2 bigint              
declare @field1 bigint   
declare @field3 bigint     
set @field1   =(select count(*) from ComboDealStoreLocation cs join ComboDeal c on cs.ComboDealID = c.ComboDealID  where begindate < GetDate() and EndDate< Getdate()  and c.CompanyID=@CompanyID    
)      
set @field2=(select count(*) from ComboDealStoreLocation cs join ComboDeal c on cs.ComboDealID= c.ComboDealID  where  DATEDIFF(day, GETDATE(),endDate)= @Daysleft  and c.companyID=@CompanyID)    
     
     
     
   set @field3 =(select count(*) from ComboDealStoreLocation cs join ComboDeal c on cs.ComboDealID = c.ComboDealID  where  day (EndDate) >= day (Getdate())  and c.CompanyID=@CompanyID    
)     
declare @result  table      
(ExpiredCount bigint, GoingToExpireCount bigint, Active bigint)      
      
insert into @result values(@field1,@field2,@field3)      
      
select * from @result   
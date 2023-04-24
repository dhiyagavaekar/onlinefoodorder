declare @field2 bigint                  
declare @field1 bigint   
declare @field3 bigint          
set @field1   =(select count(*) from MixMatchstorelocation ms join mixmatch m on ms.MixmatchID = m.MixmatchID  where begindate < GetDate() and cast(EndDate as date )< Getdate()  and m.CompanyID=@CompanyID        
)          
set @field2=(select count(*) from mixmatchstorelocation ms join mixmatch m on ms.MixmatchID= m.MixmatchID where ( DATEDIFF(day,GETDATE(),cast (EndDate as date)) < @Daysleft  OR DATEDIFF(day,GETDATE(),cast (EndDate as date)) = @Daysleft OR  DATEDIFF(day,GETDATE(),cast (EndDate as date)) =0 ) AND (cast (EndDate as date ) > Getdate() OR cast (EndDate as date ) = Getdate())  and m.companyID=@CompanyID)        
set @field3=(select count(*) from mixmatchstorelocation ms join mixmatch m on ms.MixmatchID= m.MixmatchID where  day (EndDate) >= day (Getdate())  and m.CompanyID=@CompanyID    
)     
         
  
  
declare @result  table          
(ExpiredCount bigint, GoingToExpireCount bigint,Active bigint)          
          
insert into @result values(@field1,@field2,@field3)          
          
select * from @result 
declare @field2 bigint            
declare @field1 bigint    
declare @insertitems table    
(    
ItemID bigint )    
declare @companygrp table    
(CompanypriceGroupID Bigint )    
    
insert into @insertitems select items from     
    dbo.GetTableFromCommaString(@ItemID, ',')    
    
declare @Items table    
( ItemID bigint,PriceGroupID bigint,POSCode varchar(50),Description varchar(100)    
)    
    
    
    
insert into @companygrp    
select ig.CompanyPriceGroupID from itemListGroup ig      
where ItemListID= @ItemListID    
DECLARE cur CURSOR Local   FOR    
SELECT CompanyPriceGroupID from @companygrp    
open cur    
fetch next from cur into @field1    
    
while @@FETCH_STATUS = 0 BEGIN    
    
    
    insert into @Items     
    exec spGetPriceGroupItems @field1    
     
    
  fetch next from cur into @field1    
    
  END    
    
close cur    
deallocate cur    
    
    
delete from @insertitems  where ItemID in (SELECT  itemID      
                FROM    @Items)    
        
        
    
    declare inscur cursor local for     
    select ItemID from @insertitems      
    open inscur     
    fetch next from inscur into @field2    
        
while @@FETCH_STATUS = 0 BEGIN     
    
insert into ItemListItem values( @ItemListID,@field2,@username,GetDate(),@username,getDate())    
fetch next from inscur into @field2    
end    
close inscur    
deallocate inscur    
select 1
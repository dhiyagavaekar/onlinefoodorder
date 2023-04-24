declare @tempdata table          
(ItemListId bigint,          
           
NoOfItems bigint          
           
)          
          
  ;          
  with           
  itemData AS (SELECT    i.ItemListID, COUNT(il.ItemID) AS NoOfItems                 
                                 FROM         dbo.ItemList AS i left JOIN                  
                                                       dbo.ItemListItem AS il ON i.ItemListID = il.ItemListID                  
                               where i.CompanyID=@CompanyID  GROUP BY i.ItemListID)             
                
insert into @tempdata           
select *  from itemData           
          
          
            
  declare @field2 bigint                    
declare @field1 bigint            
declare @spdata table          
(          
ItemID bigint,          
PriceGroupID bigint,          
POSCode varchar(100),          
Description varchar(100)          
          
)          
declare @insertitems table            
(            
          
ItemListID bigint,          
CompanypriceGroupID bigint,          
itemcount bigint)            
declare @companygrp table            
(CompanypriceGroupID Bigint,          
itemListID Bigint )            
          
            
            
            
insert into @companygrp            
select ig.CompanyPriceGroupID,ItemListID from itemListGroup ig              
where ItemListID in (Select ItemListID from ItemList where companyID=@CompanyID)           
          
          
declare @ItemListId bigint          
DECLARE cur CURSOR Local   FOR            
SELECT CompanyPriceGroupID,itemListID from @companygrp            
open cur            
fetch next from cur into @field1 ,@ItemListId           
            
while @@FETCH_STATUS = 0 BEGIN            
insert into @spdata          
  exec spGetPriceGroupItems @field1            
  set @field2= @@RowCount          
           
  insert into @insertitems          
  values ( @ItemListId,@field1,@field2)          
            
  fetch next from cur into @field1 ,@ItemListId           
            
  END            
            
close cur            
deallocate cur            
            
  insert into @tempdata select ItemListID,itemcount from @insertitems          
          
  ;          
  with           
  finaldata as(          
  select td.ItemListID As ItemListID, SUM(td.NoOfItems) as NoOfItems,it.Description As Description from @tempdata td           
   join ItemList it on td.ItemListID = it.ItemListID group by  td.ItemListID,it.Description          
  )          
          
   select * from finaldata
declare @tempdata table        
(ItemListID bigint,        
  MixMatchID bigint,    
  MixMatchName varchar(100),    
  ItemListName varchar(100),     
NoOfItems bigint        
         
)        
        
  ;        
  with         
  itemData AS (SELECT    i.ItemListID,m.MixMatchID,M.Description as MixMatchName,i.Description as ItemListName,  COUNT(il.ItemID) AS NoOfItems              
                                 FROM         dbo.ItemList AS i left JOIN                
                                                       dbo.ItemListItem AS il ON i.ItemListID = il.ItemListID    
                join dbo.MixMatch m on m.ItemListID= i.ItemListID                
                               where i.CompanyID=@CompanyID GROUP BY i.ItemListID,m.MixMatchID,m.Description,i.Description)           
              
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
          
  insert into @tempdata select m.ItemListID,m.MixmatchID,m.Description,il.description ,i.itemcount from @insertitems i    
                                join ItemList il on i.ItemListID= il.ItemListID     
        join MixMatch m on m.ItemListID= il.ItemListID        
        
  ;        
  with         
  finaldata as(        
  select td.ItemListID, SUM(td.NoOfItems) as NoOfItems,td.ItemListName,td.MixMatchID,td.MixMatchName from @tempdata td              
   group by  td.ItemListID, td.ItemListName,td.MixMatchID,td.MixMatchName      
  )        
        
   select * from finaldata
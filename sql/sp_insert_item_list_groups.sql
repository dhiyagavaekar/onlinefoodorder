                 
declare @field2 bigint            
declare @field1 bigint    
    
    
declare @Items table    
( ItemID bigint,PriceGroupID bigint,POSCode varchar(50),Description varchar(100)    
)    
    insert into @Items     
    exec spGetPriceGroupItems @GroupID    
    
    
 delete from ItemListItem where itemID in (select itemID from @items) and ItemListID=@ItemListID    
    
     
 insert into ItemListgroup values(@ItemListID,@GroupID,@username,GetDate(),@username,GetDate())    
 select  1    
    
    
 select il.ItemListID,il.ItemListItemID,il.ItemID,i.POSCode,i.Description,si.StoreLocationItemID,si.StorelocationID,    
 si.POSSyncStatusID,ps.POSSyncStatusCode,si.RegularSellPrice,si.InventoryValuePrice,si.ProfitMargin,    
  si.Buydown,i.POSCode AS UPCCode from ItemListItem il              
        join Item i on il.ItemID= i.ItemID             
    left join StoreLocationItem si on si.ItemID=i.ItemID   and si.StoreLocationID=@StoreLocationID           
    left  join POSSyncStatus ps on ps.POSSyncStatusID=si.POSSyncStatusID            
     where il.ItemLIstID= @ItemListID   
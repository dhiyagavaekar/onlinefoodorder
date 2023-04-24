With           
AllStores          
as          
(          
  select storelocationId,StoreName,POSSystemCD,StoreFullName,IsInPOSSyncStatus        
  from  StoreLocation where storelocationId=@storeLocationID      
),          
SLI as          
(          
 select *           
 from vwStoreLocationItem          
 where ItemID in(select ItemID from ItemPriceGroup where PriceGroupID=@itemPricegroupID)  And StoreLocationID=@storeLocationID        
)       
select distinct AllStores.StoreLocationID,          
  AllStores.StoreName,          
  AllStores.POSSystemCD,          
  AllStores.StoreFullName,          
  AllStores.IsInPOSSyncStatus,        
     ISNULL(SLI.POSSyncStatusID,1) POSSyncStatusID ,           
  ISNULL(SLI.POSSyncStatusCode,'Current')POSSyncStatusCode,          
  SLI.IsTrackItem,          
  ISNULL(SLI.ReportPOSCode,'') ReportPOSCode,          
  SLI.InventoryValuePrice,          
  SLI.RegularSellPrice AS RegularSellPrice,          
  SLI.BasicBuyDown,          
  SLI.RackAllowance,          
  SLI.BuyDown,          
  SLI.POSCode,          
  SLI.ItemID,          
  SLI.GrossProfit,          
  SLI.MaxInventory,          
  SLI.MinInventory,          
  SLI.DepartmentDescription,          
  SLI.CurrentInventory,          
  SLI.InventoryAsOfDate,          
  ISNULL(SLI.StoreLocationItemID,0) StoreLocationItemID,          
  SLI.StoreLocationTaxID,          
  SLI.StoreLocationSalesRestrictionID,          
  (SELECT TaxStrategyDescription FROM StoreLocationTax          
       WHERE StoreLocationTaxID = SLI.StoreLocationTaxID          
   ) AS TaxStrategyDescription ,          
   (SELECT SalesRestrictionDescription FROM StoreLocationSalesRestriction               
       WHERE StoreLocationSalesRestrictionID = SLI.StoreLocationSalesRestrictionID          
   ) AS SalesRestrictionDescription ,        
    SLI.StoreLocationFeeID,          
       (SELECT FeeDescription FROM StoreLocationFee         
       WHERE StoreLocationFeeID = SLI.StoreLocationFeeID          
   ) AS StoreLocationFeeDescription ,         
  SLI.IsUpdatePrice,            
  (case           
  when SLI.StoreLocationID is null then          
   255          
  else          
   ROW_NUMBER() OVER(ORDER BY SLI.StoreName)          
  end) SrNO,          
  (case           
  when SLI.StoreLocationID is null then          
   CONVERT(bit,0)          
  else          
   CONVERT(bit,1)          
  end) StoreExists,  
  SLI.ItemDescription          
from AllStores      
LEFT join SLI on AllStores.StoreLocationID=SLI.StoreLocationID          
         
ORDER BY SrNO          

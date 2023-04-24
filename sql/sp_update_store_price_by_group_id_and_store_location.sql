BEGIN  
  
Declare @CompanyID bigint    
    
SET  @CompanyID=(SELECT CompanyID from StoreLocation where StoreLocationID=@storeLocationID)    
  
IF(@buyingCost is not Null and @buyingCost>0)  
BEGIN  
update StoreLocationItem set RegularSellPrice=@sellingPrice,InventoryValuePrice=@buyingCost where StoreLocationID=@storeLocationID and itemID in(Select ItemID from ItemPriceGroup where PriceGroupID=@itemPricegroupID)  
END  
ELSE  
BEGIN  
update StoreLocationItem set RegularSellPrice=@sellingPrice where StoreLocationID=@storeLocationID and itemID in(Select ItemID from ItemPriceGroup where PriceGroupID=@itemPricegroupID)  
END  
  
IF Exists(Select StorePriceGroupID from StorePriceGroup where StoreLocationID=@storeLocationID AND ItemGroupID=@itemPricegroupID )  
BEGIN  
update StorePriceGroup set SellingPrice=@sellingPrice,BuyingCost=@buyingCost where StoreLocationID=@storeLocationID AND ItemGroupID=@itemPricegroupID  
END  
ELSE  
BEGIN  
INSERT INTO StorePriceGroup  
           ([StoreLocationID]  
           ,[ItemGroupID]  
           ,[SellingPrice]  
           ,[BuyingCost])  
     VALUES  
           (@storeLocationID  
           ,@itemPricegroupID  
           ,@sellingPrice  
           ,@buyingCost)  
END  
  
END       
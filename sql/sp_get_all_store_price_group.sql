BEGIN 
Declare @IsPriceChanged bit, @price money,@CompanyID bigint      
      
SET  @CompanyID=(SELECT CompanyID from StoreLocation where StoreLocationID=@StoreLocationID)      
        
  SELECT Distinct G.CompanyPriceGroupID As GroupID,  
   G.CompanyPriceGroupName As GroupDescription,@StoreLocationID As StoreLocationID,(SELECT StoreName from StoreLocation where StoreLocationID=@StoreLocationID) As StoreName,      
   Case When((SELECT top 1 [StorePriceGroupID] from StorePriceGroup where ItemGroupID=G.CompanyPriceGroupID AND StoreLocationID=@StoreLocationID)>0) Then       
  (SELECT top 1 [StorePriceGroupID] from StorePriceGroup where ItemGroupID=G.CompanyPriceGroupID AND StoreLocationID=@StoreLocationID) ELSE NULL      
  END As StorePriceGroupID,      
  Case When((SELECT top 1 [StorePriceGroupID] from StorePriceGroup where ItemGroupID=G.CompanyPriceGroupID AND StoreLocationID=@StoreLocationID)>0) Then       
  (SELECT top 1 [SellingPrice] from StorePriceGroup where ItemGroupID=G.CompanyPriceGroupID AND StoreLocationID=@StoreLocationID) ELSE NULL      
  END As SellingPrice,Case When((SELECT top 1 [StorePriceGroupID] from StorePriceGroup where ItemGroupID=G.CompanyPriceGroupID)>0) Then       
  (SELECT top 1 BuyingCost from StorePriceGroup where ItemGroupID=G.CompanyPriceGroupID AND StoreLocationID=@StoreLocationID) ELSE NULL      
  END As BuyingCost,      
  Case When((SELECT top 1 [StorePriceGroupID] from StorePriceGroup where ItemGroupID=G.CompanyPriceGroupID AND StoreLocationID=@StoreLocationID)>0) Then       
  Case When((SELECT top 1 StoreLocationItemID from StoreLocationItem where StoreLocationID=@StoreLocationID AND RegularSellPrice<>(SELECT top 1 [SellingPrice] from StorePriceGroup where ItemGroupID=G.CompanyPriceGroupID AND StoreLocationID=@StoreLocationID))>0) then     
1 ELSE      
  0  END END As IsPriceChanged,(SELECT Count(*) from ItemPriceGroup Where PriceGroupID=G.CompanyPriceGroupID) As itemCount      
   from  CompanyPriceGroup G Where CompanyID=@CompanyID     
    order by GroupDescription 
  END 
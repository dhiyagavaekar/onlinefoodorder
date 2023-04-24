Declare
@CompanyID NVARCHAR(12) =@tempCompanyID,                  
@isShowPricing BIT = @tempisShowPricing ,                  
@isShowMultiPackPricing BIT = @tempisShowMultiPackPricing,                  
@posCodeOrDesc NVARCHAR(400) = @tempposCodeOrDesc ,                  
@sellingUnitStart NUMERIC(10, 4) = @tempsellingUnitStart ,                  
@sellingUnitEnd NUMERIC(10, 4) = @tempsellingUnitEnd ,                  
@UnitsInCaseStart NUMERIC(10, 4) = @tempUnitsInCaseStart ,                  
@UnitsInCaseEnd NUMERIC(10, 4) = @tempUnitsInCaseEnd ,                  
@SellingPriceStart NUMERIC(10, 4) = @tempSellingPriceStart ,                  
@SellingPriceEnd NUMERIC(10, 4) = @tempSellingPriceEnd ,                  
@InventoryValuePriceStart NUMERIC(10, 4) = @tempInventoryValuePriceStart ,                  
@InventoryValuePriceEnd NUMERIC(10, 4) = @tempInventoryValuePriceEnd ,                  
@CurrentInventoryStart NUMERIC(10, 4) = @tempCurrentInventoryStart ,                  
@CurrentInventoryEnd NUMERIC(10, 4) = @tempCurrentInventoryEnd ,                  
@ProfitMarginStart NUMERIC(10, 4) = @tempProfitMarginStart ,                  
@ProfitMarginEnd NUMERIC(10, 4) = @tempProfitMarginEnd ,                  
@Location NVARCHAR(1500) = @tempLocation ,                  
@Vendor NVARCHAR(1500) = @tempVendor ,                  
@Department NVARCHAR(1500) = @tempDepartment,                  
@POSSyncStatus NVARCHAR(12) = @tempPOSSyncStatus ,                  
@isTrackItem BIT = @tempisTrackItem ,                  
@isMultipack BIT = @tempisMultipack ,                  
@isActive BIT = @tempisActive ,                  
@GroupID NVARCHAR(12) = @tempGroupID,                  
@isShowDetails  BIT = @tempisShowDetails    
  
 declare  @MyTable TABLE  
           (        ItemID bigint ,  
                    CompanyID  bigint,  
                   DepartmentID bigint ,  
                    ActiveFlag bit,  
                    POSCode varchar(24) ,  
                   PosCodeFormatID bigint ,  
                    UOMID bigint ,  
                    Description VARCHAR(40),  
                    FamilyUPCCode VARCHAR(3),  
                    SellingUnits float,  
                    UnitsInCase int,  
                    LastModifiedBy VARCHAR(20) ,  
                    IsMultipackFlag bit,  
                    NoOfBaseUnitsInCase int,  
                    LastModifiedDateTime datetime,  
                    DepartmentDescription VARCHAR(24) ,  
                    UOMDescription VARCHAR(50),  
                     GrossProfit DECIMAL ,  
                     IsTrackItem  bit,  
                    RegularSellPrice money ,  
                     InventoryValuePrice money,  
                     BuyDown  DECIMAL,  
                     BasicBuyDown DECIMAL,  
                     RackAllowance DECIMAL,  
                    MaxInventory int ,  
                     MinInventory int,  
                   CurrentInventory int,  
                   InventoryAsOfDate datetime,  
                    StoreLocationItemID BIGINT,  
                     StoreLocationID BIGINT,  
                     StoreName varchar(20),  
                   VendorID BIGINT,  
                   POSCodeModifier int,  
                   RegularPackageSellPrice money,  
                   mulType VarChar(10),  
                   MultipackItemID bigint)  
                   insert into @MyTable  
                     
     exec spSearchStoreLocationItems     @CompanyID  ,  
    @isShowPricing  ,  
    @isShowMultiPackPricing,  
    @posCodeOrDesc  ,  
    @sellingUnitStart  ,  
    @sellingUnitEnd  ,  
    @UnitsInCaseStart  ,  
    @UnitsInCaseEnd,  
    @SellingPriceStart  ,  
    @SellingPriceEnd ,  
    @InventoryValuePriceStart ,  
    @InventoryValuePriceEnd  ,  
    @CurrentInventoryStart ,  
    @CurrentInventoryEnd  ,  
    @ProfitMarginStart ,  
    @ProfitMarginEnd ,  
    @Location  ,  
    @Vendor ,  
    @Department  ,  
    @POSSyncStatus  ,  
    @isTrackItem ,  
    @isMultipack ,  
    @isActive  ,  
    @GroupID,  
    @isShowDetails  
      
    IF(@SearchBy=1)  
    select * from @MyTable where DepartmentDescription='' or DepartmentDescription is null or DepartmentDescription='UNKNOWN'  
      
      
        --Top 50 Selling Items               
    Else if(@SearchBy=2)  
    begin  
     with Results as(  
             SELECT top 50 t.POSCode, SalesQuantity  
                   FROM  
                  (SELECT ism.POSCode,ism.SalesQuantity,ROW_NUMBER() OVER (PARTITION BY i.POSCode ORDER BY SalesQuantity DESC) AS RN  
                            FROM ISMDetail ism join Item i on i.POSCode=ism.POSCode where CompanyID=@CompanyID) AS t  
                               WHERE RN = 1  
                        ORDER BY SalesQuantity desc)  
             select m.* from @MyTable m join Results on m.POSCode=Results.POSCode  
         end      
               
          --Least 50 Selling Items  
              Else if(@SearchBy=3)  
              begin  
                with Results as(  
                     SELECT top 50 t.POSCode, SalesQuantity  
                                 FROM  
                      (SELECT ism.POSCode,ism.SalesQuantity,ROW_NUMBER() OVER (PARTITION BY i.POSCode ORDER BY SalesQuantity asc) AS RN  
                               FROM ISMDetail ism join Item i on i.POSCode=ism.POSCode where CompanyID=@CompanyID) AS t  
                                         WHERE RN = 1  
                                 ORDER BY SalesQuantity asc)  
                           select m.* from @MyTable m join Results on m.POSCode=Results.POSCode     
                     end        
                         
       ELSE IF(@SearchBy=4)  
         select * from @MyTable where SellingUnits is null or SellingUnits=0  
       ELSE IF(@SearchBy=5)  
         select * from @MyTable m where  m.InventoryValuePrice=0 or m.InventoryValuePrice is null    
           
       ELSE IF(@SearchBy=6)  
         select * from @MyTable m where  m.regularSellPrice=0 or m.regularSellPrice is null   
                
       ELSE IF(@SearchBy=7)  
         select * from @MyTable where  UnitsInCase is null or UnitsInCase=0  
        
       Else IF(@SearchBy=8)  
         select * from @MyTable where Description='' or Description is null  
      
       ELSE IF(@SearchBy=9)  
         select * from @MyTable m where m.ItemID Not in(Select ItemID from StoreLocationItem where StoreLocationID in (select StoreLocationID from StoreLocation where CompanyID=@CompanyID) )   
     -- select * from Item where Item.ItemID Not in(Select * from StoreLocationItem sli left  join @MyTable  m on m.ItemID=sli.ItemID where sli.ItemID=null)  -- sli.StoreLocationID is null or sli.StoreLocationID=0  
       Else IF(@SearchBy=10)  
       BEGIN     
         select m.ItemID, m.CompanyID, m.DepartmentID, m.ActiveFlag, m.POSCode, m.PosCodeFormatID, m.UOMID,  m.Description, m.FamilyUPCCode, m.SellingUnits, m.UnitsInCase, m.LastModifiedBy,   
         m.IsMultipackFlag, m.NoOfBaseUnitsInCase, m.LastModifiedDateTime, m.DepartmentDescription, m.UOMDescription, m.GrossProfit, m.IsTrackItem, m.RegularSellPrice, m.InventoryValuePrice, m.BuyDown, m.BasicBuyDown, m.RackAllowance, m.MaxInventory, m.Mi
nInventory, m.CurrentInventory,isnull(m.InventoryAsOfDate,'') as InventoryAsOfDate, m.StoreLocationItemID, m.StoreLocationID, m.StoreName, m.VendorID, m.POSCodeModifier ,m.RegularPackageSellPrice,m.mulType,m.MultipackItemID  
         from @MyTable m join Multiplier ml ON m.ItemID= ml.ContainedItemID  
         UNION  
         select m.ItemID, m.CompanyID, m.DepartmentID, m.ActiveFlag, m.POSCode, m.PosCodeFormatID, m.UOMID,  m.Description, m.FamilyUPCCode, m.SellingUnits, m.UnitsInCase, m.LastModifiedBy,  
          m.IsMultipackFlag, m.NoOfBaseUnitsInCase, m.LastModifiedDateTime, m.DepartmentDescription, m.UOMDescription, m.GrossProfit, m.IsTrackItem, m.RegularSellPrice, m.InventoryValuePrice, m.BuyDown, m.BasicBuyDown, m.RackAllowance, m.MaxInventory, m.M
inInventory, m.CurrentInventory,isnull(m.InventoryAsOfDate,'')as InventoryAsOfDate, m.StoreLocationItemID, m.StoreLocationID, m.StoreName, m.VendorID, m.POSCodeModifier,m.RegularPackageSellPrice,m.mulType,m.MultipackItemID  
          from @MyTable m join Multiplier ml ON m.ItemID= ml.ItemID  
         End  
           
       Else  
         select * from @MyTable   
  
  
  
--EXEC spSample 3,0,'',null,null,null,null,null,null,null,null,null,null,null,null,'15,16,17','','',null,null,null,null,null  
--EXEC spSearchStoreLocationItems 3,1,'',null,null,null,null,null,null,null,null,null,null,null,null,'17,','','',null,null,null,null,null  
  
--EXEC spSearchStoreLocationItems 3,0,'',null,null,null,null,null,null,null,null,null,null,null,null,'15,','','',null,null,null,null,null  
--EXEC spSearchItemsByCriteria 3,1,0,'',null,null,null,null,null,null,null,null,null,null,null,null,'15,','','',null,null,null,null,null,10  
  
  
  
  
  
  
  
  
  
  
  
  
  
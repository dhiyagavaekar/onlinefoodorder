SELECT  distinct Item.ItemID ,                                                                                  
                    Item.CompanyID ,                                                                              
                    Item.DepartmentID ,                                                                                  
                    Item.ActiveFlag ,                                                                                  
                    Item.POSCode ,  
                    Item.PosCodeFormatID ,                            
                    Item.UOMID ,                                                                                                                                                                                                                                         
                    Item.Description ,                                                                                  
                    Item.FamilyUPCCode ,                                                                                  
                    Item.SellingUnits ,                                                                                  
                    Item.UnitsInCase ,                        
                    Item.LastModifiedBy ,                                                                                  
                    Item.IsMultipackFlag ,                                                 
                    Item.NoOfBaseUnitsInCase ,                                      
                    Convert(smalldatetime,Item.LastModifiedDateTime) LastModifiedDateTime ,                                                                                  
                    'NA' as NA,
                    ISNULL(SLI.IsTrackItem, 0) AS IsTrackItem ,                                                                                  
                    ROUND( SLI.RegularSellPrice, 3) AS RegularSellPrice ,                                                                                  
                    ROUND(ISNULL(SLI.InventoryValuePrice, 0), 3) AS InventoryValuePrice ,                                                   
                    ISNULL(SLI.BasicBuydown, 0) AS BasicBuyDown ,                                                                                  
                    ISNULL(SLI.RackAllowance, 0) AS RackAllowance ,                                                                                  
                    ISNULL(SLI.MaxInventory, 0) AS MaxInventory ,                                         
                    ISNULL(SLI.MinInventory, 0) AS MinInventory ,                                                                                  
                    ISNULL(SLI.CurrentInventory, 0) AS CurrentInventory ,                                          
                    ISNULL(SLI.InventoryAsOfDate,'') AS InventoryAsOfDate ,                                                                                  
                    ISNULL(SLI.StoreLocationItemID, 0) AS StoreLocationItemID ,                      
                    ISNULL(SLI.StoreLocationID, 0) AS StoreLocationID,
                    SL.StoreName as StoreName,
                    0 AS VendorID,                             
                    0 POSCodeModifier  ,                                                                              
                    0.00 as RegularPackageSellPrice,
                    Case WHEN Item.ItemID = MPack.ContainedItemID THEN 'Pack'                                                                                 
                    WHEN Item.ItemID=MCarton.ItemID THEN 'Crtn' ELSE   'none' END mulType,                                                                                  
                    CONVERT(BIGINT, 0) as MultipackItemID,
                    ISNULL(CompanyStoreGRP.CompanyStoreGroupName, NULL) AS CompanyStoreGroupName,                                                                
				      ISNULL(CompanyStoreGRP.CompanyStoreGroupID, NULL) AS CompanyStoreGroupID   ,                                  
				   ( CASE WHEN ( ISNULL(SLI.RegularSellPrice, 0) <> 0 )                                                                                  
				                           THEN (ISNULL(SLI.RegularSellPrice, 0) - ISNULL(SLI.InventoryValuePrice, 0)- (ISNULL(BDSL.BuyDownAmt, 0) * ISNULL(IPG.ConversionFactor, 1))) / SLI.RegularSellPrice * 100  
				         ELSE 0                                                                                  
				                      END ) AS GrossProfit,                                  
				    ISNULL(BDSL.BuyDownAmt, 0) * ISNULL(IPG.ConversionFactor, 1) as BuyDownAmt,                                  
				   ISNULL(BDSL.MaxSuggestedRetailSellingPrice, 0) * ISNULL(IPG.ConversionFactor, 1) as SRP,                                  
				   ISNULL(IPG.ConversionFactor, 1) as ConversionFactor  
            FROM Item  
            JOIN StoreLocationItem SLI ON Item.ItemID = SLI.ItemID
            JOIN StoreLocation SL ON SL.StoreLocationID = SLI.StoreLocationID
            LEFT JOIN Multiplier MCarton on MCarton.ItemID =Item.ItemID                                                                                 
            LEFT JOIN Multiplier( NOLOCK ) MPack on MPack.ContainedItemID = Item.ItemID                                                                    
            LEFT JOIN StoreGroup StoreGrp ON StoreGrp.StoreLocationID = SLI.StoreLocationID                                                                  
            LEFT JOIN CompanyStoreGroup CompanyStoreGRP ON CompanyStoreGRP.CompanyStoreGroupID = StoreGrp.CompanyStoreGroupID                                               
            JOIN dbo.DepartmentLocation dl ON dl.DepartmentID in ('<departmentid>') AND  dl.StoreLocationID  =  SL.StoreLocationID 
            left  outer join ItemPriceGroup IPG on Item.ItemID= IPG.ItemID and (ipg.PriceGroupID = 25426402)                 
  			left Outer join BuydownGroup BDG on IPG.PriceGroupID = BDG.companypricegroupID and BDG.CompanySKUID=IPG.CompanySKUID                                  
            left  outer join BuydownStoreLocation BDSL on BDG.BuydownID=BDSL.BuydownID and BDSL.StoreLocationID=SL.StoreLocationID 
            WHERE Item.CompanyID in ('<companyid>') AND Item.DepartmentID IN ('<departmentid>') AND SL.StoreLocationID IN ('<storelocation>')
            AND SLI.IsTrackItem = <IsTrackItem>
            AND SLI.POSSyncStatusID = <POSSyncStatusID>
            AND Item.IsMultipackFlag = '<IsMultipackFlag>'
            AND Item.SellingUnits >= <sellingUnitStart>
            AND Item.SellingUnits <= <sellingUnitEnd>
            AND Item.UnitsInCase >= <UnitsInCaseStart>  
            AND Item.UnitsInCase <= <UnitsInCaseEnd>
            AND ROUND(SLI.RegularSellPrice, 2) >= <SellingPriceStart>
            AND ROUND(SLI.RegularSellPrice, 2) <= <SellingPriceEnd>                                                                              
            AND ROUND(SLI.InventoryValuePrice, 2) >= <InventoryValuePriceStart>
            AND ROUND(SLI.InventoryValuePrice, 2) <= <InventoryValuePriceEnd>
            AND ROUND(SLI.CurrentInventory, 2) >= <CurrentInventoryStart>
            AND ROUND(SLI.CurrentInventory, 2) <= <CurrentInventoryEnd>
            AND ProfitMargin >= <ProfitMarginStart>
            AND ProfitMargin <= <ProfitMarginEnd>
            AND (Item.Description like '%a%' OR Item.FamilyUPCCode like '%a%')
            order by Item.ItemID  desc 
            OFFSET <pagenumber> ROWS FETCH NEXT <records> ROWS ONLY
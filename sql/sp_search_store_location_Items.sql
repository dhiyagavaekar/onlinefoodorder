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

if (@Location  is null )                 
Begin set @Location =''                
end                
if (@Vendor  is Null)                 
Begin set @Vendor =''                
end                
                
                
if (@Department  IS  Null)                 
Begin set @Department =''                
end                
                
                  
                  
                  
                  
    DECLARE @VendorList TABLE ( VendorID BIGINT )                  
                      
    DECLARE @ItemList TABLE ( ItemID BIGINT )                  
                      
    IF ( LEN(@posCodeOrDesc) > 1 )                   
        BEGIN                                 
            INSERT  INTO @ItemList                  
                    SELECT  VendorItem.ItemID                  
                    FROM    VendorItem WITH ( NOLOCK )                  
                            JOIN Vendor( NOLOCK ) ON VendorItem.VendorID = Vendor.VendorID                  
                                           AND Vendor.CompanyID = @CompanyID                  
                                           AND VendorItem.VendorItemCode = @posCodeOrDesc                  
                                      
        END                  
                      
                  
    IF ( ISNUMERIC(@posCodeOrDesc) = 1                  
         AND LEN(@posCodeOrDesc) > 4                  
         AND LEN(@posCodeOrDesc) < 11                  
         AND @posCodeOrDesc IS NOT NULL                  
       )                   
        BEGIN                  
            SELECT  @posCodeOrDesc = dbo.funcConvertUPCEtoUPCA(@posCodeOrDesc)                  
        END                  
                    
    DECLARE @Store TABLE                  
        (                  
          CompanyID BIGINT ,                  
          StoreLocationID BIGINT ,                  
          StoreName VARCHAR(20)                  
        )                  
    DECLARE @Dept TABLE                  
        (                  
          DepartmentID BIGINT ,                  
          DepartmentDescription VARCHAR(24)                  
        )                  
    DECLARE @ItemPriceSchedule TABLE                  
        (                  
          ItemID BIGINT ,                  
          StoreLocationID BIGINT ,                  
          RegularSellPrice MONEY ,                  
          BeginDate DATETIME ,                  
          EndDate DATETIME                  
        )                  
                  
                  
                  
    INSERT  INTO @Store                  
            SELECT  CompanyID ,                 
                    StoreLocationID ,                  
                    StoreName                  
            FROM    StoreLocation( NOLOCK )                  
            WHERE   StoreLocationID IN (                  
                    SELECT  items                  
                    FROM    dbo.GetTableFromCommaString(@Location, ',') )                  
            UNION                  
      SELECT  CompanyID ,                  
                    StoreLocationID ,                  
                    StoreName                  
            FROM    StoreLocation( NOLOCK )                  
            WHERE   ISNULL(LTRIM(@Location), '') = ''                  
                    AND CompanyID = @CompanyID                  
                  
    INSERT  INTO @Dept                  
            SELECT  DepartmentID ,                  
         DepartmentDescription                  
            FROM    Department( NOLOCK )                  
            WHERE   CompanyID = @CompanyID                  
                    AND DepartmentID IN (                  
                    SELECT  items                  
      FROM    dbo.GetTableFromCommaString(@Department, ',') )                  
            UNION                  
            SELECT  DepartmentID ,                  
                    DepartmentDescription                  
            FROM    Department( NOLOCK )                  
            WHERE   @Department = ''                  
                    AND CompanyID = @CompanyID                                 
                    
                  
    IF ( LEN(LTRIM(@Vendor)) > 0 )                   
        BEGIN                  
                   
            INSERT  INTO @ItemList                  
                    SELECT  VendorItem.ItemID                  
                    FROM    VendorItem WITH ( NOLOCK )                  
                    WHERE   VendorID IN (                  
                            SELECT  VendorID                  
                            FROM    Vendor( NOLOCK )                  
                            WHERE   CompanyID = @CompanyID                  
                                    AND VendorID IN (                  
                                    SELECT  items                  
                                    FROM    dbo.GetTableFromCommaString(@Vendor,                  
                                                              ',') ) )                  
        END                  
                      
    IF ( ISNULL(@GroupID, -10) = -1 )                   
        BEGIN                  
            INSERT  INTO @ItemList                  
                    SELECT  I.ItemID                  
                    FROM    Item( NOLOCK ) i                  
                    WHERE   NOT EXISTS ( SELECT 1                  
                                         FROM   ItemPriceGroup( NOLOCK ) ig                  
                                         WHERE  i.ItemID = ig.ItemID )                  
                            AND CompanyID = @CompanyID                    
        END                        
    ELSE                   
        IF ( @GroupID IS NOT NULL )                   
            BEGIN                  
                INSERT  INTO @ItemList                  
                        SELECT  I.ItemID                  
                        FROM    Item( NOLOCK ) i                  
                        WHERE   EXISTS ( SELECT 1                  
                                         FROM   ItemPriceGroup( NOLOCK ) ig                  
                                         WHERE  i.ItemID = ig.ItemID                  
                                                AND ig.PriceGroupID = @GroupID )                  
                                AND CompanyID = @CompanyID                  
                       
            END                    
                  
 -- Populate the list if there is text passed                  
    IF ISNULL(@posCodeOrDesc, '') != ''                   
        BEGIN                  
            INSERT  INTO @ItemList                  
     SELECT  I.ItemID                  
                    FROM    Item( NOLOCK ) i                  
                    WHERE   ( i.POSCode = dbo.funcCheckPOSCode(@posCodeOrDesc)                  
                              OR ( i.Description LIKE '%' + @posCodeOrDesc                  
                                   + '%' )                  
                     )                  
                            AND CompanyID = @CompanyID                  
        END                    
                  
  /*                  
               OR ( )                  
 */                  
                  
    IF ( @isShowPricing = 'true' )                   
        BEGIN                  
      --  WITH ItemsList as(                  
        SELECT  Item.ItemID ,                  
                    Item.CompanyID ,                  
                    Item.DepartmentID ,                  
                    Item.ActiveFlag ,                  
                    Item.POSCode ,                  
                    Item.PosCodeFormatID ,                  
                    Item.UOMID ,                  
                    --Item.POSCode + CAST(dbo.Item.CheckDigit AS VARCHAR(50)) AS POSCodeWithCheckDigit ,               
                    
                    Item.Description ,                  
                    Item.FamilyUPCCode ,                  
                    Item.SellingUnits ,                  
                    Item.UnitsInCase ,                  
            Item.LastModifiedBy ,                  
                    Item.IsMultipackFlag ,                  
                    Item.NoOfBaseUnitsInCase ,                  
                    Convert(smalldatetime,Item.LastModifiedDateTime) LastModifiedDateTime ,                  
                    Department.DepartmentDescription ,                  
                    UOM.UOMDescription ,                  
                    ( CASE WHEN ( ISNULL(SLI.RegularSellPrice, 0) <> 0 )                  
                           THEN ( ( ROUND(SLI.RegularSellPrice, 3)                  
                                    - ( ROUND(ISNULL(SLI.InventoryValuePrice,                  
                                                     0), 3)                  
                                        - ISNULL(SLI.BuyDown, 0) ) ) * 100 )                  
                                / ROUND(ISNULL(SLI.RegularSellPrice, 0), 3)                  
                           ELSE 0                  
                      END ) AS GrossProfit ,                  
                    ISNULL(SLI.IsTrackItem, 0) AS IsTrackItem ,                  
                    ROUND( SLI.RegularSellPrice, 3) AS RegularSellPrice ,                  
                    ROUND(ISNULL(SLI.InventoryValuePrice, 0), 3) AS InventoryValuePrice ,                  
                    ISNULL(SLI.BuyDown, 0) AS BuyDown ,                  
                    ISNULL(SLI.BasicBuydown, 0) AS BasicBuyDown ,                  
                    ISNULL(SLI.RackAllowance, 0) AS RackAllowance ,                  
                    ISNULL(SLI.MaxInventory, 0) AS MaxInventory ,                  
                    ISNULL(SLI.MinInventory, 0) AS MinInventory ,                  
                    ISNULL(SLI.CurrentInventory, 0) AS CurrentInventory ,                                      
                    ISNULL(SLI.InventoryAsOfDate,'') AS InventoryAsOfDate ,                  
                    ISNULL(SLI.StoreLocationItemID, 0) AS StoreLocationItemID ,                  
                    ISNULL(SLI.StoreLocationID, 0) AS StoreLocationID ,                  
                    ISNULL(StoreLocation.StoreName, '') AS StoreName ,                  
                    CONVERT(BIGINT, 0) AS VendorID,                  
                    0 POSCodeModifier  ,                  
                    0.00 as RegularPackageSellPrice,                   
                    Case WHEN Item.ItemID = MPack.ContainedItemID THEN 'Pack'                  
                    WHEN Item.ItemID=MCarton.ItemID THEN 'Crtn' ELSE                                    
                    'none' END mulType,                  
                    CONVERT(BIGINT, 0) as MultipackItemID                  
                  
            FROM    Item( NOLOCK )                  
                    INNER JOIN @Dept Department ON Item.DepartmentID = Department.DepartmentID                  
                                                   AND Item.CompanyID = @CompanyID             
                     --JOIN dbo.DepartmentLocation dl ON dl.DepartmentID=Department.DepartmentID -- and  dl.StoreLocationID                        
                     --JOIN  @Store s ON s.StoreLocationID=dl.StoreLocationID                                                 
                    LEFT JOIN UOM( NOLOCK ) ON Item.UOMID = UOM.UOMID                  
                    JOIN StoreLocationItem( NOLOCK ) SLI ON Item.ItemID = SLI.ItemID                  
  JOIN @Store StoreLocation ON StoreLocation.StoreLocationID = SLI.StoreLocationID                  
                    LEFT JOIN Multiplier( NOLOCK ) MCarton on MCarton.ItemID =Item.ItemID                  
                    LEFT JOIN Multiplier( NOLOCK ) MPack on MPack.ContainedItemID = Item.ItemID                  
                   -- LEFT JOIN @ItemPriceSchedule IPS ON IPS.ItemID = Item.itemID                  
                          --                              AND IPS.StoreLocationID = SLI.StoreLocationID               
            WHERE   ( @isTrackItem IS NULL                  
                      OR SLI.IsTrackItem = @isTrackItem                  
                    )                  
                    AND ( @POSSyncStatus IS NULL                  
                          OR ( SLI.POSSyncStatusID = @POSSyncStatus )                  
                        )                  
                    AND ( @isMultipack IS NULL                  
                          OR Item.IsMultipackFlag = @isMultipack                  
                        )                  
                    AND ( @isActive IS NULL                  
                          OR Item.ActiveFlag = @isActive                  
                        )                  
                    AND ( ( ISNULL(@posCodeOrDesc, '') = ''                  
                            AND @GroupID IS NULL                  
                            AND LEN(LTRIM(@Vendor)) = 0                  
                          )                  
                          OR Item.ItemID IN ( SELECT    itemID                  
                                              FROM      @ItemList )                  
                        )                  
  AND ( @sellingUnitStart IS NULL                  
                          OR Item.SellingUnits >= @sellingUnitStart                  
                        )                  
                    AND ( @sellingUnitEnd IS NULL                  
                          OR Item.SellingUnits <= @sellingUnitEnd                  
                        )                  
                    AND ( @UnitsInCaseStart IS NULL                  
                          OR Item.UnitsInCase >= @UnitsInCaseStart                  
                        )                  
                    AND ( @UnitsInCaseEnd IS NULL                  
                          OR Item.UnitsInCase <= @UnitsInCaseEnd                  
                        )                  
                    AND ( ROUND(SLI.RegularSellPrice, 2) >= @SellingPriceStart                  
      OR @SellingPriceStart IS NULL                  
                        )                  
                    AND ( ROUND(SLI.RegularSellPrice, 2) <= @SellingPriceEnd                  
                          OR @SellingPriceEnd IS NULL                  
                        )                  
                    AND ( ROUND(SLI.InventoryValuePrice, 2) >= @InventoryValuePriceStart                  
                          OR @InventoryValuePriceStart IS NULL                  
                        )                  
 AND ( ROUND(SLI.InventoryValuePrice, 2) <= @InventoryValuePriceEnd                  
                          OR @InventoryValuePriceEnd IS NULL                  
     )                  
                    AND ( ROUND(SLI.CurrentInventory, 2) >= @CurrentInventoryStart                  
                          OR @CurrentInventoryStart IS NULL                  
                        )                  
                    AND ( ROUND(SLI.CurrentInventory, 2) <= @CurrentInventoryEnd                  
                          OR @CurrentInventoryEnd IS NULL                  
                )                  
                    AND ( ProfitMargin >= @ProfitMarginStart                  
                          OR @ProfitMarginStart IS NULL                  
                        )                  
                    AND ( ProfitMargin <= @ProfitMarginEnd                  
                          OR @ProfitMarginEnd IS NULL                  
                        )                  
            UNION                  
            SELECT  Item.ItemID ,                  
                    Item.CompanyID ,                  
                    Item.DepartmentID ,                  
          Item.ActiveFlag ,                  
                    Item.POSCode ,                  
                    Item.PosCodeFormatID ,                  
                    Item.UOMID ,                  
                    --Item.POSCode + CAST(dbo.Item.CheckDigit AS VARCHAR(50)) AS POSCodeWithCheckDigit ,             
                           
                    Item.Description ,                  
                    Item.FamilyUPCCode ,                  
                    Item.SellingUnits ,                  
                    Item.UnitsInCase ,                  
                    Item.LastModifiedBy ,                  
                    Item.IsMultipackFlag ,                  
                    Item.NoOfBaseUnitsInCase ,                  
                    Convert(smalldatetime,Item.LastModifiedDateTime) LastModifiedDateTime ,                  
                    Department.DepartmentDescription ,                  
                    UOM.UOMDescription ,                  
                    NULL AS GrossProfit ,                  
                    CONVERT(BIT, 0) AS IsTrackItem ,                  
                  --  ROUND(0, 2) AS RegularSellPrice ,                  
                    0 AS RegularSellPrice ,                  
              ROUND(0, 3) AS InventoryValuePrice ,                  
                    0 AS BuyDown ,                  
                    0 AS BasicBuyDown ,                  
                    0 AS RackAllowance ,                  
                    0 AS MaxInventory ,                  
                    0 AS MinInventory ,                  
                    0 AS CurrentInventory ,                  
                    '' as InventoryAsOfDate,                  
                    0 AS StoreLocationItemID ,                  
                    0 AS StoreLocationID ,                  
                    '' AS StoreName ,                  
                    0 AS VendorID,                  
                    0 POSCodeModifier  ,                  
                    0.00 as RegularPackageSellPrice,                   
                   Case WHEN Item.ItemID = MPack.ContainedItemID THEN 'Pack'        
                    WHEN Item.ItemID=MCarton.ItemID THEN 'Crtn' ELSE                              
                    'none' END mulType,                  
                    0 as MultipackItemID                  
                  
            FROM    Item( NOLOCK )                  
                    INNER JOIN @Dept Department ON Item.DepartmentID = Department.DepartmentID                  
                                                   AND CompanyID = @CompanyID                  
                    --JOIN dbo.DepartmentLocation dl ON dl.DepartmentID=Department.DepartmentID -- and  dl.StoreLocationID                        
      -- JOIN  @Store s ON s.StoreLocationID=dl.StoreLocationID                                                  
                    LEFT JOIN UOM( NOLOCK ) ON Item.UOMID = UOM.UOMID                  
                    LEFT JOIN Multiplier( NOLOCK ) MCarton on MCarton.ItemID =Item.ItemID                  
                    LEFT JOIN Multiplier( NOLOCK ) MPack on MPack.ContainedItemID = Item.ItemID                  
            WHERE   NOT EXISTS ( SELECT 1                  
                                 FROM   dbo.StoreLocationItem( NOLOCK ) sn                  
                                        JOIN @Store s ON sn.StoreLocationID = s.StoreLocationID                  
                 WHERE  item.ItemID = sn.ItemID )                  
                    AND ( @isMultipack IS NULL                  
                          OR Item.IsMultipackFlag = @isMultipack                  
                        )                  
                    AND ( @isActive IS NULL                  
                          OR Item.ActiveFlag = @isActive                  
                        )          
                    
                    AND ( ( ISNULL(@posCodeOrDesc, '') = ''                  
                            AND @GroupID IS NULL                  
                          )                  
          OR Item.ItemID IN ( SELECT    itemID                  
FROM      @ItemList )                  
                        )                  
                    AND ( @sellingUnitStart IS NULL                  
                          OR Item.SellingUnits >= @sellingUnitStart                  
                        )                  
                    AND ( @sellingUnitEnd IS NULL                  
                          OR Item.SellingUnits <= @sellingUnitEnd                  
                        )                  
                    AND ( @UnitsInCaseStart IS NULL                  
                          OR Item.UnitsInCase >= @UnitsInCaseStart                  
                        )                  
                    AND ( @UnitsInCaseEnd IS NULL                  
                          OR Item.UnitsInCase <= @UnitsInCaseEnd                  
                        )                  
                    AND @Location IS NULL                    
                                           
                                      
            --ORDER BY POSCodeWithCheckDigit                       
                   
        END                  
    ELSE IF(@isShowMultiPackPricing='true')                  
        BEGIN                  
                   
         SELECT  Item.ItemID ,                  
                    Item.CompanyID ,                  
                    Item.DepartmentID ,                  
                    Item.ActiveFlag ,                  
                    Item.POSCode ,                  
                    Item.PosCodeFormatID ,                  
                    Item.UOMID ,                  
                    --Item.POSCode + CAST(dbo.Item.CheckDigit AS VARCHAR(50)) AS POSCodeWithCheckDigit ,                 
                                 
     Item.Description ,                  
                    Item.FamilyUPCCode ,                  
                    Item.SellingUnits ,                  
                    Item.UnitsInCase ,                  
                    Item.LastModifiedBy ,                  
                    Item.IsMultipackFlag ,                  
                    Item.NoOfBaseUnitsInCase ,                  
                    Convert(smalldatetime,Item.LastModifiedDateTime) LastModifiedDateTime ,                  
                    Department.DepartmentDescription ,                  
                    UOM.UOMDescription ,                  
                    ( CASE WHEN ( ISNULL(SLI.RegularSellPrice, 0) <> 0 )                  
                           THEN ( ( ROUND(SLI.RegularSellPrice, 3)                  
                                    - ( ROUND(ISNULL(SLI.InventoryValuePrice,       
                                                     0), 3)                  
                                        - ISNULL(SLI.BuyDown, 0) ) ) * 100 )                  
                                / ROUND(ISNULL(SLI.RegularSellPrice, 0), 3)                  
                           ELSE 0                  
                      END ) AS GrossProfit ,                  
                    ISNULL(SLI.IsTrackItem, 0) AS IsTrackItem ,                  
                    ROUND( SLI.RegularSellPrice, 3) AS RegularSellPrice ,                  
                    ROUND(ISNULL(SLI.InventoryValuePrice, 0), 3) AS InventoryValuePrice ,                  
                    ISNULL(SLI.BuyDown, 0) AS BuyDown ,                  
                    ISNULL(SLI.BasicBuydown, 0) AS BasicBuyDown ,                  
            ISNULL(SLI.RackAllowance, 0) AS RackAllowance ,                  
                    ISNULL(SLI.MaxInventory, 0) AS MaxInventory ,                  
                    ISNULL(SLI.MinInventory, 0) AS MinInventory ,                  
                    ISNULL(SLI.CurrentInventory, 0) AS CurrentInventory ,                                  
                    ISNULL(SLI.InventoryAsOfDate,'') AS InventoryAsOfDate ,                  
                    ISNULL(SLI.StoreLocationItemID, 0) AS StoreLocationItemID ,                  
                    ISNULL(SLI.StoreLocationID, 0) AS StoreLocationID ,                  
                    ISNULL(StoreLocation.StoreName, '') AS StoreName ,                  
                    CONVERT(BIGINT, 0) AS VendorID,                  
                    MultipackItem.POSCodeModifier,                  
                    RegularPackageSellPrice,                  
                    Case WHEN Item.ItemID = MPack.ContainedItemID THEN 'Pack'                  
                    WHEN Item.ItemID=MCarton.ItemID THEN 'Crtn' ELSE                                    
                    'none' END mulType,                  
                    Convert( bigint,ISNULL(MultipackItem.MultipackItemID,0)) AS MultipackItemID                  
            FROM    Item( NOLOCK )                  
                    INNER JOIN @Dept Department ON Item.DepartmentID = Department.DepartmentID                  
                                                   AND Item.CompanyID = @CompanyID                  
                     --JOIN dbo.DepartmentLocation dl ON dl.DepartmentID=Department.DepartmentID -- and  dl.StoreLocationID                        
                     --JOIN  @Store s ON s.StoreLocationID=dl.StoreLocationID                                                 
                    LEFT JOIN UOM( NOLOCK ) ON Item.UOMID = UOM.UOMID                  
                    JOIN StoreLocationItem( NOLOCK ) SLI ON Item.ItemID = SLI.ItemID                  
                    JOIN @Store StoreLocation ON StoreLocation.StoreLocationID = SLI.StoreLocationID                  
                   INNER JOIN MultipackItem( NOLOCK ) on SLI.StoreLocationItemID=MultipackItem.StoreLocationItemID                  
                   LEFT JOIN Multiplier( NOLOCK ) MCarton on MCarton.ItemID =Item.ItemID                  
                    LEFT JOIN Multiplier( NOLOCK ) MPack on MPack.ContainedItemID = Item.ItemID                  
            WHERE   ( @isTrackItem IS NULL                  
                      OR SLI.IsTrackItem = @isTrackItem                  
                    )                  
AND ( @POSSyncStatus IS NULL                  
                          OR ( SLI.POSSyncStatusID = @POSSyncStatus )                  
                        )                  
                    --AND ( @isMultipack IS NULL                  
                    --      OR Item.IsMultipackFlag = @isMultipack                  
                    --    )         
     --by Gowtham to get all the items with or without ismultipack it true           
                    AND ( @isActive IS NULL                  
                          OR Item.ActiveFlag = @isActive                  
                        )                  
                    AND ( ( ISNULL(@posCodeOrDesc, '') = ''                  
                  AND @GroupID IS NULL                  
                            AND LEN(LTRIM(@Vendor)) = 0                  
                          )                  
                          OR Item.ItemID IN ( SELECT    itemID                  
                                              FROM      @ItemList )                  
                        )                  
                    AND ( @sellingUnitStart IS NULL                  
                          OR Item.SellingUnits >= @sellingUnitStart                  
                        )                  
                    AND ( @sellingUnitEnd IS NULL                  
                          OR Item.SellingUnits <= @sellingUnitEnd                  
                        )                  
                    AND ( @UnitsInCaseStart IS NULL                  
                          OR Item.UnitsInCase >= @UnitsInCaseStart                  
                   )                  
                    AND ( @UnitsInCaseEnd IS NULL                  
                          OR Item.UnitsInCase <= @UnitsInCaseEnd                  
                        )                  
                    AND ( ROUND(SLI.RegularSellPrice, 2) >= @SellingPriceStart                  
                          OR @SellingPriceStart IS NULL                  
                        )                  
                    AND ( ROUND(SLI.RegularSellPrice, 2) <= @SellingPriceEnd                  
                          OR @SellingPriceEnd IS NULL                  
                        )                  
                    AND ( ROUND(SLI.InventoryValuePrice, 2) >= @InventoryValuePriceStart                  
                          OR @InventoryValuePriceStart IS NULL                  
                        )                  
                    AND ( ROUND(SLI.InventoryValuePrice, 2) <= @InventoryValuePriceEnd                  
                          OR @InventoryValuePriceEnd IS NULL                  
                       )                  
                    AND ( ROUND(SLI.CurrentInventory, 2) >= @CurrentInventoryStart                  
                          OR @CurrentInventoryStart IS NULL                  
                        )                  
                    AND ( ROUND(SLI.CurrentInventory, 2) <= @CurrentInventoryEnd                  
                          OR @CurrentInventoryEnd IS NULL                  
                        )                  
                    AND ( ProfitMargin >= @ProfitMarginStart                  
                          OR @ProfitMarginStart IS NULL                  
                        )                  
                    AND ( ProfitMargin <= @ProfitMarginEnd                  
                          OR @ProfitMarginEnd IS NULL                  
                        )                  
            UNION                  
            SELECT  Item.ItemID ,                  
                    Item.CompanyID ,                  
     Item.DepartmentID ,                  
                    Item.ActiveFlag ,                
                    Item.POSCode ,                  
                    Item.PosCodeFormatID ,                  
                    Item.UOMID ,                  
                    --Item.POSCode + CAST(dbo.Item.CheckDigit AS VARCHAR(50)) AS POSCodeWithCheckDigit ,                  
                                 
     Item.Description ,                  
     Item.FamilyUPCCode ,                  
                    Item.SellingUnits ,                  
                    Item.UnitsInCase ,                  
                    Item.LastModifiedBy ,                  
                    Item.IsMultipackFlag ,                  
                    Item.NoOfBaseUnitsInCase ,                  
                    Convert(smalldatetime,Item.LastModifiedDateTime) LastModifiedDateTime ,                  
                    Department.DepartmentDescription ,                  
            UOM.UOMDescription ,                  
                    NULL AS GrossProfit ,                  
                    CONVERT(BIT, 0) AS IsTrackItem ,                  
                  --  ROUND(0, 2) AS RegularSellPrice ,                  
                    0 AS RegularSellPrice ,                  
                    ROUND(0, 3) AS InventoryValuePrice ,                  
                    0 AS BuyDown ,                  
                    0 AS BasicBuyDown ,                  
                    0 AS RackAllowance ,                  
                    0 AS MaxInventory ,                  
                    0 AS MinInventory ,                  
                    0 AS CurrentInventory ,                  
                    '' InventoryAsOfDate ,                  
                    0 AS StoreLocationItemID ,                  
                    0 AS StoreLocationID ,                  
                    '' AS StoreName ,                  
                    0 AS VendorID,                  
                    0 as POSCodeModifier,                  
                    0.00 RegularPackageSellPrice,              
                    Case WHEN Item.ItemID = MPack.ContainedItemID THEN 'Pack'                  
                    WHEN Item.ItemID=MCarton.ItemID THEN 'Crtn' ELSE                                    
                    'none' END mulType,                  
                    0 as MultipackItemID                  
                  
            FROM    Item( NOLOCK )                  
                    INNER JOIN @Dept Department ON Item.DepartmentID = Department.DepartmentID                  
                                                   AND CompanyID = @CompanyID                  
                    --JOIN dbo.DepartmentLocation dl ON dl.DepartmentID=Department.DepartmentID -- and  dl.StoreLocationID                        
                    -- JOIN  @Store s ON s.StoreLocationID=dl.StoreLocationID                                                  
                    LEFT JOIN UOM( NOLOCK ) ON Item.UOMID = UOM.UOMID                  
                    LEFT JOIN Multiplier( NOLOCK ) MCarton on MCarton.ItemID =Item.ItemID                  
                 LEFT JOIN Multiplier( NOLOCK ) MPack on MPack.ContainedItemID = Item.ItemID                  
            WHERE   NOT EXISTS ( SELECT 1                  
                                 FROM   dbo.StoreLocationItem sn                  
                                        JOIN @Store s ON sn.StoreLocationID = s.StoreLocationID                  
                                 WHERE  item.ItemID = sn.ItemID )                  
                    AND ( @isMultipack IS NULL                  
                          OR Item.IsMultipackFlag = @isMultipack                  
                        )                  
                    AND ( @isActive IS NULL                  
                          OR Item.ActiveFlag = @isActive                  
                        )                  
                AND ( ( ISNULL(@posCodeOrDesc, '') = ''                  
                            AND @GroupID IS NULL                  
                          )                  
                          OR Item.ItemID IN ( SELECT    itemID                  
                                              FROM      @ItemList )                  
                        )                  
                    AND ( @sellingUnitStart IS NULL                  
                          OR Item.SellingUnits >= @sellingUnitStart                  
                        )                  
                    AND ( @sellingUnitEnd IS NULL                  
                          OR Item.SellingUnits <= @sellingUnitEnd                  
                        )                  
                    AND ( @UnitsInCaseStart IS NULL                  
                          OR Item.UnitsInCase >= @UnitsInCaseStart                  
                        )                  
                    AND ( @UnitsInCaseEnd IS NULL                  
                          OR Item.UnitsInCase <= @UnitsInCaseEnd                  
                        )                  
                  AND @Location IS NULL                    
                    
        END                   
                          
                          
        ELSE IF(@isShowDetails='true')                  
        BEGIN                  
        SELECT  Item.ItemID ,                  
                    Item.CompanyID ,                  
                    Item.DepartmentID ,                  
                    Item.ActiveFlag ,                  
                    Item.POSCode ,                  
          Item.PosCodeFormatID ,                  
                    Item.UOMID ,                  
                    --Item.POSCode + CAST(dbo.Item.CheckDigit AS VARCHAR(50)) AS POSCodeWithCheckDigit ,                  
                                 
     Item.Description ,                  
                    Item.FamilyUPCCode ,                  
                    Item.SellingUnits ,                  
                    Item.UnitsInCase ,                  
                    Item.LastModifiedBy ,                  
                    Item.IsMultipackFlag ,                  
             Item.NoOfBaseUnitsInCase ,                  
                    Convert(smalldatetime,Item.LastModifiedDateTime) LastModifiedDateTime ,                  
                    Department.DepartmentDescription ,                  
                    UOM.UOMDescription ,                  
                    CONVERT(DECIMAL, 0) AS GrossProfit ,                  
                    CONVERT(BIT, 0) AS IsTrackItem ,                  
                    0.00 AS RegularSellPrice ,                  
                    0.00 AS InventoryValuePrice ,                  
                    CONVERT(DECIMAL, 0) AS BuyDown ,                  
                    CONVERT(DECIMAL, 0) AS BasicBuyDown ,                  
                    CONVERT(DECIMAL, 0) AS RackAllowance ,                  
                    0 AS MaxInventory ,                  
                    0 AS MinInventory ,                  
                    CONVERT(INT, 0) AS CurrentInventory ,                  
                    Convert(smalldatetime,'') InventoryAsOfDate ,                  
                    --'' InventoryAsOfDate ,                  
                    CONVERT(BIGINT, 0) AS StoreLocationItemID ,                  
    CONVERT(BIGINT, 0) AS StoreLocationID ,                  
     '' AS StoreName ,                  
                    CONVERT(BIGINT, 0) AS VendorID,                  
                    0 as POSCodeModifier,                  
                    0.00 RegularPackageSellPrice,                  
                    Case WHEN Item.ItemID = MPack.ContainedItemID THEN 'Pack'                  
                    WHEN Item.ItemID=MCarton.ItemID THEN 'Crtn' ELSE                                    
                    'none' END mulType,                  
                    CONVERT(BIGINT, 0) as MultipackItemID                  
                  
            FROM    Item( NOLOCK )                  
                    INNER JOIN @Dept Department ON Item.DepartmentID = Department.DepartmentID                  
                                                   AND Item.CompanyID = @CompanyID                  
                     --JOIN dbo.DepartmentLocation dl ON dl.DepartmentID=Department.DepartmentID -- and  dl.StoreLocationID                        
                     --JOIN  @Store s ON s.StoreLocationID=dl.StoreLocationID                                                 
                    LEFT OUTER JOIN UOM( NOLOCK ) ON Item.UOMID = UOM.UOMID                  
                    LEFT JOIN Multiplier( NOLOCK ) MCarton on MCarton.ItemID =Item.ItemID              
                    LEFT JOIN Multiplier( NOLOCK ) MPack on MPack.ContainedItemID = Item.ItemID                  
            WHERE   ( ( ISNULL(@posCodeOrDesc, '') = ''                  
                        AND @GroupID IS NULL                  
                        AND LEN(LTRIM(@Vendor)) = 0                  
                      )            
                      OR Item.ItemID IN ( SELECT    itemID                  
                                          FROM      @ItemList )                  
                    )                  
                    AND ( @sellingUnitStart IS NULL                  
                          OR Item.SellingUnits >= @sellingUnitStart                  
                        )                  
                    AND ( @sellingUnitEnd IS NULL                  
                          OR Item.SellingUnits <= @sellingUnitEnd                  
                        )                  
                    AND ( @UnitsInCaseStart IS NULL                  
                          OR Item.UnitsInCase >= @UnitsInCaseStart                  
                        )                  
                    AND ( @UnitsInCaseEnd IS NULL                  
                          OR Item.UnitsInCase <= @UnitsInCaseEnd                  
                        )                  
                    AND ( @isMultipack IS NULL                  
                          OR Item.IsMultipackFlag = @isMultipack                  
                        )                  
                    AND ( @isActive IS NULL                  
                          OR Item.ActiveFlag = @isActive          
                        )                  
                    AND Item.ItemID IN (                  
                    SELECT  ItemID                  
                    FROM    StoreLocationItem( NOLOCK ) SLI                  
                            JOIN @Store StoreLocation ON SLI.StoreLocationID = StoreLocation.StoreLocationID                  
                    WHERE   ( SLI.RegularSellPrice >= @SellingPriceStart                  
                              OR @SellingPriceStart IS NULL                  
                            )                  
                            AND ( SLI.RegularSellPrice <= @SellingPriceEnd                  
                                  OR @SellingPriceEnd IS NULL                  
                                )                  
                            AND ( SLI.InventoryValuePrice >= @InventoryValuePriceStart                  
                                  OR @InventoryValuePriceStart IS NULL                  
                                )                  
                            AND ( SLI.InventoryValuePrice <= @InventoryValuePriceEnd                  
                                  OR @InventoryValuePriceEnd IS NULL                  
                                )                  
                            AND ( SLI.CurrentInventory >= @CurrentInventoryStart                  
                                  OR @CurrentInventoryStart IS NULL                  
                                )                  
                            AND ( SLI.CurrentInventory <= @CurrentInventoryEnd                  
                                  OR @CurrentInventoryEnd IS NULL                  
                                )                  
                            AND ( 0 >= @ProfitMarginStart                  
                                  OR @ProfitMarginStart IS NULL                  
                                )                  
                            AND ( 0 <= @ProfitMarginEnd                  
                                  OR @ProfitMarginEnd IS NULL                  
                                )                  
                            AND ( SLI.POSSyncStatusID = @POSSyncStatus                  
                                  OR @POSSyncStatus IS NULL                  
                                )          
        AND ( @isTrackItem IS NULL                  
                      OR SLI.IsTrackItem = @isTrackItem                  
                    )                    
                         --Added by Jaswanth for POSSyncStatus search                  
                    UNION                  
                    SELECT                    
                         CASE WHEN @POSSyncStatus ='' THEN ItemID                  
                         ELSE 0 END                 
                    FROM    @ItemList                   
                                      
                    --UNION                  
                    --SELECT  Item.ItemID                 
                    --FROM    Item                  
                    --WHERE   CompanyID = @CompanyID                  
                    --        AND NOT EXISTS ( SELECT 1                  
                    --                         FROM   StoreLocationItem sli                  
                    --                                JOIN @Store s ON sli.StoreLocationID = s.StoreLocationID                  
                    --                         WHERE  item.ItemID = sli.ItemID )                   
                                           )                  
          END                   
                  
    ELSE                   
        BEGIN                  
 SELECT  Item.ItemID ,                  
                    Item.CompanyID ,                  
                    Item.DepartmentID ,                  
                    Item.ActiveFlag ,                  
                    Item.POSCode ,                  
                    Item.PosCodeFormatID ,                  
                    Item.UOMID ,                  
                    --Item.POSCode + CAST(dbo.Item.CheckDigit AS VARCHAR(50)) AS POSCodeWithCheckDigit ,                  
                                 
     Item.Description ,                  
                    Item.FamilyUPCCode ,                  
                    Item.SellingUnits ,                  
                    Item.UnitsInCase ,                  
       Item.LastModifiedBy ,                  
                    Item.IsMultipackFlag ,                  
                    Item.NoOfBaseUnitsInCase ,                  
                    Convert(smalldatetime,Item.LastModifiedDateTime) LastModifiedDateTime ,                  
                    Department.DepartmentDescription ,                  
                    UOM.UOMDescription ,                  
                    CONVERT(DECIMAL, 0) AS GrossProfit ,                  
                    CONVERT(BIT, 0) AS IsTrackItem ,                  
                    0.00 AS RegularSellPrice ,                  
                    0.00 AS InventoryValuePrice ,                  
                    CONVERT(DECIMAL, 0) AS BuyDown ,                  
                    CONVERT(DECIMAL, 0) AS BasicBuyDown ,                  
                    CONVERT(DECIMAL, 0) AS RackAllowance ,                  
                    0 AS MaxInventory ,                  
                    0 AS MinInventory ,                  
                    CONVERT(INT, 0) AS CurrentInventory ,                  
                     Convert(smalldatetime,'') InventoryAsOfDate ,                  
                    --'' InventoryAsOfDate ,                  
                    CONVERT(BIGINT, 0) AS StoreLocationItemID ,                  
                    CONVERT(BIGINT, 0) AS StoreLocationID ,                  
                    '' AS StoreName ,                  
                    CONVERT(BIGINT, 0) AS VendorID,                  
                    0 as POSCodeModifier,                  
                    0.00 RegularPackageSellPrice,                  
                    Case WHEN Item.ItemID = MPack.ContainedItemID THEN 'Pack'                  
                    WHEN Item.ItemID=MCarton.ItemID THEN 'Crtn' ELSE                                    
                    'none' END mulType,                  
                     CONVERT(BIGINT, 0) as MultipackItemID                  
            FROM    Item( NOLOCK )                  
                    INNER JOIN @Dept Department ON Item.DepartmentID = Department.DepartmentID                  
                                                   AND Item.CompanyID = @CompanyID                  
                                                                     
                     --JOIN dbo.DepartmentLocation dl ON dl.DepartmentID=Department.DepartmentID -- and  dl.StoreLocationID                        
                     --JOIN  @Store s ON s.StoreLocationID=@Department.StoreLocationID                        
                                                    
                     LEFT JOIN UOM( NOLOCK ) ON Item.UOMID = UOM.UOMID                  
                    LEFT JOIN Multiplier( NOLOCK ) MCarton on MCarton.ItemID =Item.ItemID                  
                    LEFT JOIN Multiplier( NOLOCK ) MPack on MPack.ContainedItemID = Item.ItemID                  
            WHERE   ( ( ISNULL(@posCodeOrDesc, '') = ''                  
                        AND @GroupID IS NULL                  
                        AND LEN(LTRIM(@Vendor)) = 0                  
                      )                  
                      OR Item.ItemID IN ( SELECT    itemID                  
                                          FROM      @ItemList )                  
                    )                  
                    AND ( @sellingUnitStart IS NULL                  
                          OR Item.SellingUnits >= @sellingUnitStart                  
                        )                  
                    AND ( @sellingUnitEnd IS NULL                  
                          OR Item.SellingUnits <= @sellingUnitEnd                  
                        )                  
                    AND ( @UnitsInCaseStart IS NULL                  
                          OR Item.UnitsInCase >= @UnitsInCaseStart                  
)                  
                    AND ( @UnitsInCaseEnd IS NULL                  
                          OR Item.UnitsInCase <= @UnitsInCaseEnd                  
                        )                  
                    AND ( @isMultipack IS NULL                  
                          OR Item.IsMultipackFlag = @isMultipack                  
                        )                  
                    AND ( @isActive IS NULL                  
                          OR Item.ActiveFlag = @isActive                  
                        )           
     AND ( @isShowPricing IS NULL          
        AND @isShowMultiPackPricing IS NULL          
        AND @Location IS NULL          
        AND @isShowDetails IS NULL          
        OR Item.CompanyID = @CompanyID          
        )          
                    AND Item.ItemID IN (                  
                    SELECT  ItemID                  
                FROM    StoreLocationItem( NOLOCK ) SLI                  
                            JOIN @Store StoreLocation ON SLI.StoreLocationID = StoreLocation.StoreLocationID                  
                    WHERE   ( SLI.RegularSellPrice >= @SellingPriceStart                  
                              OR @SellingPriceStart IS NULL                  
                            )                  
                            AND ( SLI.RegularSellPrice <= @SellingPriceEnd                  
                                  OR @SellingPriceEnd IS NULL                  
                                )                  
                            AND ( SLI.InventoryValuePrice >= @InventoryValuePriceStart                  
                                  OR @InventoryValuePriceStart IS NULL                  
                                )                  
                            AND ( SLI.InventoryValuePrice <= @InventoryValuePriceEnd                  
                                  OR @InventoryValuePriceEnd IS NULL                  
                                )                  
                            AND ( SLI.CurrentInventory >= @CurrentInventoryStart                  
                                  OR @CurrentInventoryStart IS NULL                  
                                )                  
                            AND ( SLI.CurrentInventory <= @CurrentInventoryEnd                  
                                  OR @CurrentInventoryEnd IS NULL                  
                                )                  
                            AND ( 0 >= @ProfitMarginStart                  
           OR @ProfitMarginStart IS NULL                  
                 )                  
                            AND ( 0 <= @ProfitMarginEnd                  
                                  OR @ProfitMarginEnd IS NULL                  
                                )                  
                            AND ( SLI.POSSyncStatusID = @POSSyncStatus                  
                                  OR @POSSyncStatus IS NULL                  
                                )         
        AND        
         ( @isTrackItem IS NULL                  
                      OR SLI.IsTrackItem = @isTrackItem                  
                    )                   
                         --Added by Jaswanth for POSSyncStatus search                  
                    UNION                  
                    SELECT                    
                         CASE WHEN @POSSyncStatus ='' THEN ItemID                  
                         ELSE 0 END                   
                    FROM @ItemList                   
                                      
                    -- UNION                  
       -- SELECT  Item.ItemID                  
                    -- FROM    Item                  
                    -- WHERE   CompanyID = @CompanyID                  
                            -- AND NOT EXISTS ( SELECT 1                  
                                             -- FROM   StoreLocationItem sli                  
                                                    -- JOIN @Store s ON sli.StoreLocationID = s.StoreLocationID                  
                                             -- WHERE  item.ItemID = sli.ItemID )                   
                                           )                  
                             
                    
        END                   
                  
 --According to Greeshma RegularSellPrice needs to update in Items after the Schedule completed                       
    --EXEC [spUpdateSellingPriceforPriceSchedule]                  
    --Exec [spUpdateBuyDown]                  
                  
--EXEC spSearchStoreLocationItems 3,0,0,'018200000188',null,null,null,null,null,null,null,null,null,null,null,null,'15,16,17,','','',null,null,null,null,null,0                  
--EXEC spSearchStoreLocationItems 202,1,0,'',null,null,null,null,null,null,null,null,null,null,null,null,'318,','','5158,',null,null,null,null,null,0 
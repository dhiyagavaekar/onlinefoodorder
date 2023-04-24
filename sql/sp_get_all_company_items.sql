    
Declare    
@CompanyId BIGINT=@tempCompanyId,    
@Vendor NVARCHAR(1500) = @tempVendor ,       
@Department NVARCHAR(1500) = @tempDepartment,            
@GroupID BIGINT=@tempGroupID,       
@posCodeOrDesc NVARCHAR(400) = @tempposCodeOrDesc,      
@sellingUnitStart NUMERIC(10, 4) = @temptempsellingUnitStart ,        
@sellingUnitEnd NUMERIC(10, 4) = @tempsellingUnitEnd ,              
@UnitsInCaseStart NUMERIC(10, 4) = @tempUnitsInCaseStart ,         
@UnitsInCaseEnd NUMERIC(10, 4) = @tempUnitsInCaseEnd,      
@isMultipack BIT = @tempisMultipack,       
@isActive BIT = @tempisActive    
                   
                
            
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
                    Convert(smalldatetime,Item.LastModifiedDateTime) LastModifiedDateTime ,                  --Department.DepartmentDescription ,                  --UOM.UOMDescription ,           NUll as GrossProfit ,                  NULL AS IsTrackItem
,                  0.00 AS RegularSellPrice ,    
                 0.00 AS InventoryValuePrice ,   
        
                     0 AS BuyDown ,   
  0 AS BasicBuyDown ,               
       0 AS RackAllowance ,         
      
               0 AS MaxInventory ,                    
0 AS MinInventory ,             
       0 AS CurrentInventory ,    
           Convert(smalldatetime,'') InventoryAsOfDate  ,   
                      0 AS StoreLocationItemID ,      
                        
               0 AS StoreLocationID ,   
           '' AS StoreName ,               
     0 AS VendorID,                  0 AS POSCodeModifier  ,         
             0.00 AS RegularPackageSellPrice  ,       
                --Case WHEN Item.ItemID = MPack.ContainedItemID THEN 'Pack'                  --WHEN Item.ItemID=MCarton.ItemID THEN 'Crtn' ELSE                                    --'none' END mulType,                  CONVERT(BIGINT, 0) as MultipackItemID
 ,                   
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
                   --- JOIN StoreLocationItem( NOLOCK ) SLI ON Item.ItemID = SLI.ItemID                  
                   --- JOIN @Store StoreLocation ON StoreLocation.StoreLocationID = SLI.StoreLocationID                  
                    LEFT JOIN Multiplier( NOLOCK ) MCarton on MCarton.ItemID =Item.ItemID                  
                    LEFT JOIN Multiplier( NOLOCK ) MPack on MPack.ContainedItemID = Item.ItemID                  
                   -- LEFT JOIN @ItemPriceSchedule IPS ON IPS.ItemID = Item.itemID                  
                          --                              AND IPS.StoreLocationID = SLI.StoreLocationID               
            WHERE                   
                                     
                     ( ( ISNULL(@posCodeOrDesc, '') = ''                  
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
            OR Item.SellingUnits <= @sellingUnitEnd                                 )                             AND ( @UnitsInCaseStart IS NULL                                   OR Item.UnitsInCase >= @UnitsInCaseStart                                 ) 
  
                     
           AND ( @UnitsInCaseEnd IS NULL                                   OR Item.UnitsInCase <= @UnitsInCaseEnd          )                             AND ( @isMultipack IS NULL                                   OR     
     Item.IsMultipackFlag = @isMultipack                                 )                             AND ( @isActive IS NULL                                   OR Item.ActiveFlag = @isActive                                 )  
 UPDATE StoreLocationItem  
 SET StoreLocationSalesRestrictionID = @saleRestrictionID,LastModifiedBy=@modifieduser,POSSyncStatusID=@POSSyncStatusID,  
  LastModifiedDateTime=GETDATE()  
 WHERE ItemId IN   
 (SELECT ItemID FROM Item WHERE DepartmentID = @departmentID)  
 AND StoreLocationID=@storeLocationID  
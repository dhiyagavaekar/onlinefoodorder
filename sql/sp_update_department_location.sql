SELECT * FROM vwGetDepartmentLocation   
    WHERE   
    DepartmentID = '<DepartmentID>'  
    And StoreLocationID  
     IN (SELECT StoreLocationID FROM   
     funcGetStoresForUser('<CompanyID>','<UserName>'))
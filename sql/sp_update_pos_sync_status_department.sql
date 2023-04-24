UPDATE  StoreLocationItem  
 SET     POSSyncStatusID =( 
            CASE WHEN((RegularSellPrice=0) 
                  OR (RegularSellPrice IS NULL)
                  OR (i.ActiveFlag=0) ) 
                  THEN 
                     1 
                  ELSE  
                     ( @POSSyncStatusID) 
                  END),  
         LastModifiedBy=@modifieduser,  
      LastModifiedDateTime=GETDATE()  
        
      FROM dbo.StoreLocationItem sli  
         JOIN dbo.Item i ON i.ItemID = sli.ItemID  
           
 WHERE   sli.ItemID IN ( 
   SELECT  ItemID FROM Item  
      WHERE DepartmentID IN(SELECT *  
      FROM    dbo.GetTableFromCommaString(@deplst, ',')) )  
   AND
    StoreLocationID IN (  
   SELECT  *  
   FROM    dbo.GetTableFromCommaString(@storelst, ',') )  
  
 
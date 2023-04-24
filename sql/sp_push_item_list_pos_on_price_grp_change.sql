Update ms   
  
set POSSyncStatusID=2,  
LastModifiedBy=@UserName,  
LastModifiedDateTime=GETDATE()  
 from MixMatchStoreLocation ms   
  join  MixMatch m on m.MixmatchID=ms.MixMatchID  
  
where ItemListID in (select itemListID from ItemListGroup  where CompanyPriceGroupID=@CompanyPriceGroupID)  
  
  
Update cs  
set POSSyncStatusID=2,  
LastModifiedBy=@UserName,  
LastModifiedDateTime=GETDATE()  
from ComboDealStoreLocation cs  
join ComboDeal c on c.ComboDealID= cs.ComboDealID  
where ItemListID in (select itemListID from ItemListGroup  where CompanyPriceGroupID=@CompanyPriceGroupID)  
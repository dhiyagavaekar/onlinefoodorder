DECLARE @GetPermittedUserStoreLocations TABLE              
        (              
          StoreLocationID BIGINT,              
          StoreName varchar(100)              
        );              
       INSERT  INTO @GetPermittedUserStoreLocations              
    SELECT * FROM funcGetStoresForUser(@companyID,@UserName)              
                            
;               
With               
AllStores              
as              
(              
             
  select dl.storelocationId,sl.StoreName,sl.POSSystemCD,sl.StoreFullName,sl.CompanyID from @GetPermittedUserStoreLocations dl              
  join StoreLocation sl on dl.storelocationId=sl.StoreLocationID              
          
              
) ,              
SLI as              
(              
select mm.* ,              
st.StoreName,              
mu.MixMatchPromotionUnitTypeName,              
        
ps.POSSyncStatusCode   ,           
              
    m.Description as  MixMatchName        
         
            
from MixMatchStoreLocation mm            
join mixmatch m on m.MixmatchID= mm.mixMatchID          
inner join @GetPermittedUserStoreLocations st on mm.StoreLocationID =st.StoreLocationID              
left join MixMatchPromotionUnitType mu on  mu.MixMatchPromotionUnitTypeID =mm.MixMatchPromotionUnitTypeID               
left join POSSyncStatus ps on ps.POSSyncStatusID= mm.POSSyncStatusID              
  where m.MixMatchID =@MixMatchID            
)              
               
           
              
select              
                      
als.StoreName,              
ps.POSSyncStatusID,              
pss.possystemname,              
ps.POSSyncStatusCode,              
            
sli.MixMatchPromotionUnitTypeID,              
IsNull (sli.MixMatchStoreLocationID ,null) MixMatchStoreLocationID,          
sli.MixMatchName,          
        
        
sli.MixMatchID,        
sli.MixMatchPromotionUnitTypeName,              
als.StoreLocationID,         
sli.POSID,             
IsNull(sli.BeginDate,Null) BeginDate,              
ISNull(sli.EndDate,Null) EndDate,              
IsNull(sli.MixMatchAmount ,null) MixMatchAmount,              
IsNull(sli.MixMatchUnits,null) MixMatchUnits,              
IsNUll(sli.LastModifiedDateTime, Null) LastModifiedDateTime,              
IsNull(sli.ManufacturerFunded, Null) ManufacturerFunded,              
IsNull(sli.RetailerFunded , Null) RetailerFunded,              
IsNull (sli.Co_funded, Null) Co_funded,              
  (case               
  when sli.StoreLocationID is null then              
   255              
  else              
   ROW_NUMBER() OVER(ORDER BY als.StoreName)              
  end) SrNO,              
  (case               
  when sli.StoreLocationID is null then              
   CONVERT(bit,0)              
  else              
   CONVERT(bit,1)              
  end) StoreExists              
              
                
from AllStores als              
               
left join   sli  on als.StoreLocationID= sli.StoreLocationID              
left join POSSyncStatus  ps on ps.POSSyncStatusID = sli.POSSyncStatusID              
inner JOIN  POSSystem pss ON als.POSSystemCD = pss.POSSystemCD
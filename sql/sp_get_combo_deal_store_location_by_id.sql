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
select                   
 st.StoreName,                  
cs.*,  cp.ComboPriorityTypeName,ct.ComboTypeName,                
            
ps.POSSyncStatusCode   ,               
                  
    c.Description as ComboDealName            
             
                
 from ComboDealStorelocation cs                
 join ComboDeal c on c.ComboDealID= cs.ComboDealID              
 inner join @GetPermittedUserStoreLocations st on cs.StoreLocationID =st.StoreLocationID                  
 left join ComboPriorityType cp on  cp.ComboPriorityTypeID =cs.ComboPriorityTypeID      
      left join ComboType ct on  ct.ComboTypeID =cs.ComboTypeID                         
 left join POSSyncStatus ps on ps.POSSyncStatusID= cs.POSSyncStatusID                  
  where c.ComboDealID =@ComboDealID                
)                  
                   
               
                  
select                                                 
als.StoreName,                  
ps.POSSyncStatusID,                  
pss.possystemname,                  
ps.POSSyncStatusCode,                  
sli.ComboPriorityTypeName,sli.ComboTypeName,                
                
IsNull (sli.ComboDealStoreLocationID ,null) ComboDealStoreLocationID,              
sli.ComboDealName,              
            
sli.ComboPriorityTypeID  ,          
sli.ComboDealID,            
                
als.StoreLocationID,             
sli.POSID,                 
IsNull(sli.BeginDate,Null) BeginDate,                  
ISNull(sli.EndDate,Null) EndDate,                  
IsNull(sli.ComboAmount ,null) ComboAmount,                  
IsNull(sli.ComboUnits,null) ComboUnits,                  
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
 order by ComboDealName  
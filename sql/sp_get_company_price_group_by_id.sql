select COUNT(ig.ItemID) as NOOfItems ,cg.* ,d.DepartmentDescription,d.DepartmentID       
from CompanyPriceGroup cg             
left join ItemPriceGroup ig on cg.CompanyPriceGroupID = ig.PriceGroupID    
left join Item i on i.ItemID=ig.ItemID  
left Join Department d on d.DepartmentID=i.DepartmentID  
where cg.CompanyID=@CompanyID       
group By CompanyPriceGroupID,CompanyPriceGroupName,masterPriceGroupID,IsSuperGroup,GroupIDs,cg.CompanyID,ManufacturerID,FromAPI,IsActive,d.DepartmentID,DepartmentDescription         
order by cg.CompanyPriceGroupName     
     
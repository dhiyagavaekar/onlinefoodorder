from pydantic import BaseModel,validator,ValidationError
from datetime import datetime
from typing import Optional
from configurations import database as config_db
# from api.company import validators
# Create Company Schema (Pydantic Model)
class CompanyCreate(BaseModel):
    CompanyLoginCode:  Optional[str] = None
    CompanyTaxID:  Optional[str] = None        
    CompanyName:  Optional[str] = None         
    CompanyAddressLine1:  Optional[str] = None 
    CompanyAddressLine2:  Optional[str] = None 
    City:  Optional[str] = None                
    CountyCode:  Optional[str] = None          
    StateCode:  Optional[str] = None           
    E_Mail:  Optional[str] = None              
    PhoneNo:  Optional[str] = None             
    Fax:  Optional[str] = None                 
    SyncUser:  Optional[str] = None            
    SyncPwd:  Optional[str] = None             
    EnableMobileLogging: Optional[bool] = None 
    IsInPOSSyncStatus: Optional[bool] = None   
    IsJobber: Optional[bool] = None            
    ZIPCode:  Optional[str] = None             

class CompanyUpdate(BaseModel):
    CompanyLoginCode:  Optional[str] = None
    CompanyTaxID:  Optional[str] = None        
    CompanyName:  Optional[str] = None         
    CompanyAddressLine1:  Optional[str] = None 
    CompanyAddressLine2:  Optional[str] = None 
    City:  Optional[str] = None                
    CountyCode:  Optional[str] = None          
    StateCode:  Optional[str] = None           
    E_Mail:  Optional[str] = None              
    PhoneNo:  Optional[str] = None             
    Fax:  Optional[str] = None                 
    SyncUser:  Optional[str] = None            
    SyncPwd:  Optional[str] = None             
    EnableMobileLogging: Optional[bool] = None 
    IsInPOSSyncStatus: Optional[bool] = None   
    IsJobber: Optional[bool] = None            
    ZIPCode:  Optional[str] = None
    IsActive: Optional[bool] = None                 

class Company(BaseModel):
    CompanyID: Optional[int] = None
    CompanyLoginCode:  Optional[str] = None
    CompanyTaxID:  Optional[str] = None        
    CompanyName:  Optional[str] = None         
    CompanyAddressLine1:  Optional[str] = None 
    CompanyAddressLine2:  Optional[str] = None 
    City:  Optional[str] = None                
    CountyCode:  Optional[str] = None          
    StateCode:  Optional[str] = None           
    E_Mail:  Optional[str] = None              
    PhoneNo:  Optional[str] = None             
    Fax:  Optional[str] = None                 
    SyncUser:  Optional[str] = None            
    SyncPwd:  Optional[str] = None             
    EnableMobileLogging: Optional[bool] = None 
    IsInPOSSyncStatus: Optional[bool] = None   
    IsJobber: Optional[bool] = None            
    ZIPCode:  Optional[str] = None             
    IsActive: Optional[bool] = None

    class Config:
        orm_mode = True
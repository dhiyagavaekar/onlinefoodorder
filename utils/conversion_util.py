def convert_pagination_sql(data,inputJson,pageNumber,noOfRecords):

    companyID = inputJson['companyID']
    storelocId = inputJson['locationCriteria']
    departmentId = inputJson['department']


    if departmentId is None or departmentId == "":
        data = data.replace("dl.DepartmentID in ('<departmentid>') AND","").replace("Item.DepartmentID IN ('<departmentid>') AND","")
    else:
        data = data.replace('<departmentid>',str(departmentId))
    
    data = data.replace('<storelocation>',str(storelocId)).replace('<companyid>',str(companyID))


    if inputJson['isOnWatchList'] is None or inputJson['isOnWatchList'] == "":
        data = data.replace("AND SLI.IsTrackItem = <IsTrackItem>","")
    else:
        data = data.replace("<IsTrackItem>",inputJson['IsTrackItem'])

    
    if inputJson['posSyncStatus'] is None or inputJson['posSyncStatus'] == "":
        data = data.replace("AND SLI.POSSyncStatusID = <POSSyncStatusID>","")
    else:
        data = data.replace("<POSSyncStatusID>",str(inputJson['posSyncStatus']))
    

    if inputJson['isMultipack'] is None or inputJson['isMultipack'] == "":
        data = data.replace("AND SLI.IsMultipackFlag = '<IsMultipackFlag>'","")
    else:
        data = data.replace("<IsMultipackFlag>",str(inputJson['isMultipack']))
    
    if inputJson['sellingUnitStart'] is None or inputJson['sellingUnitStart'] == "":
        data = data.replace("AND Item.SellingUnits >= <sellingUnitStart>","")
    else:
        data = data.replace("<sellingUnitStart>",str(inputJson['sellingUnitStart']))
    
    if inputJson['sellingUnitEnd'] is None or inputJson['sellingUnitEnd'] == "":
        data = data.replace("AND Item.SellingUnits <= <sellingUnitEnd>","")
    else:
        data = data.replace("<sellingUnitEnd>",str(inputJson['sellingUnitEnd']))
    

    if inputJson['unitsInCaseStart'] is None or inputJson['unitsInCaseStart'] == "":
        data = data.replace("AND Item.UnitsInCase >= <UnitsInCaseStart>","")
    else:
        data = data.replace("<UnitsInCaseStart>",str(inputJson['unitsInCaseStart']))
    
    if inputJson['unitsInCaseEnd'] is None or inputJson['unitsInCaseEnd'] == "":
        data = data.replace("AND Item.UnitsInCase <= <UnitsInCaseEnd>","")
    else:
        data = data.replace("<UnitsInCaseEnd>",str(inputJson['unitsInCaseEnd']))

    
    if inputJson['sellingPriceStart'] is None or inputJson['sellingPriceStart'] == "":
        data = data.replace("AND ROUND(SLI.RegularSellPrice, 2) >= <SellingPriceStart>","")
    else:
        data = data.replace("<SellingPriceStart>",str(inputJson['sellingPriceStart']))
    
    if inputJson['sellingPriceEnd'] is None or inputJson['sellingPriceEnd'] == "":
        data = data.replace("AND ROUND(SLI.RegularSellPrice, 2) <= <SellingPriceEnd>","")
    else:
        data = data.replace("<SellingPriceEnd>",str(inputJson['sellingPriceEnd']))

    
    if inputJson['inventoryValuePriceStart'] is None or inputJson['inventoryValuePriceStart'] == "":
        data = data.replace("AND ROUND(SLI.InventoryValuePrice, 2) >= <InventoryValuePriceStart>","")
    else:
        data = data.replace("<InventoryValuePriceStart>",str(inputJson['inventoryValuePriceStart']))
    
    if inputJson['inventoryValuePriceEnd'] is None or inputJson['inventoryValuePriceEnd'] == "":
        data = data.replace("AND ROUND(SLI.InventoryValuePrice, 2) <= <InventoryValuePriceEnd>","")
    else:
        data = data.replace("<InventoryValuePriceEnd>",str(inputJson['inventoryValuePriceEnd']))

    if inputJson['currentInventoryStart'] is None or inputJson['currentInventoryStart'] == "":
        data = data.replace("AND ROUND(SLI.CurrentInventory, 2) >= <CurrentInventoryStart>","")
    else:
        data = data.replace("<CurrentInventoryStart>",str(inputJson['currentInventoryStart']))
    
    if inputJson['currentInventoryEnd'] is None or inputJson['currentInventoryEnd'] == "":
        data = data.replace("AND ROUND(SLI.CurrentInventory, 2) <= <CurrentInventoryEnd>","")
    else:
        data = data.replace("<CurrentInventoryEnd>",str(inputJson['currentInventoryEnd']))
    

    if inputJson['pMStartCriteria'] is None or inputJson['pMStartCriteria'] == "":
        data = data.replace("AND ProfitMargin >= <ProfitMarginStart>","")
    else:
        data = data.replace("<ProfitMarginStart>",str(inputJson['pMStartCriteria']))
    
    if inputJson['pmEndCriteria'] is None or inputJson['pmEndCriteria'] == "":
        data = data.replace("AND ProfitMargin <= <ProfitMarginEnd>","")
    else:
        data = data.replace("<ProfitMarginEnd>",str(inputJson['pmEndCriteria']))
    


    data = data.replace("<pagenumber>",str(pageNumber)).replace("<records>",str(noOfRecords))
    

    data = data.replace('\n',"  ").strip() 

    return data
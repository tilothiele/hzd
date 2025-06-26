import requests

region = "Nord"

filterParams1 = {
    "animal": 0
}

filterParams = {
    "animal": 0,
    "animalFilter[name]": "",
    "animalFilter[breedingStation]": "",
    "animalFilter[studbook]": "",
    "animalFilter[chipNumber]": "",
    "animalFilter[identitycontrol]": "",
    "animalFilter[studbookNumber]": "",
    "animalFilter[stdbkSectionID]": -1,
    "animalFilter[breedID]": -1,
    "animalFilter[sexID]": -1,
    "animalFilter[virtual]": -1,
    "animalFilter[age]": -1,
    "animalFilter[bdateFrom]": "",
    "animalFilter[bdateTo]": "",
    "animalFilter[ddateFrom]": "",
    "animalFilter[ddateTo]": "",
    "animalFilter[fertile]": 0,
    "animalFilter[onlyDeadAnimals]": 0,
    "animalFilter[breederLastName]": "",
    "animalFilter[breederMembershipNumber]": "",
    "animalFilter[ownerLastName]": "",
    "animalFilter[ownerMembershipNumber]": "",
    "animalFilter[breedingDisqualification]": 0,
    "animalFilter[cullingReasonID]": -1,
    "animalFilter[determinationID]": -1,
    "animalFilter[colourID]": -1,
    "personFilter[lastname]": "",
    "personFilter[breeder]": 0,
    "personFilter[activeBreeder]": 0,
    "personFilter[breederStation]": "",
    "personFilter[organizationID]": -1,
    "personFilter[countryID]": -1,
    "personFilter[federalState]": "",
    "personFilter[rayon]": "",
    "personFilter[oblast]": region,
    "personFilter[bdateFrom]": "",
    "personFilter[bdateTo]": "",
    "personFilter[ddateFrom]": "",
    "personFilter[ddateTo]": "",
    "personParam[memberOfAssos]": 0,
    "personParam[activeMember]": 0,
    "personParam[membershipNumber]": "",
    "personParam[memStatusID]": -1,
    "personParam[roleID]": -1,
    "personParam[otherRole]": "",
    "personParam[jdateFrom]": "",
    "personParam[jdateTo]": "",
    "personParam[ldateFrom]": "",
    "personParam[ldateTo]": "",
    "personParam[perfjudge]": 0,
    "personParam[showjudge]": 0,
    "personParam[subscriber]": 0,
    "personParam[subscriberID]": -1,
}

saveSearchListParams = {
    "groupTypeID": 5,
    "sendEmail": 0,
    "exportCsv": 1,
    "exportXls": 0,
    "selectAll": 1,
    "valid": 1,
    "animal": 0,
    "and": 1,
    "searchStr": ""
}

formDataHeaders = {
    "Content-Type": "application/x-www-form-urlencoded"
}

def search(phpsessid, ci_session):
    # Cookies setzen
    cookies = {
        "PHPSESSID": phpsessid,
        "ci_session": ci_session
    }

    response = requests.post("https://hzd.chromosoft.de/powersearch/json_storePSFilters", data=filterParams1, cookies=cookies, headers=formDataHeaders);

    print(response.status_code)
    #print(response.text)

    response = requests.post("https://hzd.chromosoft.de/powersearch/json_saveSearchList", data=saveSearchListParams, cookies=cookies, headers=formDataHeaders);

    print(response.status_code)
    #print(response.text)

    searchMeta = response.json()
    print(searchMeta)
    groupId = searchMeta.data

    downloadParams = {
        groupId: groupId,
        group: 1
    }

    response = requests.post("https://hzd.chromosoft.de/powersearch/json_downloadCSVByGroup", data=downloadParams, cookies=cookies, headers=formDataHeaders);

    print(response.status_code)
    #print(response.text)

    downloadMeta = response.json()
    print(downloadMeta)


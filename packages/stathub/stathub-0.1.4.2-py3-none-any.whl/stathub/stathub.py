def getdata(dataflow,version="1.0",start="",end="",language="th",label='name'):
    import requests
    import io
    import pandas as pd
    if (end != ""):
        end = "&endPeriod="+str(end)
    if (label == "name"):
        nlabel = "both"
    else:
        nlabel = label
        
    r=requests.get("https://ns1-stathub.nso.go.th/rest/data/TNSO,"+dataflow+","+version+"/?startPeriod="+str(start)+end+"&dimensionAtObservation=AllDimensions",
                   headers={"Accept":"application/vnd.sdmx.data+csv;file=true;labels="+nlabel,"Accept-Language" : language}).content
    rawData = pd.read_csv(io.StringIO(r.decode('utf-8')))
    if(label=="name"):
        nrow = rawData.shape[0]
        ncol = rawData.shape[1]
        for i in range(0,nrow):
            for j in range(0,ncol):
                element = str(rawData.iat[i,j]).split(": ")
                if (len(element)>1):
                    rawData.iat[i,j] = element[1]
        names = list(rawData.columns)
        for i in range(0,len(names)):
            element = str(names[i]).split(": ")
            if (len(element)>1):
                names[i] = element[1]
        rawData.columns = names
    return rawData

def dataexport(data,path="",exporttype='csv'):
    import pandas as pd
    if (exporttype=='csv'):
        out = path+"output.csv"
        data.to_csv(out, index=False, header=True, mode='a')
    elif (exporttype=='excel'):
        out = path+"output.xlsx"
        data.to_excel(out, index=False, header=True)

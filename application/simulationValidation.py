def __validEmpty(value):
    if value == "" or value == None:
        return False
    return True

def __validFloat(value):
    try:
        if float(value) < 0:
            return "Negative number"
    except ValueError:
        return "Not a number"
    return None
    
def __validInt(value):
    try:
        if int(value) < 1:
            return "Less than 1"
    except ValueError:
        return "Not a number"
    return None


def simulationValidation(initialInvestment, investmentAmount, investmentInterval, investmentPeriod, stockData):
    returnStatus = [None, None, None, None, None]
    
    if __validEmpty(initialInvestment):
        returnStatus[0] = __validFloat(initialInvestment)
    else:
        returnStatus[0] = "No data"

    if __validEmpty(investmentAmount):
        returnStatus[1] = __validFloat(investmentAmount)
    else:
        returnStatus[1] = "No data"

    if __validEmpty(investmentInterval):
        returnStatus[2] = __validInt(investmentInterval)
    else:
        returnStatus[2] = "No data"
    
    if __validEmpty(investmentPeriod):
        returnStatus[3] = __validInt(investmentPeriod)
    else:
        returnStatus[3] = "No data"

    if stockData is None:
        returnStatus[4] = "Stock not found"
    
    return returnStatus
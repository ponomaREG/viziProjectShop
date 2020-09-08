


def buildSqlQueryByTags(baseSqlQuery,tags):
    resultQuery = "{} where ".format(baseSqlQuery)
    for i in range(len(tags)-1):
        resultQuery +=  "like '%{}%' and ".format(tags[i])
    resultQuery += "like '%{}%';".format(tags[len(tags)-1])
    return resultQuery





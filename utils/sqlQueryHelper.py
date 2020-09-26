


def buildSqlQueryByTags(baseSqlQuery,tags):
    resultQuery = "{} where ".format(baseSqlQuery)
    for i in range(len(tags)-1):
        resultQuery +=  "tags like '%{}%' and ".format(tags[i])
    resultQuery += "tags like '%{}%';".format(tags[len(tags)-1])
    return resultQuery

def buildSqlQueryByTagsAndPage(baseSqlQuery,tags,page,offset):
    buildedSqlWithoutOffset = buildSqlQueryByTags(baseSqlQuery,tags)
    buildedSqlWithoutOffset = buildedSqlWithoutOffset[:len(buildedSqlWithoutOffset)-1]
    buildedSqlWithoutOffset += " order by rate DESC LIMIT {1} OFFSET {2};".format(offset,offset*(page-1))
    return buildedSqlWithoutOffset





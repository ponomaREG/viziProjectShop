


def makeArrayOfTagsToStr(tags):
    if(len(tags) == 0):
        return ''
    else:
        tagsStr = ''
        for i in range(len(tags)):
            tagsStr += tags[i]
            if(i != len(tags)-1):
                tagsStr += ','
        return tagsStr

def makeTagsStrToArray(tagStr):
    return tagStr.split(',')


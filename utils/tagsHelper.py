


def makeArrayOfTagsToStr(tags):
    if(len(tags) == 0):
        return ''
    else:
        tagsStr = ''
        for tag in tags:
            tagsStr += tag
            tagsStr += ','
        return tagsStr

def makeTagsStrToArray(tagStr):
    return tagStr.split(',')


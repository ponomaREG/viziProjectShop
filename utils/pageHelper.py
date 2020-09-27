


def getRangeOfPages(countOfPages,currentPage):
    if(currentPage + 1 <=countOfPages) and (currentPage - 1 > 0):
            return range(currentPage-1,currentPage+2)
    elif(currentPage + 1 <= countOfPages):
            return range(currentPage,currentPage+2)
    elif(currentPage - 1 > 0):
        return range(currentPage-1,currentPage+1)
    else:
        return range(currentPage,currentPage+1)
    

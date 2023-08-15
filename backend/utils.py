def paginate(result_list, pageNum, pageSize):
    page_num = 1
    page_size = len(result_list)

    page_num = int(pageNum) if pageNum else page_num

    page_size = int(pageSize) if pageSize else page_size

    start = (page_num - 1) * page_size
    end = start + page_size
    return result_list[slice(start, end)]



def search_in_list(list, search_item):

    """Method 1"""

    # for item in list:
    #     if item.url == search_item.url:
    #         if item.price == search_item.price:
    #             return True

    """Method 2"""
    for item in list:
        if item.price == search_item.price and item.img == search_item.img:
            return True
    return False


def diff_list(item_list, new_list):
    diff_list = []
    for item in new_list:
        isOld = search_in_list(item_list, item)
        if not isOld:
            diff_list.append(item)
    return diff_list



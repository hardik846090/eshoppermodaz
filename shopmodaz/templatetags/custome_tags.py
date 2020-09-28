from django import template

register = template.Library()


@register.simple_tag
def to_dict(value):
    """converts string  to dict"""
    return eval(value)


@register.simple_tag
def to_str(value):
    """converts string  to dict"""
    return str(value)

@register.simple_tag
def listConverter(value):
    listConverter = list(str(value[1:len(value) - 1]).split(","))
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", listConverter)

    return listConverter


@register.filter(name='split')
def split(value, key):
    return value.split(key)


@register.simple_tag
def sizequantity(size,quantity):

    # print("$$$$$$$$$$$$$$", size, type(size))
    # print("VVVVVVVVVVVV", quantity, type(quantity))

    size = list(str(size[1:len(size) - 1]).split(","))
    quantity = list(str(quantity[1:len(quantity) - 1]).split(","))


    # color = list(str(color[1:len(color) - 1]).split(","))


    dict = {}
    lensize = len(size)
    for i in range(lensize):
        dict[size[i]]=quantity[i]
    print(">>>>>>>>><<<<<<<MMMMMMMMMMMMMMMM???????????????",dict)


    # colordict = {}
    # lencolor = len(color)
    # for i in range(lencolor):
    #     dict[color[i]] = quantity[i]
    # print(">>>>>>>>VVVVVVVVV", colordict)


    return dict

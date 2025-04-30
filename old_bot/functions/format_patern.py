def text_is_cart_number(text:str)->bool:
    "check input is 16 digit cart number "
    text = text.replace(" ", "")
    text = text.replace("-", "")
    text = text.replace("_", "")
    text = text.replace(",", "")
    return len(text) == 16 and text.isdigit()

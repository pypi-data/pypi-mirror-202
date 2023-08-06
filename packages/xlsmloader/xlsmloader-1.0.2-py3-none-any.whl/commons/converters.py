import math

def province_converter(source_province: str):
    province = source_province.upper()
    if province == "YUKON":
        return "YT"
    if province == "YUKON TERRITORY":
        return "YT"
    else:
        return source_province

def requeriment_type_converter(source_requeriment_type: str):
    if type(source_requeriment_type) == float and math.isnan(source_requeriment_type):
        return None
    elif source_requeriment_type.upper() == "LIFECYCLE REPLACEMENT":
        return "Lifecycle"
    else:
        return source_requeriment_type
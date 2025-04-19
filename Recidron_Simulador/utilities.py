from data_base.data_base_manager import DataBaseConnector


def generate_random_color_hex():
    import random
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
def calculate_concentration_by_object_type(object_type: str,db: DataBaseConnector) -> int:
    data = db.get_records_by_object_type(object_type)
    return sum(item[4]for item in data)
#generete random color by desing parten 
def generate_random_color_hex_by_design_parten(): pass

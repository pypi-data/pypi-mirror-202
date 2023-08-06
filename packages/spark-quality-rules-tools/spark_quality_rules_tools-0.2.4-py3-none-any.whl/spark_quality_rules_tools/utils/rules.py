import warnings

warnings.filterwarnings('always')
warnings.filterwarnings('ignore')


def get_validate_rules(hocons_dir=None):
    import os
    import sys
    import json
    from spark_quality_rules_tools.utils import BASE_DIR
    from pyhocon.converter import HOCONConverter
    from pyhocon import ConfigFactory
    from prettytable import PrettyTable

    is_windows = sys.platform.startswith('win')
    dir_default_rules = os.path.join(BASE_DIR, "utils", "resource", "rules.json")
    file_conf = hocons_dir

    if hocons_dir in ("", None):
        raise Exception(f'required variable hocons_dir')

    if is_windows:
        dir_default_rules = dir_default_rules.replace("\\", "/")
        file_conf = file_conf.replace("\\", "/")

    with open(dir_default_rules) as f:
        default_rules = json.load(f)

    file_conf = ConfigFactory.parse_file(file_conf)
    file_conf = HOCONConverter.to_json(file_conf)
    file_conf = json.loads(file_conf)
    haas_rules = file_conf["hammurabi"]["rules"]

    rules_default_properties = default_rules["rules_common_properties"][0]

    for haas_rule in haas_rules:
        haas_class = str(haas_rule["class"])
        haas_columns = haas_rule["config"]
        haas_rules_type = str(haas_class).split(".")[4]
        haas_rules_class = str(haas_class).split(".")[5]

        rules_version = default_rules["rules_config"][haas_rules_type][haas_rules_class][0]["rules_version"]
        rules_columns = default_rules["rules_config"][haas_rules_type][haas_rules_class][0]["rules_columns"][0]
        rules_columns_all = {**rules_columns, **rules_default_properties}

        print("type=>", haas_rules_type, "class=>", haas_rules_class, "version=>", rules_version)

        t = PrettyTable()
        t.field_names = [f"Variable", "Value", "Dtype Actual", "Dtype Esperado", "Es Obligatorio"]

        if 'id' not in haas_columns.keys():
            print("variable id: no existe")
        else:
            print("variable id:", haas_columns["id"])

        for col, value in haas_columns.items():
            if not str(col) in rules_columns_all.keys():
                t.add_row([col, value, str(type(col)), "Deprecado", "false"])

        for col, value in haas_columns.items():
            if str(col) in rules_columns_all.keys():
                t.add_row([col, value, str(type(value)), rules_columns_all[col][0], rules_columns_all[col][1]])
        print(t)

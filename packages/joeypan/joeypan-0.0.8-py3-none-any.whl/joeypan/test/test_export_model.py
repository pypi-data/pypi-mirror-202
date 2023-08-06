import os

from config.settings import SettingsFactory, inject_settings

os.system("pip install sqlacodegen")


def test_export():
    # sqlacodegen版本不兼容python3.11
    # 需要修改sqlacodegen.codegen#9 -> from inspect import FullArgSpec as ArgSpec
    inject_settings.set_default_log_dir(r"./logs")
    s = SettingsFactory.default()
    cmd = f"sqlacodegen {s.datasource.url.split('?')[0]} > models.py"
    print(cmd)
    os.system(cmd)

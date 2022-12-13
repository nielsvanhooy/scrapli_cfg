from scrapli_community.huawei.vrp.sync_driver import default_sync_on_open, default_sync_on_close
from scrapli_community.huawei.vrp.huawei_vrp import DEFAULT_PRIVILEGE_LEVELS as VRP_DEFAULT_PRIVILEGE_LEVELS
from scrapli_community.huawei.vrp.sync_driver import HuaweiVRPDriver

from scrapli_cfg import ScrapliCfg


def make_connection_scrapli():
    my_device = {
        "host": "10.1.1.131",
        "auth_username": "lagen008",
        "auth_password": "lagen008",
        "auth_strict_key": False,
        "privilege_levels": VRP_DEFAULT_PRIVILEGE_LEVELS,
        "default_desired_privilege_level": "privilege_exec",
        "ssh_config_file": "config",
        "on_open": default_sync_on_open,
        "on_close": default_sync_on_close,
    }

    conn = HuaweiVRPDriver(**my_device)
    conn.open()
    conn.send_command("show users")
    cfg_conn = ScrapliCfg(conn=conn)
    cfg_conn.prepare()
    cfg_result = cfg_conn.get_config(source="startup")
    loeloe = "lala"


make_connection_scrapli()

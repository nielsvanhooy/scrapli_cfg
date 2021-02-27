"""scrapli_cfg.examples.basic_usage.iosxe_config_replace"""
from scrapli import Scrapli
from scrapli_cfg.platform.core.cisco_iosxe import ScrapliCfgIOSXE

DEVICE = {
    "host": "172.18.0.11",
    "auth_username": "vrnetlab",
    "auth_password": "VR-netlab9",
    "auth_strict_key": False,
    "platform": "cisco_iosxe",
}


def main():
    """Demo basic config replace functionality"""

    # load up a config to use for the candidate config
    with open("config", "r") as f:
        my_config = f.read()

    # open the "normal" scrapli connection
    conn = Scrapli(**DEVICE)

    # create the scrapli cfg object, passing in the scrapli connection
    cfg_conn = ScrapliCfgIOSXE(conn=conn)

    # open the scrapli cfg object (opens the underlying scrapli object)
    cfg_conn.open()

    # load up the new candidate config, set replace to True
    cfg_conn.load_config(config=my_config, replace=True)

    # get a diff from the device
    diff = cfg_conn.diff_config()

    # print out the different types of diffs; sometimes the "side by side" and "unified" diffs can
    # be dumb as they only know what you are sending and what is on the device, but have no context
    # about what is getting added or removed. in theory the "device_diff" is smarter because it is
    # what the actual device can give us, though this varies from vendor to vendor!
    print(diff.device_diff)
    print(diff.side_by_side_diff)
    print(diff.side_by_side_diff)

    # if you are happy you can commit the config, or if not you can use `abort_config` to abort
    cfg_conn.commit_config()

    # close it all down when done!
    cfg_conn.close()


if __name__ == "__main__":
    main()
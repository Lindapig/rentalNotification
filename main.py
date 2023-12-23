from my_email import Email
from my_parse import ParseBayonneBay
from utils import load_config
from config_path import CONFIG_PATH
import datetime
import time


def main_function():
    config = load_config(CONFIG_PATH)

    email = Email(config)
    parse_bb = ParseBayonneBay(config)

    website = "https://bestrentnj.com/Communities/Bayonne-Bay/"

    apt_link = parse_bb.parse_apt_link(website)

    content = parse_bb.parse_apt_detail(apt_link)
    email.send_email(content)


def run_forever():
    while True:
        current_hour = datetime.datetime.now().hour
        if 7 <= current_hour < 19:
            # Daytime hours, run every 2 hours
            main_function()
            time.sleep(2 * 3600)  # Sleep for 2 hours
        else:
            # Nighttime hours, run every 8 hours
            main_function()
            time.sleep(8 * 3600)  # Sleep for 8 hours


if __name__ == "__main__":
    main_function()
    # run_forever()

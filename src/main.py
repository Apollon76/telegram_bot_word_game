import configparser


def main():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    api_key = config[config.default_section]['api_key']


if __name__ == '__main__':
    main()

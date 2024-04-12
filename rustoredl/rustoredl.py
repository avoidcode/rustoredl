#!/usr/bin/python3

import requests
import argparse
import random
import functools
import pathlib
import shutil
from tqdm.auto import tqdm


def get_random_hex(length):
    return ''.join([random.choice("0123456789abcdef") for _ in range(length)])


BASE_URL = "https://backapi.rustore.ru/"

MIMIC_HEADERS = {
    "Deviceid": get_random_hex(16) + "--" + str(random.randrange(100000000, 999999999)),
    "Firmwarever": "11",
    "Devicemodel": "Pixel A4",
    "Firmwarelang": "en",
    "Rustorevercode": "251",
    "Devicetype": "mobile",
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "okhttp/4.10.0"
}


def get_appid(package_name):
    info_url = BASE_URL + "applicationData/overallInfo/" + package_name
    response = requests.get(info_url, headers=MIMIC_HEADERS)
    return response.json()["body"]["appId"]


def get_download_links(app_id):
    download_url = BASE_URL + "applicationData/v2/download-link"
    json_data = {
        "appId": app_id,
        "firstInstall": False,
        "withoutSplits": False
    }
    response = requests.post(download_url, headers=MIMIC_HEADERS, json=json_data)
    urls = response.json()["body"]["downloadUrls"]
    return [url["url"] for url in urls]


def download_file(url, filename):
    response = requests.get(url, stream=True, allow_redirects=True)
    if response.status_code != 200:
        response.raise_for_status()
        raise RuntimeError(f"Request to {url} returned status code {response.status_code}")
    file_size = int(response.headers.get('Content-Length', 0))

    path = pathlib.Path(filename).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    desc = "(Unknown total file size)" if file_size == 0 else ""
    response.raw.read = functools.partial(response.raw.read, decode_content=True)
    try:
        with tqdm.wrapattr(response.raw, "read", total=file_size, desc=desc) as r_raw:
            with path.open("wb") as f:
                shutil.copyfileobj(r_raw, f)
    except Exception:
        path.unlink()
    return path


def download_package(package_name):
    print(f"Downloading package: {package_name}")
    app_id = get_appid(package_name)
    download_links = get_download_links(app_id)
    for i, download_link in enumerate(download_links):
        source = download_link[(download_link.rfind("/")+1):]
        destination = package_name + f".{i+1}.apk"
        if ("/apk/" in download_link):
            print(f"Downloading [{source}] -> [{destination}]")
            download_file(download_link, destination)
        else:
            print(f"Skipping non-apk [{source}]")
    print("Done!")


def search():
    query = input("Query> ")
    search_url = BASE_URL + "applicationData/apps"
    page_number = 0
    while True:
        response = requests.get(search_url, headers=MIMIC_HEADERS, params={
            "pageNumber": page_number,
            "pageSize": "5",
            "query": query,
            "buyeruid": "null",
        })
        apps = response.json()["body"]["content"]
        print(f"Page {page_number+1}")
        for i, app in enumerate(apps):
            print(f"[{(i+1)}]\u2501\u2533\u2501[{app['appName']}]")
            print("    \u2523\u2501 Package: " + app["packageName"])
            print("    \u2523\u2501 Company: " + app["companyName"])
            print("    \u2523\u2501 Version: " + str(app["versionCode"]))
            print("    \u2517\u2501 Description: " + app["shortDescription"])
        try:
            selection = int(input(f"[1-{len(apps)}]> ")) - 1
            download_package(apps[selection]["packageName"])
            return
        except KeyboardInterrupt:
            return
        except Exception:
            page_number += 1


def main():
    parser = argparse.ArgumentParser("rustoredl", description="Downloads an Android application by given package name from RuStore")
    subparsers = parser.add_subparsers(dest="sub")
    search_parser = subparsers.add_parser("search", help="Search packages on RuStore by name")
    download_parser = subparsers.add_parser("download", help="Download apk by package name immediately")
    download_parser.add_argument("-p", "--package_name", help="Package name to download.", required=True, type=str)

    parsed_args = parser.parse_args()

    if parsed_args.sub is None:
        parser.print_help()
        return

    if parsed_args.sub == "search":
        search()
    if parsed_args.sub == "download":
        download_package(parsed_args.package_name)


if __name__ == "__main__":
    main()

#!/usr/bin/python3

import requests
import argparse
import functools
import pathlib
import shutil
import sys
import os
from tqdm.auto import tqdm

from util import *

BASE_URL = "https://backapi.rustore.ru/"

MIMIC_HEADERS = {
    "Deviceid": get_random_device_id(),
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
    debug_print(response.json())
    return response.json()["body"]["appId"]


def get_download_links(app_id):
    download_url = BASE_URL + "applicationData/v2/download-link"
    json_data = {
        "appId": app_id,
        "firstInstall": False,
        "withoutSplits": False
    }
    response = requests.post(download_url, headers=MIMIC_HEADERS, json=json_data)
    debug_print(response.json())
    urls = response.json()["body"]["downloadUrls"]
    return [url["url"] for url in urls]


def download_file(url, filename):
    response = requests.get(url, stream=True, allow_redirects=True)
    if response.status_code != 200:
        response.raise_for_status()
        raise RuntimeError(f"Request to {url} returned status code {response.status_code}")
    file_size = int(response.headers.get('Content-Length', 0))

    path = pathlib.Path(filename).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        desc = "(Unknown total file size)" if file_size == 0 else ""
        response.raw.read = functools.partial(response.raw.read, decode_content=True)
        with tqdm.wrapattr(response.raw, "read", total=file_size, desc=desc) as r_raw:
            with path.open("wb") as destination:
                shutil.copyfileobj(r_raw, destination)
    except:
        print("Download interrupted.")
        path.unlink()
        sys.exit()


def print_links(package_name):
    try:
        app_id = get_appid(package_name)
    except:
        print(f"Package [{package_name}] could not be found")
        sys.exit(-1)
    print(f"Getting links for [{package_name}]...")
    download_links = get_download_links(app_id)
    for i, download_link in enumerate(download_links):
        print(f"[{i}] {download_link}")


def download_package(package_name):
    try:
        app_id = get_appid(package_name)
    except:
        print(f"Package [{package_name}] could not be found")
        sys.exit(-1)
    print(f"Downloading package [{package_name}]...")
    download_links = get_download_links(app_id)
    for i, download_link in enumerate(download_links):
        source = download_link[(download_link.rfind("/")+1):]
        destination = os.path.basename(package_name + f".{i+1}.apk")
        if ("/apk/" in download_link):
            print(f"Downloading [{source}] -> [{destination}]")
            download_file(download_link, destination)
        else:
            print(f"Skipping non-apk [{source}]")
    print("Done!")


def search_apps(query, page_number):
    search_url = BASE_URL + "applicationData/apps"
    response = requests.get(search_url, headers=MIMIC_HEADERS, params={
        "pageNumber": page_number,
        "pageSize": "5",
        "query": query,
        "buyeruid": "null",
    })
    debug_print(response.json())
    apps = response.json()["body"]["content"]
    return apps


def search():
    try:
        query = input("Query> ")
    except:
        sys.exit(-1)
    page_number = 0
    while True:
        apps = search_apps(query, page_number)
        print(f"Page [{page_number+1}]")
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
        except (SystemExit, KeyboardInterrupt):
            sys.exit()
        except:
            page_number += 1


def main():
    parser = argparse.ArgumentParser("rustoredl", description="Downloads an Android application by given package name from RuStore")
    parser.add_argument("-l", "--link-only", help="Get direct download link, skip downloading", action='store_true')
    subparsers = parser.add_subparsers(dest="sub")
    search_parser = subparsers.add_parser(OperationMode.SEARCH.value, help="Search packages on RuStore by application name")
    download_parser = subparsers.add_parser(OperationMode.DOWNLOAD.value, help="Download apk by package name immediately")
    download_parser.add_argument("-p", "--package_name", help="Package name to download.", required=True, type=str)

    parsed_args = parser.parse_args()
    
    if parsed_args.sub == OperationMode.SEARCH.value:
        return search()
    
    if parsed_args.sub == OperationMode.DOWNLOAD.value:
        if (parsed_args.link_only):
            return print_links(parsed_args.package_name)
        else:
            return download_package(parsed_args.package_name)
    
    parser.print_help()


if __name__ == "__main__":
    main()

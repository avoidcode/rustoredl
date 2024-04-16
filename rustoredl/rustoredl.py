#!/usr/bin/python3

import os
import shutil
import pathlib
import requests
import argparse
import functools
from colorama import Fore, Style
from tqdm.auto import tqdm
from datetime import datetime

from .util import *

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


def get_app_info(package_name):
    try:
        info_url = BASE_URL + "applicationData/overallInfo/" + package_name
        response = requests.get(info_url, headers=MIMIC_HEADERS).json()
        debug_print(response)
        return response["body"]
    except:
        raise NoSuchPackageException(f"Package [{package_name}] could not be found")


def get_download_links(app_id):
    download_url = BASE_URL + "applicationData/v2/download-link"
    json_data = {
        "appId": app_id,
        "firstInstall": False,
        "withoutSplits": False
    }
    response = requests.post(download_url, headers=MIMIC_HEADERS, json=json_data).json()
    debug_print(response)
    urls = response["body"]["downloadUrls"]
    return [url["url"] for url in urls]


def download_file(url, filename):
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get('Content-Length', 0))

    path = pathlib.Path(filename).resolve()

    try:
        desc = "(Unknown total file size)" if file_size == 0 else ""
        response.raw.read = functools.partial(response.raw.read, decode_content=True)
        with tqdm.wrapattr(response.raw, "read", total=file_size, desc=desc) as r_raw:
            with path.open("wb") as destination:
                shutil.copyfileobj(r_raw, destination)
    except:
        path.unlink()
        raise DownloadInterruptException("Download interrupted.")


def print_links(package_name):
    app_info = get_app_info(package_name)
    print(f"Getting links for [{package_name}] version [{app_info['versionName']}]...")
    download_links = get_download_links(app_info["appId"])
    for i, download_link in enumerate(download_links):
        print(f"[{i}] {download_link}")


def download_package(package_name):
    app_info = get_app_info(package_name)
    print(f"Downloading package [{package_name}] version [{app_info['versionName']}]...")
    download_links = get_download_links(app_info["appId"])
    
    if len(download_links) > 1:
        print("Seems like application is a split bundle. Downloading all files...")

    for i, download_link in enumerate(download_links):
        source_name = download_link[(download_link.rfind("/") + 1):]
        destination = os.path.basename(package_name + f".{i+1}" + pathlib.Path(source_name).suffix)
        if ("/apk/" in download_link):
            print(f"Downloading [{download_link}] -> [{destination}]")
            download_file(download_link, destination)
        else:
            print(f"Skipping non-apk [{download_link}]")
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


def search(link_only):
    query = input("Query> ")
    page_number = 0
    while True:
        apps = search_apps(query, page_number)
        print(Fore.LIGHTBLACK_EX + f"Page [{page_number+1}]" + Style.RESET_ALL)
        for i, app in enumerate(apps):
            print(f"[{(i+1)}]\u2501\u2533\u2501[{app['packageName']}] [{app['appName']}]")
            print("    \u2523\u2501 Description: " + app["shortDescription"])
            print("    \u2523\u2501 Company: " + app["companyName"])
            print("    \u2523\u2501 Version: " + str(app["versionCode"]))
            print("    \u2517\u2501 Updated: " + datetime.fromisoformat(app["updatedAt"]).strftime('%d.%m.%Y %H:%M'))
        try:
            selected_app = apps[int(input(f"[1-{len(apps)}]> ")) - 1]
            if link_only:
                return print_links(selected_app["packageName"])
            else:
                return download_package(selected_app["packageName"])
        except Exception as e:
            if type(e) in [KeyboardInterrupt, DownloadInterruptException]:
                raise
            page_number += 1


def main():
    parser = argparse.ArgumentParser(
        prog="rustoredl",
        description="Downloads an Android application by given package name from RuStore"
    )

    subparsers = parser.add_subparsers(dest="sub")

    search_parser = subparsers.add_parser(
        OperationMode.SEARCH.value,
        help="Search packages on RuStore by application name"
    )
    search_parser.add_argument(
        "-l", "--link-only",
        help="Get direct download link, skip downloading",
        action='store_true'
    )

    download_parser = subparsers.add_parser(
        OperationMode.DOWNLOAD.value,
        help="Download apk by package name immediately"
    )
    download_parser.add_argument(
        "-p", "--package-name",
        help="Package name to download.",
        required=True,
        type=str
    )

    get_link_parser = subparsers.add_parser(
        OperationMode.GETLINK.value,
        help="Get direct download link for apk by package name"
    )
    get_link_parser.add_argument(
        "-p", "--package-name",
        help="Package name to download.",
        required=True,
        type=str
    )

    parsed_args = parser.parse_args()

    try:
        if parsed_args.sub == OperationMode.SEARCH.value:
            return search(parsed_args.link_only)

        if parsed_args.sub == OperationMode.DOWNLOAD.value:
            return download_package(parsed_args.package_name)

        if (parsed_args.sub == OperationMode.GETLINK.value):
            return print_links(parsed_args.package_name)
    except (NoSuchPackageException, DownloadInterruptException) as e:
        print(e)
        return
    except KeyboardInterrupt:
        return

    parser.print_help()


if __name__ == "__main__":
    main()

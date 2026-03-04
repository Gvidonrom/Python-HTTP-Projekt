import sys
import argparse
from dataclasses import dataclass
from typing import Dict, Any

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


DEFAULT_URL = "https://example.com"
GET_URL = "https://httpbin.org/get"
POST_URL = "https://httpbin.org/post"


@dataclass
class HttpConfig:
    base_url: str = DEFAULT_URL
    get_url: str = GET_URL
    post_url: str = POST_URL


def create_webdriver() -> webdriver.Chrome:
    """Create a headless Chrome WebDriver."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    return driver


def scrape_tag(tag_name: str, config: HttpConfig) -> None:
    """
    Load a webpage and print the content of the first HTML tag found.

    Example:
        python script.py title
    """
    driver = create_webdriver()

    try:
        driver.get(config.base_url)

        elements = driver.find_elements(By.TAG_NAME, tag_name)

        if not elements:
            print(f"Tag <{tag_name}> not found on page {config.base_url}")
            return

        text = elements[0].text or elements[0].get_attribute("innerText") or ""
        print(text.strip())

    finally:
        driver.quit()


def perform_get(params: Dict[str, Any], config: HttpConfig) -> None:
    """
    Perform a GET request with parameters.
    """
    response = requests.get(config.get_url, params=params, timeout=10)

    print("=== GET URL ===")
    print(response.url)

    print("=== STATUS ===")
    print(response.status_code)

    print("=== RESPONSE JSON ===")

    try:
        print(response.json())
    except ValueError:
        print(response.text)


def perform_post(data: Dict[str, Any], config: HttpConfig) -> None:
    """
    Perform a POST request (form submission).
    """
    response = requests.post(config.post_url, data=data, timeout=10)

    print("=== POST URL ===")
    print(response.url)

    print("=== STATUS ===")
    print(response.status_code)

    print("=== RESPONSE JSON ===")

    try:
        print(response.json())
    except ValueError:
        print(response.text)


def list_cookies(config: HttpConfig) -> None:
    """
    Open the webpage with Selenium and print cookies.
    """
    driver = create_webdriver()

    try:
        driver.get(config.base_url)

        cookies = driver.get_cookies()

        if not cookies:
            print("No cookies found.")
            return

        print("=== COOKIES ===")

        for cookie in cookies:
            name = cookie.get("name", "")
            value = cookie.get("value", "")
            domain = cookie.get("domain", "")
            path = cookie.get("path", "")

            print(f"{name} = {value}; domain={domain}; path={path}")

    finally:
        driver.quit()


def show_status(config: HttpConfig) -> None:
    """
    Show HTTP status code of the webpage.
    """
    response = requests.get(config.base_url, timeout=10)

    print("=== STATUS ===")
    print(response.status_code)


def parse_key_value_list(pairs: list[str]) -> Dict[str, str]:
    """
    Convert list of 'key=value' strings to dictionary.
    """
    result: Dict[str, str] = {}

    for item in pairs:
        if "=" not in item:
            continue

        key, value = item.split("=", 1)
        result[key] = value

    return result


def build_arg_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Python HTTP Project\n\n"
            "Examples:\n"
            "  python script.py title\n"
            "  python script.py get foo=1 bar=2\n"
            "  python script.py post username=alice password=secret\n"
            "  python script.py list-cookies\n"
            "  python script.py status\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "command",
        help="HTML tag name or command: get, post, list-cookies, status",
    )

    parser.add_argument(
        "params",
        nargs="*",
        help="key=value parameters for GET/POST",
    )

    return parser


def main(argv: list[str] | None = None) -> None:
    """Program entry point."""

    if argv is None:
        argv = sys.argv[1:]

    parser = build_arg_parser()

    # если аргументов нет — показать help
    if not argv:
        parser.print_help()
        return

    args = parser.parse_args(argv)

    config = HttpConfig()

    command = args.command.lower()
    params_dict = parse_key_value_list(args.params)

    if command == "get":
        perform_get(params_dict, config)

    elif command == "post":
        perform_post(params_dict, config)

    elif command == "list-cookies":
        list_cookies(config)

    elif command == "status":
        show_status(config)

    else:
        # treat command as HTML tag name
        scrape_tag(args.command, config)


if __name__ == "__main__":
    main()
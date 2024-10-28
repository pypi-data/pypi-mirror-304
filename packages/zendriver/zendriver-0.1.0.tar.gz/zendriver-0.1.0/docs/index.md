# Zendriver

Zendriver is a blazing fast, async-first, undetectable webscraping/web automation framework implemented using the Chrome Devtools Protocol. Visit websites, scrape content, and run JavaScript using a real browser (no Selenium/Webdriver) all with just a few lines of Python.

This package is a fork of the excellent [`ultrafunkamsterdam/nodriver`](https://github.com/ultrafunkamsterdam/nodriver/), created in order to compile a variety of unmerged bugfixes and increase overall community engagement with the project.

## Features

- **Undetectable** - Zendriver uses the Chrome Devtools Protocol instead of Selenium/WebDriver, making it (almost) impossible to detect
- **Blazing fast** - Chrome Devtools Protocol is _fast_, much faster than previous Selenium/WebDriver solutions. CDP combined with an async Python API makes Zendriver highly performant.
- **Feature complete and easy to use** - Packed with allowing you to get up and running in just a few lines of code.
- **Automatic cookie and profile management** - By default, uses fresh profile on each run, cleaning up on exit. Or, save and load cookies to a file to avoid repeating tedious login steps.
- **Smart element lookup** - Find elements selector or text, including iframe content. This could also be used as wait condition for a element to appear, since it will retry for the duration of `timeout` until found. Single element lookup by text using `tab.find()` accepts a `best_match flag`, which will not naively return the first match, but will match candidates by closest matching text length.
- **Easy debugging** - Descriptive `repr` for elements, which represents the element as HTML makes debugging much easier.

## Installation

To install, simply use `pip` (or your favorite package manager):

```sh
pip install zendriver
# or uv add zendriver, poetry add zendriver, etc.
```

## Usage

Example for visiting [https://www.browserscan.net/bot-detection](https://www.browserscan.net/bot-detection) and saving a screenshot of the results:

```python
import asyncio

import zendriver as zd


async def main():
    browser = await zd.start()
    page = await browser.get("https://www.browserscan.net/bot-detection")
    await page.save_screenshot("browserscan.png")
    await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
```

See [Quickstart](./quickstart.md) for more examples.

## Who is this for?

This project is intended for individuals looking for a way to automate common tasks in their daily lives. In modern times, many websites implement stringent anti-bot measures which are in clear violation of the founding principles of the open web. These measures make it all-but impossible for regular people to programmatically interact with their favorite websites, while doing nothing against the hostile scrapers of for-profit technology companies like Amazon or OpenAI which are developed by teams of experienced engineers.

Zendriver (like [`nodriver`](https://github.com/ultrafunkamsterdam/nodriver/) and [`undetected-chromedriver`](https://github.com/ultrafunkamsterdam/undetected-chromedriver) before it) is an attempt to re-democratize the web, giving normal people access to the same data and tools as these large technology companies. If you ever wanted to set up a notification bot for Facebook Marketplace or archive the content of your favorite blogger before it their website inevitably goes offline, this project is for you.

On the other hand, if you are interested in DDoSing someone, automatically creating thousands of fake social media accounts, or leaving fake reviews on e-commerce sites, **you are not welcome here**. Please think carefully about whether the website you are scraping has good reason for the anti-bot measures they have implemented and do not use this tool for anything illegal or otherwise malicious.

## Rationale for the fork

Zendriver remains committed to `nodriver`'s goals of staying undetected for all modern anti-bot solutions and also keeps with the batteries-included approach of its predecessor. Unfortunately, contributions to the original [`nodriver` repo](https://github.com/ultrafunkamsterdam/nodriver/) are heavily restricted, making it difficult to submit issues or pull requests. At the time of writing, there are several pull requests open to fix critical bugs which have beeen left unaddressed for many months.

Zendriver aims to change this by:

1. Including open pull requests in the original `nodriver` repo as part of the initial release
2. Modernizing the development process to include static analysis tools such as [`ruff`](https://docs.astral.sh/ruff/) and [`mypy`](https://mypy-lang.org/), reducing the number of easy-to-catch bugs which make it through in the future
3. Opening up the issue tracker and pull requests for community contributions, allowing the project to continue to grow along with its community.

With these changes in place, we hope to further development of state-of-the-art open-source web automation tools even further, helping to once again make the web truly open for all.

import csv
import time
import argparse
from typing import Dict

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as Soup

from setupDriver import setupDriver


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", type=str, default="https://www.facebook.com")
    return parser.parse_args()


def crawlData(args, driver) -> Dict:
    driver.get(args.page)
    time.sleep(5)

    for _ in range(50):
        try:
            seeMoreButton = driver.find_element(By.XPATH, "//div[@role='button' and text()='顯示更多']")
            seeMoreButton.click()
            time.sleep(1)
        except NoSuchElementException:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
        
    results = []
    soup = Soup(driver.page_source, "lxml")

    articles = soup.findAll('div', {'role': 'article'})
    for article in articles:
        if article == None:
            continue

        result = []
        # Find contents
        contents = article.findAll('div', {'dir': 'auto'})
        if contents == None or len(contents) == 0:
            continue
        mainPost = contents[0].text
        mainPostWithDelimiter = ""
        for i in range(1, len(contents)):
            if contents[i].text in mainPost:
                mainPostWithDelimiter += contents[i].text
                mainPostWithDelimiter += "，"
        mainPostWithDelimiter = mainPostWithDelimiter[:-1]
        if mainPostWithDelimiter == "":
            continue
        result.append(mainPostWithDelimiter)
        
        # Find likes
        likes = article.find('span', {'role': 'toolbar'})
        if likes == None:
            continue
        likes = likes.findAll('div', {'role': 'button'})
        if likes == None:
            continue
        likeToNum = {}
        for like in likes:
            try:
                label = like['aria-label']
                if '：' in label:
                    label = label[:-1]
                    likeToNum[label[:label.find('：')]] = int(label[label.find('：') + 1:])
            except KeyError:
                pass
        result.append(likeToNum)
        results.append(result)
    return results


def saveToFile(textToLikes):
    with open("../data.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(['text', 'likes'])
        for textToLike in textToLikes:
            writer.writerow(textToLike)


if __name__ == "__main__":
    args = parseArgs()
    driver = setupDriver()
    data = crawlData(args, driver)
    saveToFile(data)
    driver.quit()
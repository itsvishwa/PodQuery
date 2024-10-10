import requests
from bs4 import BeautifulSoup
import json

# scrap transcript data from URLs
def scrape_data(transcript_list, title_list, youtube_url_list):
    print("Scraping transcript data...")
    data = []
    # data = [{url: ..., title: ..., chapters: [{title: ..., statements: [{speaker: ..., timestamp: ..., text: ...}]}]}]

    for i, url in enumerate(transcript_list):
        data.append({
            "url": youtube_url_list[i],
            "title": title_list[i],
            "chapters": []
        })
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        segment = soup.find('div', class_='ts-segment')
        all_contents = segment.find_parent("div")


        current_speaker = ""

        for content in all_contents:
            if content.name is None:
                continue
            elif content.name == "h2":
                data[-1]["chapters"].append({"title": content.get_text(strip=True), "statements": ""})
            elif content.get("class") and content.get("class") == ["ts-segment"]:
                timestamp = content.find("span", class_="ts-timestamp").get_text(strip=True).strip("()")

                speaker = content.find("span", class_="ts-name").get_text(strip=True)
                current_speaker = speaker if speaker != "" else current_speaker

                text = content.find("span", class_="ts-text").get_text(strip=True)
                text = text.translate(str.maketrans({
                    "\u2019": "'",
                    "\u2026": "...",
                    '"': "'"
                }))
              
                temp = f"[{timestamp}][{current_speaker}][{text}]."
                data[-1]["chapters"][-1]["statements"] += temp
            else:
                continue
    print("Transcript data scraped.")
    return data


# initialize json file with data
def init_json_file(data, file_path):
    # data = [{url: ..., title: ..., chapters: [{title: ..., statements: [{speaker: ..., timestamp: ..., text: ...}]}]}]
    print("Initializing json file...")
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("Json file initialized.")

def main():
    transcript_list = [
        "https://lexfridman.com/ben-shapiro-destiny-debate-transcript/",
        "https://lexfridman.com/elon-musk-4-transcript/#chapter1_war_and_human_nature",
        "https://lexfridman.com/sam-altman-2-transcript/",
        "https://lexfridman.com/yann-lecun-3-transcript"
    ]
    title_list = [
        "Ben Shapiro vs Destiny Debate: Politics, Jan 6, Israel, Ukraine & Wokeism | Lex Fridman Podcast #410",
        "Elon Musk: War, AI, Aliens, Politics, Physics, Video Games, and Humanity | Lex Fridman Podcast #400",
        "Sam Altman: OpenAI, GPT-5, Sora, Board Saga, Elon Musk, Ilya, Power & AGI | Lex Fridman Podcast #419",
        "Yann Lecun: Meta AI, Open Source, Limits of LLMs, AGI & the Future of AI | Lex Fridman Podcast #416"
    ]
    youtube_url_list = [
        "https://www.youtube.com/watch?v=tYrdMjVXyNg",
        "https://www.youtube.com/watch?v=JN3KPFbWCy8",
        "https://www.youtube.com/watch?v=jvqFAi7vkBc",
        "https://www.youtube.com/watch?v=5t1vTLU7s40"
    ]

    data = scrape_data(transcript_list, title_list, youtube_url_list)
    init_json_file(data, "data/data.json")


if __name__ == "__main__":
    main()



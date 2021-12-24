import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Pokemon:
    def __init__(self, name):
        self.name = name
        self.url = "https://pokemondb.net/pokedex/" + self.name
        page = requests.get(self.url)
        page = page.text
        self.soup = BeautifulSoup(page, "html.parser")

    def getBio(self):
        bio_table = self.soup.find("div", class_="grid-col span-md-6 span-lg-4")

        bio_name = []
        for tr in bio_table.find_all("tr"):
            name = tr.find("th")
            bio_name.append(name)
            for td in tr.findAll("td"):
                print(td.text)
            print(name)

    # Returns DataFrame of Pokemon Stats
    def getStats(self):
        stats_table = self.soup.find("div", class_="grid-col span-md-12 span-lg-8")

        # Contains all the stat names
        stat_names = []
        base_stats = []
        min = []
        max = []

        # Sum of Base Stat Total
        total = 0

        for t in stats_table.find_all("tr"):
            stat = t.find("th").text
            if stat == "Total":
                break
            else:
                stat_names.append(stat)
            index = 0
            for n in t.findAll(class_="cell-num"):
                value = int(n.text)
                if index == 0:
                    base_stats.append(value)
                elif index == 1:
                    min.append(value)
                else:
                    max.append(value)
                index += 1

        # Create Data Frame
        column = ["Stat_Name", "Base_Stat", "Min", "Max"]
        df = pd.DataFrame(columns=column)
        df["Stat_Name"] = stat_names
        df["Base_Stat"] = base_stats
        df["Min"] = min
        df["Max"] = max
        return df

    def getBio(self):
        bio_table = self.soup.find_all("div", class_="grid-col span-md-6 span-lg-4")
        bio_name = []
        bio_data = []
        abilities = []
        for tr in bio_table[1].findAll("tr"):
            name = tr.find("th").text
            bio_name.append(name)
            for td in tr.findAll("td"):
                if name == "Abilities":
                    for t in td.findAll(class_="text-muted"):
                        abilities.append(t.text)
                    bio_data.append(abilities)
                    break
                bio_data.append(td.text)

        # Create DataFrame
        df = pd.DataFrame([bio_data], columns=bio_name)
        df["Type"] = df["Type"][0].strip("\n").rstrip(" ").replace(" ", "/")

        # Delete Location Column
        del df["Local №"]

        # Clean Abilities Column
        for n in range(len(abilities)):
            is_number = abilities[n][0]
            if is_number.isdigit():
                abilities[n] = abilities[n][3:]
        return df

    # Get total bst
    def getTotal(self):
        total = 0
        for b_stat in self.getStats()["Base_Stat"]:
            total += b_stat
        return total

    # Displays Bar Graph of Pokemon Stats
    def stat_vis(self):
        fig, ax = plt.subplots()
        sns.barplot(x="Base_Stat", y="Stat_Name", data=self.getStats())
        plt.show()
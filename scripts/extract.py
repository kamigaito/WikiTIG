import bs4
import json
import os

with open("./extracted/enwiki2008.jsonl", mode="w", encoding="utf-8") as f_out:
    dir_path = "./data/enwiki2008/"
    with open("./extracted/pages.lst") as f_in:
        for line in f_in:
            file_path = dir_path + line.strip()
            print(file_path)
            try:
                f = open(file_path, mode="r", encoding="utf-8")
                text = f.read()
                f.close()
            except:
                continue
            if "infobox" not in text:
                continue
            soup = bs4.BeautifulSoup(text, "html.parser")
            page_title = soup.select("title")
            if len(page_title) == 0:
                continue
            page_title = page_title[0].get_text().replace(" - Wikipedia, the free encyclopedia", "").strip()
            infoboxes = soup.select(".infobox")
            if len(infoboxes) > 0:
                for infobox in infoboxes:
                    rows = []
                    has_image = False
                    for row in infobox.find_all('tr'):
                        cells = []
                        for cell in row.children:
                            if cell.name in ('td', 'th'):
                                text = cell.get_text().strip()
                                images = []
                                for img in cell.find_all('img'):
                                    has_image = True
                                    img_name = (img['src'].split("/"))[-1]
                                    if "px-" in img_name:
                                        img_name = "-".join((img_name.split("-"))[1:])
                                    img_name = img_name.replace(".svg.png", ".svg")
                                    if 'alt' in img:
                                        images.append({"alt" : img['alt'], "src" : img_name})
                                    else:
                                        images.append({"alt" : "", "src" : img_name})
                                if len(images) == 0:
                                    cells.append({"text" : text})
                                else:
                                    cells.append({"text" : text, "images" : images})
                        rows.append(cells)
                    if has_image:
                        line = {"title" : page_title, "infobox": rows}
                        print(line)
                        json.dump(line, f_out, ensure_ascii=False)
                        f_out.write("\n")

import requests
from bs4 import BeautifulSoup

URL = "https://plants.ces.ncsu.edu/plants/quercus-chrysolepis/" # main source of info
URL2 = "https://edis.ifas.ufl.edu/publication/ST541" # edis
URL3 = "https://www.wildflower.org/plants/result.php?id_plant=QUCH2" # Habitat stuff
page = requests.get(URL)
page2 = requests.get(URL2)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="plant_detail")

soup2 = BeautifulSoup(page2.content, "html.parser")
trees = soup2.find(id="edis-content")

# user agent is needed because regular GET requests don't work on URL3
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": USER_AGENT} # adding the user agent
resp = requests.get(URL3, headers=headers)
soup3 = BeautifulSoup(resp.content, "html.parser") # use this if you want to scrape the site
habitat = soup3.find(id="fullpage_content")

# URL(1) structure: <dl><dt>Attribute</dt> <dd>Value</dd> <dd>Value 2</dd></dl>
def get_dl(soup):
    keys, values = [], []
    for dl in soup.findAll("li", {"class": "list-group-item"}):
        for dt in dl.findAll("dt"):
            keys.append(dt.text.strip())
            arr = []
            dd = dt.findNext("dd")
            #dd_next = dd.find_next_sibling("dd")
            dt_next = dt.find_next_sibling("dt")
            if (dt_next): 
                dd_last = dt_next.find_next("dd")
            
            while (True):
                if (dd):
                    arr.append(dd.text.strip())
                try:
                    dd = dd.find_next_sibling("dd")
                except: 
                    dd = dd_last

                if (dd != dd_last): continue
                else: break
            values.append(arr)               

    return dict(zip(keys, values))

# URL2 structure: <p> <b>Attribute:</b> Value </p>
def get_p(soup):
    keys, values = [], []
    for p in soup.findAll("p"):
        stuff = p.text.strip()
        broke = stuff.partition(":")
        if (len(stuff) > 0): 
            keys.append(broke[0] + broke[1]) # substring before ":" including ":"
            values.append(broke[2]) # substring after ":"
    for p in soup.findAll("blockquote"):
        stuff = p.text.strip()
        broke = stuff.partition(":")
        if (len(stuff) > 0): 
            keys.append(broke[0] + broke[1]) # substring before ":" including ":"
            values.append(broke[2]) # substring after ":"
    return dict(zip(keys, values))

# URL3 structure: <div> <strong>Attribute:</strong> " Value " <br> </div>
def get_text(soup):
    keys, values = [], []
    for st in soup.findAll("strong"):
        keys.append(st.text.strip())
        values.append(st.find_next_sibling(string=True))
    return dict(zip(keys, values))

# Building dictionaries
dl_dict = get_dl(results)
p_dict = get_p(trees)
text_dict = get_text(habitat)

# Keys needed from URL and URL2
wanted = ["Family:", "Woody Plant Leaf Characteristics:", "Leaf Color:", "Deciduous Leaf Fall Color:", "Leaf Type:",
           "Leaf Arrangement:", "Leaf Shape:", "Leaf venation:", "Leaf Margin:", "Hairs Present:", "Leaf Length:",
            "Leaf blade length:", "Fall color:", "Fall characteristic:", "Leaf Description:",
             "USDA Plant Hardiness Zone:", "USDA hardiness zones:", "Country Or Region Of Origin:", "Origin:", "UF/IFAS Invasive Assessment Status:", "Invasive potential:", "Uses (Ethnobotany):",
               "Wildlife Value:", "Play Value:", "Edibility:", "Use Ornamental:", "Use Wildlife:", "Use Food:", "Height:", "Spread:", "Dimensions:",
                 "Flower Color:", "Flower Inflorescence:", "Flower Bloom Time:", "Flower Size:",
               "Flower Description:", "Fruit Color:", "Display/Harvest Time:", "Fruit Type:", "Fruit Length:", "Fruit Description:",
               "Bark Color:", "Surface/Attachment:", "Bark Plate Shape:", "Bark Description:", "Stem Color:", "Stem Is Aromatic:",
                 "Stem Buds:", "Stem Bud Terminal:", "Stem Cross Section:", "Stem Form:", "Stem Leaf Scar Shape:", "Stem Description:",
                 "USA:", "Canada:", "Native Distribution:", "Native Habitat:", "Water Use:", "Light Requirement:", "Soil Moisture:",
                 "Soil pH:", "Cold Tolerant:", "Heat Tolerant: ",
          "CaCO3 Tolerance:", "Drought Tolerance:", "Soil Description:", "Conditions Comments:", "Resistance To Challenges:",
            "Attracts:", "Problems:"]

placeholder = ["", "", "", "", "", "", "", "", "", "", ""]

final = ""
for elem in wanted:

    # Convert to str type in order to concatenate
    main = str(dl_dict.get(elem))
    alt = str(p_dict.get(elem))
    alt2 = str(text_dict.get(elem))

    # If main or alt doesn't exist, its value becomes "None" instead of None because of str()

    final += elem
    if (main != "None"):       
        final += " " + main
    elif (alt != "None"):
        final += alt
    else:  
        final += alt2
    final += "\n"

remove = ["[", "]", "'"]
for i in remove:
        final = final.replace(i, "")
print(final)

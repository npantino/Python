from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup


URL = "https://plants.ces.ncsu.edu/plants/quercus-imbricaria/common-name/shingle-oak/" # main source of info
URL2 = "https://edis.ifas.ufl.edu/publication/ST548" # edis
URL3 = "https://www.wildflower.org/plants/result.php?id_plant=QUIM" # Habitat stuff

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
            "Leaf blade length:", "Fall characteristic:", "Leaf Description:", "USDA hardiness zones:", 
            "Origin:", "UF/IFAS Invasive Assessment Status:", "Uses (Ethnobotany):",
               "Wildlife Value:", "Play Value:", "Edibility:", "Use Ornamental:", "Use Wildlife:", "Use Food:",
                 "Height:", "Spread:",
                 "Flower Color:", "Flower Inflorescence:", "Flower Bloom Time:", "Flower Size:",
               "Flower Description:", "Fruit Color:", "Display/Harvest Time:", "Fruit Type:", "Fruit Length:", "Fruit Description:",
               "Trunk/branches:", "Bark:", "Current year twig color:",
                 "Current year twig thickness:", "Stem Description:",
                 "USA:", "Canada:", "Native Distribution:", "Native Habitat:", "Water Use:", "Light Requirement:", "Soil Moisture:",
                 "Soil pH:", "Cold Tolerant:", "Heat Tolerant: ",
          "CaCO3 Tolerance:", "Drought Tolerance:", "Soil Description:", "Conditions Comments:", "Resistance To Challenges:",
            "Attracts:", "Problems:"]

placeholder = ["", "", "", "", "", "", "", "", "", "", ""]


final_arr = []
for elem in wanted:
    # Convert to str type in order to concatenate
    main = str(dl_dict.get(elem))
    alt = str(p_dict.get(elem))
    alt2 = str(text_dict.get(elem))

    # If main or alt doesn't exist, its value becomes "None" instead of None because of str()
    final = ""
    final += elem
    if (main != "None"):       
        final += " " + main
    elif (alt != "None"):
        final += alt
    else:  
        final += alt2
    remove = ["[", "]", "'"]
    for i in remove:
        final = final.replace(i, "")
    final_arr.append(final)

app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])


   

def get_beer():
    info = {
        0: final_arr[0],
        1: final_arr[1],
        2: final_arr[2],
        3: final_arr[3],
        4: final_arr[4],
        5: final_arr[5],
        6: final_arr[6],
        7: final_arr[7],
        8: final_arr[8],
        9: final_arr[9],
        10: final_arr[10],
        11: final_arr[11],
        12: final_arr[12],
        13: final_arr[13],
        14: final_arr[14],
        15: final_arr[15],
        16: final_arr[16],
        17: final_arr[17],
        18: final_arr[18],
        19: final_arr[19],
        20: final_arr[20],
        21: final_arr[21],
        22: final_arr[22],
        23: final_arr[23],
        24: final_arr[24],
        25: final_arr[25],
        26: final_arr[26],
        27: final_arr[27],
        28: final_arr[28],
        29: final_arr[29],
        30: final_arr[30],
        31: final_arr[31],
        32: final_arr[32],
        33: final_arr[33],
        34: final_arr[34],
        35: final_arr[35],
        36: final_arr[36],
        37: final_arr[37],
        38: final_arr[38],
        39: final_arr[39],
        40: final_arr[40],
        41: final_arr[41],
        42: final_arr[42],
        43: final_arr[43],
        44: final_arr[44],
        45: final_arr[45],
        46: final_arr[46],
        47: final_arr[47],
        48: final_arr[48],
        49: final_arr[49],
        50: final_arr[50],
        51: final_arr[51],
        52: final_arr[52],
        53: final_arr[53],
        54: final_arr[54],
        55: final_arr[55],
        56: final_arr[56],
        57: final_arr[57],
    }
    print(info)
    return render_template('home.html', info=info)

if __name__ == '__main__':
    app.run(debug=True)
#print(final)

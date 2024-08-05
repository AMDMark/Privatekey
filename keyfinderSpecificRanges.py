import requests
from bs4 import BeautifulSoup
import random
import time
import sys

# Define the list of ranges
ranges = [
    (614966547447110042, 634102135138549692),
    (634111519928981982, 653317493548663808),
    (653397264267338275, 672462466030535748),
    (672612622677452391, 691677824440649864),
    (691827981087566507, 710893182850763981),
    (711043339497680624, 730108541260878097),
    (730258697907794740, 749323899670992214),
    (749474056317908856, 768539258081106330),
    (768689414728022973, 787754616491220446),
    (787904773138137089, 806969974901334562),
    (807120131548251205, 826185333311448679),
    (826335489958365321, 845400691721562795),
    (845550848368479438, 864616050131676911),
    (864766206778593554, 883831408541791027),
    (883981565188707670, 903046766951905144),
    (903196923598821786, 922262125362019260),
    (922412282008935903, 941477483772133376),
    (941627640419050019, 960692842182247492),
    (960842998829164135, 979908200592361609),
    (980058357239278251, 999123559002475725),
    (999273715649392368, 1018338917412589841),
    (1018489074059506484, 1037554275822703958),
    (1037704432469620600, 1056769634232818074),
    (1056919790879734717, 1075984992642932190),
    (1076135149289848833, 1095200351053046306),
    (1095350507699962949, 1114415709463160423),
    (1114565866110077065, 1133631067873274539),
    (1133781224520191182, 1152846426283388655),
    (1152996582930305298, 1172061784693502771),
    (1172211941340419414, 1191277143103616888),
    (1191427299750533530, 1210492501513731004),
    (1210642658160647647, 4899841316255641327)
]

# Target address to check for a match
target_address = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"

# Initialize the counter
keys_generated_counter = 0

def fetch_data():
    global keys_generated_counter

    # Select a random range
    selected_range = random.choice(ranges)
    min_value, max_value = selected_range

    # Generate a random number within the selected range
    random_number = random.randint(min_value, max_value)

    # Increment the counter
    keys_generated_counter += 1

    # Print the counter and last number generated (overwrite the same line)
    sys.stdout.write(f"\rKeys Generated: {keys_generated_counter}, Last Number Generated: {random_number}")
    sys.stdout.flush()

    # Construct the URL
    url = f"https://privatekeyfinder.io/private-keys/bitcoin/{random_number}"

    # Fetch the webpage
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return False

    # Parse the webpage content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract private keys and Bitcoin addresses
    private_keys = []
    bitcoin_addresses = []

    # Assuming the private keys and addresses are in table rows
    rows = soup.find_all('tr')

    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            private_key_label = cells[0].text.strip()
            bitcoin_address_label = cells[1].text.strip()

            if private_key_label.startswith('HEX'):
                private_key = private_key_label.split()[1]
                bitcoin_address = bitcoin_address_label.split()[1]

                private_keys.append(private_key)
                bitcoin_addresses.append(bitcoin_address)

                #print(f"Private Key: {private_key}")
                #print(f"Bitcoin Address: {bitcoin_address}")

                # Check for a match with the specified address
                if bitcoin_address == target_address:
                    print(f"\nMatch found: {target_address}")
                    with open("match_found.txt", "w") as file:
                        file.write(f"Private Key: {private_key}\n")
                        file.write(f"Bitcoin Address: {bitcoin_address}\n")
                    return True

    #print("No match found.")
    return False

while True:
    try:
        if fetch_data():
            break
    except Exception as e:
        print(e)
        print("Retrying...")
        time.sleep(1)

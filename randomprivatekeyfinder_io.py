import requests
from bs4 import BeautifulSoup
import random
import time

#The address 0x2fb1fce3b8dcfc000 with a 10% increase in range is 0x3476fc94182648800
#The address 0x3141a7ecbef754000 with a 7% increase in range is 0x34b454f5a35fae800

# Define the range for the random number
min_value = 1008129773390568400
max_value = 1041128767536780800  # Correcting the max range based on your initial input

# Target address to check for a match
target_address = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"

def fetch_data():
    # Generate a random number within the specified range
    random_number = random.randint(min_value, max_value)

    # Print the random number generated
    print(f"Random Number Generated: {random_number}")

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

                print(f"Private Key: {private_key}")
                print(f"Bitcoin Address: {bitcoin_address}")

                # Check for a match with the specified address
                if bitcoin_address == target_address:
                    print(f"Match found: {target_address}")
                    with open("match_found.txt", "w") as file:
                        file.write(f"Private Key: {private_key}\n")
                        file.write(f"Bitcoin Address: {bitcoin_address}\n")
                    return True

    print("No match found.")
    return False

while True:
    try:
        if fetch_data():
            break
    except Exception as e:
        print(e)
        print("Retrying...")
        time.sleep(1)

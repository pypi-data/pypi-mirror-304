from .data_loader import load_data, load_state_province_abbreviations
from .spell_checker import initialize_spell_checker, correct_spelling
from .fuzzy_match import fuzzy_city_lookup
from .model_invoke import initialize_model, invoke_model
from .geo_location import lookup_lat_long_canada, lookup_lat_long_us
from .utils import clean_address
from .scrape import get_lat_long

class AddressLookup:
    def __init__(self, canadian_postal_codes_path, us_zip_codes_path, llama_model, success_output="success.txt", failed_path='failed.txt', can_key='CITY', usa_key='City' debug=False, remote=False, remote_api_base=None, remote_api_key=None):
        # Load data
        self.canadian_postal_codes, self.us_zip_codes = load_data(canadian_postal_codes_path, us_zip_codes_path)
        self.failed_path = failed_path
        self.success_output = success_output

        # Ensure failed_path file exists or create it
        if not os.path.exists(self.failed_path):
            with open(self.failed_path, 'w') as f:
                pass  # Create an empty file

        # Ensure success_output file exists or create it
        if not os.path.exists(self.success_output):
            with open(self.success_output, 'w') as f:
                pass  # Create an empty file

        if self.canadian_postal_codes is None or self.us_zip_codes is None:
            raise FileNotFoundError("One or more postal code files could not be loaded.")
        
        self.debug = debug
        self.state_province_abbreviations = load_state_province_abbreviations()

        # Initialize spell checker
        canadian_cities = self.canadian_postal_codes['CITY'].dropna().unique().tolist()
        us_cities = self.us_zip_codes['City'].dropna().unique().tolist()
        self.spell_checker = initialize_spell_checker(canadian_cities, us_cities)

        # Initialize model
        self.llm = initialize_model(remote, llama_model, remote_api_base, remote_api_key)

    def lookup(self, address):
        # Clean the address
        address = clean_address(address)

        # Generate prompt for model
        prompt = (
            f"Extract the following information from the address: '{address}'. "
            "1. 'city' (ensure correct spelling), "
            "2. 'state_or_province' (full name), "
            "3. 'state_or_province_abbreviation', "
            "4. 'country' (either 'Canada' or 'America'. State the country in this exact format.). "
            "Ensure that none of the values are null or missing. "
            "If any information is uncertain, make the best guess based on the address provided. "
            "Return the result strictly in JSON format with these keys: "
            "'city', 'state_or_province', 'state_or_province_abbreviation', 'country'. "
            "Do not include any explanatory text."
            "Do not make extrapolations of where a city might be"
        )
        
        try:
            # Invoke model
            data = invoke_model(self.llm, prompt)
            if data:
                # Correct spelling
                city = correct_spelling(data['city'], self.spell_checker)
                
                state_abbr = data['state_or_province_abbreviation']
                country = data['country']

                # Perform geolocation lookup
                if country == 'Canada':
                    lat, long = lookup_lat_long_canada(self.canadian_postal_codes, city, state_abbr)
                elif country == 'America':
                    lat, long = lookup_lat_long_us(self.us_zip_codes, city, state_abbr)
                else:
                    return None

                # Check if lat/long is valid
                if lat is not None and long is not None:
                    with open(self.success_output, 'a') as f:
                        f.write(f"{city} / {data['state_or_province} / {latitude} / {longitude}\n")
                    return {
                        'city': city,
                        'state_full': data['state_or_province'],
                        'latitude': lat,
                        'longitude': long
                    }
                else:
                    google_query = f"{data['city']} {data['state_or_province']} latitude and longitude"
                    lat, long = get_lat_long(google_query)
                    return {
                        'city': city,
                        'state_full': data['state_or_province'],
                        'latitude': lat,
                        'longitude': long
                    }

            else:
                if debug == True:
                    print(f"{city} {data['state_or_province']} not found")
                with open(self.failed_path, 'a') as f:
                    f.write(f"{city} / {data['state_or_province']}\n")
                return None

        except Exception as e:
            return None


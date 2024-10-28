import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torchvision")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

from .data_loader import load_data, load_state_province_abbreviations
from .spell_checker import initialize_spell_checker, correct_spelling
from .fuzzy_match import fuzzy_city_lookup
from .model_invoke import initialize_model, invoke_model
from .geo_location import lookup_lat_long_canada, lookup_lat_long_us
from .utils import clean_address
from .scrape import get_lat_long
import os
import json
import torch
from transformers import BertTokenizer, AutoModel
import torch.nn as nn

class AddressTransformer(nn.Module):
    def __init__(self, num_cities, num_provinces):
        super(AddressTransformer, self).__init__()
        self.bert = AutoModel.from_pretrained('huawei-noah/TinyBERT_General_4L_312D')
        self.city_classifier = nn.Sequential(
            nn.Linear(self.bert.config.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, num_cities)
        )
        self.province_classifier = nn.Sequential(
            nn.Linear(self.bert.config.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, num_provinces)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_output = outputs.last_hidden_state[:, 0, :]
        city_logits = self.city_classifier(cls_output)
        province_logits = self.province_classifier(cls_output)
        return city_logits, province_logits


class AddressLookup:
    def __init__(self, canadian_postal_codes_path, us_zip_codes_path, llama_model, success_output="success.txt", failed_path='failed.txt', can_key='CITY', usa_key='City', debug=False, remote=False, remote_api_base=None, remote_api_key=None):
        # Locate the optional_files directory
        optional_files_dir = os.path.join(os.path.dirname(__file__), 'optional_files')
        mappings_path = os.path.join(optional_files_dir, 'mappings.json')
        model_path = os.path.join(optional_files_dir, 'clean_address_transformer_model.pth')
        tokenizer_path = os.path.join(optional_files_dir, 'tokenizer/')

        # Load data
        self.canadian_postal_codes, self.us_zip_codes = load_data(canadian_postal_codes_path, us_zip_codes_path)
        self.failed_path = failed_path
        self.success_output = success_output

        # Ensure files exist
        for path in [self.failed_path, self.success_output]:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    pass

        if self.canadian_postal_codes is None or self.us_zip_codes is None:
            raise FileNotFoundError("One or more postal code files could not be loaded.")
        
        self.debug = debug
        self.state_province_abbreviations, self.abbreviation_to_fullname = load_state_province_abbreviations()

        # Initialize spell checker
        canadian_cities = self.canadian_postal_codes[can_key].dropna().unique().tolist()
        us_cities = self.us_zip_codes[usa_key].dropna().unique().tolist()
        self.spell_checker = initialize_spell_checker(canadian_cities, us_cities)

        # Initialize model
        if llama_model == "ADG":
            # Load mappings
            with open(mappings_path, 'r') as f:
                mappings = json.load(f)
            self.city_to_idx = mappings['city_to_idx']
            self.province_to_idx = mappings['province_to_idx']
            self.idx_to_city = {v: k for k, v in self.city_to_idx.items()}
            self.idx_to_province = {v: k for k, v in self.province_to_idx.items()}

            # Initialize custom model and tokenizer
            self.device = torch.device("cpu")
            self.model = AddressTransformer(num_cities=len(self.city_to_idx), num_provinces=len(self.province_to_idx)).to(self.device)
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
            self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
            print("Custom model (ADG) loaded.")
        else:
            self.llm = initialize_model(remote, llama_model, remote_api_base, remote_api_key)
            print(f"Using llama model: {self.llm}")

    def lookup(self, address):
        # Clean the address
        address = clean_address(address)

        if hasattr(self, 'model'):  # Use custom model if initialized (ADG)
            inputs = self.tokenizer(address, return_tensors="pt", padding="max_length", truncation=True, max_length=128)
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)

            with torch.no_grad():
                city_logits, province_logits = self.model(input_ids, attention_mask)

            predicted_city_idx = torch.argmax(city_logits, dim=1).item()
            predicted_province_idx = torch.argmax(province_logits, dim=1).item()

            city = self.idx_to_city.get(predicted_city_idx, "Unknown")
            state_abbr = self.idx_to_province.get(predicted_province_idx, "Unknown")

            # Look up the full state/province name based on the abbreviation
            state_full = self.abbreviation_to_fullname.get(state_abbr, state_abbr)

            country = "Canada" if state_abbr in self.canadian_postal_codes["PROVINCE_ABBR"].values else "America"

        else:
            # Generate prompt for LLM model
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
                # Invoke model and check if it returned data
                data = invoke_model(self.llm, prompt)
                if data is None:
                    return {'city': 'Unknown', 'state_full': 'Unknown', 'latitude': None, 'longitude': None, 'valid': 0}
                
                # Retrieve data safely and handle missing fields gracefully
                city = correct_spelling(data.get('city', 'Unknown'), self.spell_checker)
                state_full = data.get('state_or_province', 'Unknown')
                state_abbr = data.get('state_or_province_abbreviation', 'Unknown')
                country = data.get('country', 'Unknown')

            except Exception as e:
                return {'city': 'Unknown', 'state_full': 'Unknown', 'latitude': None, 'longitude': None, 'valid': 0}

        # Geolocation lookup
        if country == 'Canada':
            lat, long = lookup_lat_long_canada(self.canadian_postal_codes, city, state_abbr)
        elif country == 'America':
            lat, long = lookup_lat_long_us(self.us_zip_codes, city, state_abbr)
        else:
            lat = long = None

        if lat is None or long is None:
            google_query = f"{city} {state_full} latitude and longitude"
            lat, long = get_lat_long(google_query)

        # Save result
        result_dict = {
            'city': city.upper(),
            'state_full': state_full.upper(),
            'latitude': lat,
            'longitude': long,
            'valid': int(lat is not None and long is not None)
        }
        output_file = self.success_output if result_dict['valid'] else self.failed_path
        with open(output_file, 'a') as f:
            f.write(json.dumps(result_dict) + "\n")

        return result_dict


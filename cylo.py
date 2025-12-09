import requests
import urllib.parse

__ENDPOINT_URL__: str = "https://cpmjbc.squareweb.app/api"

class Bubcyz:
    def __init__(self) -> None:
        self.auth_token = None
    
    def login(self, email, password) -> int:
        payload = { "account_email": email, "account_password": password }
        response = requests.post(f"{__ENDPOINT_URL__}/account_login", data=payload)
        response_decoded = response.json()
        if response_decoded.get("ok"):
            self.auth_token = response_decoded.get("auth")
        return response_decoded.get("error")
    
    def change_email(self, new_email):
        decoded_email = urllib.parse.unquote(new_email)
        payload = {
            "account_auth": self.auth_token,
            "new_email": decoded_email
        }
        response = requests.post(f"{__ENDPOINT_URL__}/change_email", data=payload)
        response_decoded = response.json()
        if response_decoded.get("new_token"):
            self.auth_token = response_decoded["new_token"]
        return response_decoded.get("ok")
    
    def change_password(self, new_password):
        payload = { "account_auth": self.auth_token, "new_password": new_password }
        response = requests.post(f"{__ENDPOINT_URL__}/change_password", data=payload)
        response_decoded = response.json()
        if response_decoded.get("new_token"):
            self.auth_token = response_decoded["new_token"]
        return response_decoded.get("ok")
        
    def register(self, email, password) -> int:
        payload = { "account_email": email, "account_password": password }
        response = requests.post(f"{__ENDPOINT_URL__}/account_register", data=payload)
        response_decoded = response.json()
        return response_decoded.get("error")
    
    def delete(self):
        payload = { "account_auth": self.auth_token }
        requests.post(f"{__ENDPOINT_URL__}/account_delete", data=payload)

    def get_player_data(self) -> any:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/get_data", data=payload)
        response_decoded = response.json()
        return response_decoded
    
    def set_player_rank(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/set_rank", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def set_player_money(self, amount) -> bool:
        payload = {
            "account_auth": self.auth_token,
            "amount": amount
        }
        response = requests.post(f"{__ENDPOINT_URL__}/set_money", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def set_player_coins(self, amount) -> bool:
        payload = {
            "account_auth": self.auth_token,
            "amount": amount
        }
        response = requests.post(f"{__ENDPOINT_URL__}/set_coins", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def set_player_name(self, name) -> bool:
        payload = { "account_auth": self.auth_token, "name": name }
        response = requests.post(f"{__ENDPOINT_URL__}/set_name", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def set_player_localid(self, id) -> bool:
        payload = { "account_auth": self.auth_token, "id": id }
        response = requests.post(f"{__ENDPOINT_URL__}/set_id", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def get_player_car(self, car_id) -> any:
        payload = { "account_auth": self.auth_token, "car_id": car_id }
        response = requests.post(f"{__ENDPOINT_URL__}/get_car", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def delete_player_friends(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/delete_friends", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def unlock_w16(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_w16", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def unlock_horns(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_horns", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def disable_engine_damage(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/disable_damage", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlimited_fuel(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlimited_fuel", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def set_player_wins(self, amount) -> bool:
        payload = {
            "account_auth": self.auth_token,
            "amount": amount
        }
        response = requests.post(f"{__ENDPOINT_URL__}/set_race_wins", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def set_player_loses(self, amount) -> bool:
        payload = {
            "account_auth": self.auth_token,
            "amount": amount
        }
        response = requests.post(f"{__ENDPOINT_URL__}/set_race_loses", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_houses(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_houses", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def unlock_smoke(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_smoke", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def unlock_paid_cars(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_paid_cars", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def unlock_all_cars(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_all_cars", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def unlock_all_cars_siren(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_all_cars_siren", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def account_clone(self, account_email, account_password) -> bool:
        payload = { "account_auth": self.auth_token, "account_email": account_email, "account_password": account_password }
        response = requests.post(f"{__ENDPOINT_URL__}/clone", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
        
    def set_player_plates(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/set_plates", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_wheels(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_wheels", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_equipments_male(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_equipments_male", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_equipments_female(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_equipments_female", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def hack_car_speed(self, car_id, new_hp, new_inner_hp, new_nm, new_torque):
        payload = {
            "account_auth": self.auth_token,
            "car_id": car_id,
            "new_hp": new_hp,
            "new_inner_hp": new_inner_hp,
            "new_nm": new_nm,
            "new_torque": new_torque,
        }
        response = requests.post(f"{__ENDPOINT_URL__}/hack_car_speed", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def unlock_animations(self) -> bool:
        payload = { "account_auth": self.auth_token }
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_animations", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def max_max1(self, car_id, custom):
        payload = {
        "account_auth": self.auth_token,
        "car_id": car_id,
        "custom": custom,
        }
        response = requests.post(f"{__ENDPOINT_URL__}/max_max1", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
        
    def max_max2(self, car_id, custom):
        payload = {
        "account_auth": self.auth_token,
        "car_id": car_id,
        "custom": custom,
        }
        response = requests.post(f"{__ENDPOINT_URL__}/max_max2", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
        
    def millage_car(self, car_id, custom):
        payload = {
        "account_auth": self.auth_token,
        "car_id": car_id,
        "custom": custom,
        }
        response = requests.post(f"{__ENDPOINT_URL__}/millage_car", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def brake_car(self, car_id, custom):
        payload = {
        "account_auth": self.auth_token,
        "car_id": car_id,
        "custom": custom,
        }
        response = requests.post(f"{__ENDPOINT_URL__}/brake_car", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")

    def unlock_crown(self) -> bool: 
        payload = { "account_auth": self.auth_token } 
        response = requests.post(f"{__ENDPOINT_URL__}/unlock_crown", data=payload) 
        response_decoded = response.json() 
        return response_decoded.get("ok")
        
    def shittin(self) -> bool: 
        payload = { "account_auth": self.auth_token } 
        response = requests.post(f"{__ENDPOINT_URL__}/shittin", data=payload) 
        response_decoded = response.json() 
        return response_decoded.get("ok")

    def testin(self, custom):
        payload = {
        "account_auth": self.auth_token,
        "custom": custom,
        }
        response = requests.post(f"{__ENDPOINT_URL__}/testin", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
    
    def telmunnongodz(self, car_id, custom):
        payload = {
        "account_auth": self.auth_token,
        "car_id": car_id,
        "custom": custom,
        }
        response = requests.post(f"{__ENDPOINT_URL__}/telmunnongodz", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
        
    def telmunnongonz(self, car_id, custom):
        payload = {
        "account_auth": self.auth_token,
        "car_id": car_id,
        "custom": custom,
        }
        response = requests.post(f"{__ENDPOINT_URL__}/telmunnongonz", data=payload)
        response_decoded = response.json()
        return response_decoded.get("ok")
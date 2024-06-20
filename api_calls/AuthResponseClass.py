import datetime
import json
from json import JSONEncoder

class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

class AuthResponse:
    def __init__(self, jsonObject):
        self.access_token = jsonObject["access_token"]
        self.token_type = jsonObject["token_type"]
        self.refresh_token = jsonObject["refresh_token"]
        self.expires_in = jsonObject["expires_in"]
        self.refresh_expires_in = jsonObject["refresh_expires_in"]
        self.membership_id = jsonObject["membership_id"]
        if ("date" in jsonObject):
            self.date = datetime.datetime.fromisoformat(jsonObject["date"])
        else:
            self.date = datetime.datetime.now()

    def __str__(self):
        return "access_token: " + self.access_token + "\ntoken_type: " + self.token_type + "\nrefresh_token: " + self.refresh_token + "\nexpires_in: " + str(self.expires_in) + "\nrefresh_expires_in: " + str(self.refresh_expires_in) + "\nmembership_id: " + self.membership_id

    def __repr__(self):
        return "access_token: " + self.access_token + "\ntoken_type: " + self.token_type + "\nrefresh_token: " + self.refresh_token + "\nexpires_in: " + str(self.expires_in) + "\nrefresh_expires_in: " + str(self.refresh_expires_in) + "\nmembership_id: " + self.membership_id

    def __eq__(self, other):
        if isinstance(other, AuthResponse):
            return self.access_token == other.access_token and self.token_type == other.token_type and self.refresh_token == other.refresh_token and self.expires_in == other.expires_in and self.refresh_expires_in == other.refresh_expires_in and self.membership_id == other.membership_id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.access_token, self.token_type, self.refresh_token, self.expires_in, self.refresh_expires_in, self.membership_id))

    def __contains__(self, item):
        return item in (self.access_token, self.token_type, self.refresh_token, self.expires_in, self.refresh_expires_in, self.membership_id)

    def __getitem__(self, item):
        if item == "access_token":
            return self.access_token
        elif item == "token_type":
            return self.token_type
        elif item == "refresh_token":
            return self.refresh_token
        elif item == "expires_in":
            return self.expires_in
        elif item == "refresh_expires_in":
            return self.refresh_expires_in

    def toJson (self) :
        selfJSON = {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "refresh_expires_in": self.refresh_expires_in,
            "membership_id": self.membership_id,
            "date": self.date
        }
        return json.dumps(selfJSON, cls=DateTimeEncoder)

    def isRereshExpired(self):
        return (datetime.datetime.now() - self.date).total_seconds() >= self.refresh_expires_in

    def isExpired(self):
        return (datetime.datetime.now() - self.date).total_seconds() >= self.expires_in
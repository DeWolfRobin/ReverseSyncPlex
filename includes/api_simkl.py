#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import json
import time
import os

import http.client

from dotenv import load_dotenv
load_dotenv()
BASEURL = os.environ.get("BASEURL")
SIMKLCLIENTID = os.environ.get("SIMKLCLIENTID")
SIMKLCLIENTSECRET = os.environ.get("SIMKLCLIENTSECRET")
SIMKLAPITOKEN = os.environ.get("SIMKLAPITOKEN")

REDIRECT_URI = BASEURL
APIKEY = SIMKLCLIENTID
SECRET = SIMKLCLIENTSECRET
token = SIMKLAPITOKEN


class Simkl:
    def __init__(self):
        self.userSettings = {}
        self.isLoggedIn = False
        self.loginInProgress = False

        self.headers = {"Content-Type": "application-json", "simkl-api-key": APIKEY}
        if token:
            self.headers["authorization"] = "Bearer " + token
            r = self.get_user_settings()
            if r:
                print(r)
                return
            elif r is None:
                print("Error:", r)
                return
        # self.login()

    def get_user_settings(self):
        r = self._http("/users/settings", headers=self.headers)
        if isinstance(r, dict):
            self.userSettings = r
            self.isLoggedIn = True
            print("Usersettings = " + str(self.userSettings))
            return True
        return r

    def get_all_items(self):
        r = self._http("/sync/all-items/", headers=self.headers)
        return r

    # def login(self):
    #     if self.loginInProgress: return
    #     self.loginInProgress = True
    #
    #     if not self.isLoggedIn:
    #         rdic = self._http("/oauth/pin?client_id=" + APIKEY + "&redirect=" + REDIRECT_URI, headers=self.headers)
    #
    #         if isinstance(rdic, dict) and "error" not in rdic.keys():
    #             pin = rdic["user_code"]
    #             url = rdic["verification_url"]
    #
    #             login = LoginDialog("simkl-LoginDialog.xml", __addon__.getAddonInfo("path"), pin=pin, url=url,
    #                                 pin_check=self.pin_check, pin_success=self.pin_success)
    #             login.doModal()
    #             del login
    #     else:
    #         notify(get_str(32025).format(self.userSettings["user"]["name"]))
    #     self.loginInProgress = False

    # def pin_check(self, pin):
    #     r = self._http("/oauth/pin/" + pin + "?client_id=" + APIKEY, headers=self.headers)
    #     log("PIN Check = " + str(r))
    #     if r["result"] == "OK":
    #         set_setting('token', r["access_token"])
    #         self.headers["authorization"] = "Bearer " + r["access_token"]
    #         return self.get_user_settings()
    #     elif r["result"] == "KO":
    #         return False
    #
    # def pin_success(self):
    #     notify(get_str(32030).format(self.userSettings["user"]["name"]))

    def detect_by_file(self, filename):
        values = json.dumps({"file": filename})
        r = self._http("/search/file/", headers=self.headers, body=values)
        if r:
            log("Response: {0}".format(r))
        return r

    def mark_as_watched(self, item):
        if not item: return False

        log("MARK: {0}".format(item))
        _watched_at = time.strftime('%Y-%m-%d %H:%M:%S')
        _count = 0

        s_data = {}
        if item["type"] == "episodes":
            s_data[item["type"]] = [{
                "watched_at": _watched_at,
                "ids": {
                    "simkl": item["simkl"]
                }
            }]
        elif item["type"] == "shows":
            # TESTED
            s_data[item["type"]] = [{
                "title": item["title"],
                "ids": item['ids'],
                "seasons": [{
                    "number": item['season'],
                    "episodes": [{
                        "number": item['episode']
                    }]
                }]
            }]
        elif item["type"] == "movies":
            _prep = {
                "title": item["title"],
                "year": item["year"],
            }
            if "simkl" in item:
                _prep["ids"] = {"simkl": item["simkl"]}
            elif "ids" in item:
                _prep["ids"] = item['ids']

            s_data[item["type"]] = [_prep]

        log("Send: {0}".format(json.dumps(s_data)))
        while True and s_data:
            r = self._http("/sync/history/", body=json.dumps(s_data), headers=self.headers)
            if r is None: return False
            break
        return True

    def _http(self, url, headers={}, body=None, is_json=True):
        try:
            con = http.client.HTTPSConnection("api.simkl.com")
            con.request("GET", url, headers=headers, body=body)
            r = con.getresponse().read().decode("utf-8")
            if r.find('user_token_failed') != -1:
                self.isLoggedIn = False
                print("User token failed")
                return False
            return json.loads(r) if is_json else r
        except Exception as e:
            print(e)
            return None

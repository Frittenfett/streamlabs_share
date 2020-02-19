# ---------------------------------------
#   Import Libraries
# ---------------------------------------
import json
import codecs
import os
import clr
import time

clr.AddReference("IronPython.Modules.dll")
import urllib

# ---------------------------------------
#   [Required]  Script Information
# ---------------------------------------
ScriptName = "Share"
Website = "https://www.twitch.tv/frittenfettsenpai"
Description = "Share currency to all viewers."
Creator = "frittenfettsenpai"
Version = "1.0.1"


# ---------------------------------------
#   [Required] Intialize Data (Only called on Load)
# ---------------------------------------
def Init():
    global settings
    settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")

    try:
        with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
            settings = json.load(f, encoding="utf-8")
    except:
        settings = {
            "command": "!share",
            "minimumAmount": 100,
            "userBlackList": "",
            "showWinnerNames": False,
            "languageErrorMissingArgument": "Error! Please type a argument behind the command: {0} 5000",
            "languageErrorNotEnoughCurrency": "You don't have {0} {1}!",
            "languageErrorLessMinimumAmount": "Error! The amount to share should be bigger than {0} {1}!",
            "languageDone": "{0} shared {1} {2} to EVERYONE! ( {3} {2} per person [ {4} Viewers ])",
            "languageWinners": "The lucky are: {0}",
        }
    return


# ---------------------------------------
#   [Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    global settings
    if data.IsChatMessage():
        user = data.User
        username = Parent.GetDisplayName(user)

        if (data.GetParam(0).lower() == settings["command"]):
            if data.GetParamCount() < 1:
                Parent.SendTwitchMessage(settings["languageErrorMissingArgument"].format(settings["command"]))
                return

            currencyToShare = int(data.GetParam(1))
            if currencyToShare < settings["minimumAmount"]:
                Parent.SendTwitchMessage(settings["languageErrorLessMinimumAmount"].format(settings["minimumAmount"], Parent.GetCurrencyName()))
                return

            if (Parent.GetPoints(user) < currencyToShare):
                Parent.SendTwitchMessage(settings["languageErrorNotEnoughCurrency"].format(str(currencyToShare), Parent.GetCurrencyName()))
                return

            userBlackList = settings["userBlackList"].split(",")

            viewerListRaw = Parent.GetActiveUsers()
            viewerList = []
            for viewer in viewerListRaw:
                if viewer != username.lower() and viewer not in userBlackList:
                    viewerList.append(viewer)

            viewerCount = len(viewerList)
            pricePerPerson = int(currencyToShare / viewerCount)
            if pricePerPerson < 1:
                pricePerPerson = 1

            if len(viewerList) > 0:
                Parent.RemovePoints(user, currencyToShare)
                for viewer in viewerList:
                    Parent.AddPoints(viewer, pricePerPerson)

                Parent.SendTwitchMessage(settings["languageDone"].format(username, str(currencyToShare), Parent.GetCurrencyName(), pricePerPerson, str(viewerCount)))
                if settings["showWinnerNames"]:
                    Parent.SendTwitchMessage(settings["languageWinners"].format(' '.join(viewerList)))
    return


# ---------------------------------------
#	[Required] Tick Function
# ---------------------------------------
def Tick():
    return
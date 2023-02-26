# wom.py - An asynchronous wrapper for the Wise Old Man API.
# Copyright (c) 2023-present Jonxslays
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from wom.enums import BaseEnum

__all__ = ("GroupRole",)


class GroupRole(BaseEnum):
    """Roles that can be assigned to group members."""

    Achiever = "achiever"
    Adamant = "adamant"
    Adept = "adept"
    Administrator = "administrator"
    Admiral = "admiral"
    Adventurer = "adventurer"
    Air = "air"
    Anchor = "anchor"
    Apothecary = "apothecary"
    Archer = "archer"
    Armadylean = "armadylean"
    Artillery = "artillery"
    Artisan = "artisan"
    Asgarnian = "asgarnian"
    Assassin = "assassin"
    Assistant = "assistant"
    Astral = "astral"
    Athlete = "athlete"
    Attacker = "attacker"
    Bandit = "bandit"
    Bandosian = "bandosian"
    Barbarian = "barbarian"
    Battlemage = "battlemage"
    Beast = "beast"
    Berserker = "berserker"
    Blisterwood = "blisterwood"
    Blood = "blood"
    Blue = "blue"
    Bob = "bob"
    Body = "body"
    Brassican = "brassican"
    Brawler = "brawler"
    Brigadier = "brigadier"
    Brigand = "brigand"
    Bronze = "bronze"
    Bruiser = "bruiser"
    Bulwark = "bulwark"
    Burglar = "burglar"
    Burnt = "burnt"
    Cadet = "cadet"
    Captain = "captain"
    Carry = "carry"
    Champion = "champion"
    Chaos = "chaos"
    Cleric = "cleric"
    Collector = "collector"
    Colonel = "colonel"
    Commander = "commander"
    Competitor = "competitor"
    Completionist = "completionist"
    Constructor = "constructor"
    Cook = "cook"
    Coordinator = "coordinator"
    Corporal = "corporal"
    Cosmic = "cosmic"
    Councillor = "councillor"
    Crafter = "crafter"
    Crew = "crew"
    Crusader = "crusader"
    Cutpurse = "cutpurse"
    Death = "death"
    Defender = "defender"
    Defiler = "defiler"
    Deputy_owner = "deputy_owner"
    Destroyer = "destroyer"
    Diamond = "diamond"
    Diseased = "diseased"
    Doctor = "doctor"
    Dogsbody = "dogsbody"
    Dragon = "dragon"
    Dragonstone = "dragonstone"
    Druid = "druid"
    Duellist = "duellist"
    Earth = "earth"
    Elite = "elite"
    Emerald = "emerald"
    Enforcer = "enforcer"
    Epic = "epic"
    Executive = "executive"
    Expert = "expert"
    Explorer = "explorer"
    Farmer = "farmer"
    Feeder = "feeder"
    Fighter = "fighter"
    Fire = "fire"
    Firemaker = "firemaker"
    Firestarter = "firestarter"
    Fisher = "fisher"
    Fletcher = "fletcher"
    Forager = "forager"
    Fremennik = "fremennik"
    Gamer = "gamer"
    Gatherer = "gatherer"
    General = "general"
    Gnome_child = "gnome_child"
    Gnome_elder = "gnome_elder"
    Goblin = "goblin"
    Gold = "gold"
    Goon = "goon"
    Green = "green"
    Grey = "grey"
    Guardian = "guardian"
    Guthixian = "guthixian"
    Harpoon = "harpoon"
    Healer = "healer"
    Hellcat = "hellcat"
    Helper = "helper"
    Herbologist = "herbologist"
    Hero = "hero"
    Holy = "holy"
    Hoarder = "hoarder"
    Hunter = "hunter"
    Ignitor = "ignitor"
    Illusionist = "illusionist"
    Imp = "imp"
    Infantry = "infantry"
    Inquisitor = "inquisitor"
    Iron = "iron"
    Jade = "jade"
    Justiciar = "justiciar"
    Kandarin = "kandarin"
    Karamjan = "karamjan"
    Kharidian = "kharidian"
    Kitten = "kitten"
    Knight = "knight"
    Labourer = "labourer"
    Law = "law"
    Leader = "leader"
    Learner = "learner"
    Legacy = "legacy"
    Legend = "legend"
    Legionnaire = "legionnaire"
    Lieutenant = "lieutenant"
    Looter = "looter"
    Lumberjack = "lumberjack"
    Magic = "magic"
    Magician = "magician"
    Major = "major"
    Maple = "maple"
    Marshal = "marshal"
    Master = "master"
    Maxed = "maxed"
    Mediator = "mediator"
    Medic = "medic"
    Mentor = "mentor"
    Member = "member"
    Merchant = "merchant"
    Mind = "mind"
    Miner = "miner"
    Minion = "minion"
    Misthalinian = "misthalinian"
    Mithril = "mithril"
    Moderator = "moderator"
    Monarch = "monarch"
    Morytanian = "morytanian"
    Mystic = "mystic"
    Myth = "myth"
    Natural = "natural"
    Nature = "nature"
    Necromancer = "necromancer"
    Ninja = "ninja"
    Noble = "noble"
    Novice = "novice"
    Nurse = "nurse"
    Oak = "oak"
    Officer = "officer"
    Onyx = "onyx"
    Opal = "opal"
    Oracle = "oracle"
    Orange = "orange"
    Owner = "owner"
    Page = "page"
    Paladin = "paladin"
    Pawn = "pawn"
    Pilgrim = "pilgrim"
    Pine = "pine"
    Pink = "pink"
    Prefect = "prefect"
    Priest = "priest"
    Private = "private"
    Prodigy = "prodigy"
    Proselyte = "proselyte"
    Prospector = "prospector"
    Protector = "protector"
    Pure = "pure"
    Purple = "purple"
    Pyromancer = "pyromancer"
    Quester = "quester"
    Racer = "racer"
    Raider = "raider"
    Ranger = "ranger"
    Record_chaser = "record_chaser"
    Recruit = "recruit"
    Recruiter = "recruiter"
    Red_topaz = "red_topaz"
    Red = "red"
    Rogue = "rogue"
    Ruby = "ruby"
    Rune = "rune"
    Runecrafter = "runecrafter"
    Sage = "sage"
    Sapphire = "sapphire"
    Saradominist = "saradominist"
    Saviour = "saviour"
    Scavenger = "scavenger"
    Scholar = "scholar"
    Scourge = "scourge"
    Scout = "scout"
    Scribe = "scribe"
    Seer = "seer"
    Senator = "senator"
    Sentry = "sentry"
    Serenist = "serenist"
    Sergeant = "sergeant"
    Shaman = "shaman"
    Sheriff = "sheriff"
    Short_green_guy = "short_green_guy"
    Skiller = "skiller"
    Skulled = "skulled"
    Slayer = "slayer"
    Smiter = "smiter"
    Smith = "smith"
    Smuggler = "smuggler"
    Sniper = "sniper"
    Soul = "soul"
    Specialist = "specialist"
    Speed_runner = "speed_runner"
    Spellcaster = "spellcaster"
    Squire = "squire"
    Staff = "staff"
    Steel = "steel"
    Strider = "strider"
    Striker = "striker"
    Summoner = "summoner"
    Superior = "superior"
    Supervisor = "supervisor"
    Teacher = "teacher"
    Templar = "templar"
    Therapist = "therapist"
    Thief = "thief"
    Tirannian = "tirannian"
    Trialist = "trialist"
    Trickster = "trickster"
    Tzkal = "tzkal"
    Tztok = "tztok"
    Unholy = "unholy"
    Vagrant = "vagrant"
    Vanguard = "vanguard"
    Walker = "walker"
    Wanderer = "wanderer"
    Warden = "warden"
    Warlock = "warlock"
    Warrior = "warrior"
    Water = "water"
    Wild = "wild"
    Willow = "willow"
    Wily = "wily"
    Wintumber = "wintumber"
    Witch = "witch"
    Wizard = "wizard"
    Worker = "worker"
    Wrath = "wrath"
    Xerician = "xerician"
    Yellow = "yellow"
    Yew = "yew"
    Zamorakian = "zamorakian"
    Zarosian = "zarosian"
    Zealot = "zealot"
    Zenyte = "zenyte"
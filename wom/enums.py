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

"""Global enums used throughout the project."""

from __future__ import annotations

import typing as t
from enum import Enum

T = t.TypeVar("T", bound="BaseEnum")

__all__ = (
    "Activities",
    "BaseEnum",
    "Bosses",
    "ComputedMetrics",
    "Metric",
    "Period",
    "Skills",
)


class BaseEnum(Enum):
    """The base enum all library enums inherit from."""

    def __str__(self) -> str:
        return self.value  # type: ignore[no-any-return]

    @classmethod
    def from_str(cls: t.Type[T], value: str) -> T:
        """Generate this enum from the given value.

        Args:
            value: The value to generate from.

        Returns:
            The generated enum.
        """
        try:
            return cls(value)
        except ValueError as e:
            raise ValueError(
                f"{e} variant. Please report this issue on github at "
                "https://github.com/Jonxslays/wom.py/issues/new"
            ) from None

    @classmethod
    def from_str_maybe(cls: t.Type[T], value: str) -> t.Optional[T]:
        """Attempt to generate this enum from the given value.

        Args:
            value: The value to generate from.

        Returns:
            The generated enum or `None` if the value was not a valid
                enum variant.
        """
        try:
            return cls(value)
        except ValueError:
            return None


class Metric(BaseEnum):
    """Represents a metric, this enum has no attributes itself.

    !!! tip

        Will always be one of [`Activities`][wom.Activities],
        [`Bosses`][wom.Bosses], [`ComputedMetrics`][wom.ComputedMetrics],
        or [`Skills`][wom.Skills].
    """

    @classmethod
    def from_str(cls: t.Type[T], value: str) -> T:
        if cls is not Metric:
            return super().from_str(value)

        children = {Skills, Activities, Bosses, ComputedMetrics}

        for child in children:
            try:
                return child(value)  # type: ignore
            except ValueError:
                continue

        raise ValueError(
            f"{value!r} is not a valid {cls.__name__} variant. "
            "Please report this issue on github at https://github.com/Jonxslays/wom.py/issues/new"
        )

    @classmethod
    def from_str_maybe(cls: t.Type[T], value: str) -> t.Optional[T]:
        if cls is not Metric:
            return super().from_str_maybe(value)  # pyright: ignore

        children = {Skills, Activities, Bosses, ComputedMetrics}

        for child in children:
            try:
                return child(value)  # type: ignore
            except ValueError:
                continue

        return None


class Period(BaseEnum):
    """A period of time used by the API."""

    FiveMins = "five_min"
    Day = "day"
    Week = "week"
    Month = "month"
    Year = "year"


class Skills(Metric):
    """Skills from OSRS."""

    Overall = "overall"
    Attack = "attack"
    Defence = "defence"
    Strength = "strength"
    Hitpoints = "hitpoints"
    Ranged = "ranged"
    Prayer = "prayer"
    Magic = "magic"
    Cooking = "cooking"
    Woodcutting = "woodcutting"
    Fletching = "fletching"
    Fishing = "fishing"
    Firemaking = "firemaking"
    Crafting = "crafting"
    Smithing = "smithing"
    Mining = "mining"
    Herblore = "herblore"
    Agility = "agility"
    Thieving = "thieving"
    Slayer = "slayer"
    Farming = "farming"
    Runecrafting = "runecrafting"
    Hunter = "hunter"
    Construction = "construction"


class Activities(Metric):
    """Activities from OSRS."""

    LeaguePoints = "league_points"
    BountyHunterHunter = "bounty_hunter_hunter"
    BountyHunterRogue = "bounty_hunter_rogue"
    ClueScrollsAll = "clue_scrolls_all"
    ClueScrollsBeginner = "clue_scrolls_beginner"
    ClueScrollsEasy = "clue_scrolls_easy"
    ClueScrollsMedium = "clue_scrolls_medium"
    ClueScrollsHard = "clue_scrolls_hard"
    ClueScrollsElite = "clue_scrolls_elite"
    ClueScrollsMaster = "clue_scrolls_master"
    LastManStanding = "last_man_standing"
    PvpArena = "pvp_arena"
    SoulWarsZeal = "soul_wars_zeal"
    GuardiansOfTheRift = "guardians_of_the_rift"


class Bosses(Metric):
    """Bosses from OSRS."""

    AbyssalSire = "abyssal_sire"
    AlchemicalHydra = "alchemical_hydra"
    Artio = "artio"
    BarrowsChests = "barrows_chests"
    Bryophyta = "bryophyta"
    Callisto = "callisto"
    Calvarion = "calvarion"
    Cerberus = "cerberus"
    ChambersOfXeric = "chambers_of_xeric"
    ChambersOfXericChallenge = "chambers_of_xeric_challenge_mode"
    ChaosElemental = "chaos_elemental"
    ChaosFanatic = "chaos_fanatic"
    CommanderZilyana = "commander_zilyana"
    CorporealBeast = "corporeal_beast"
    CrazyArchaeologist = "crazy_archaeologist"
    DagannothPrime = "dagannoth_prime"
    DagannothRex = "dagannoth_rex"
    DagannothSupreme = "dagannoth_supreme"
    DerangedArchaeologist = "deranged_archaeologist"
    DukeSucellus = "duke_sucellus"
    GeneralGraardor = "general_graardor"
    GiantMole = "giant_mole"
    GrotesqueGuardians = "grotesque_guardians"
    Hespori = "hespori"
    KalphiteQueen = "kalphite_queen"
    KingBlackDragon = "king_black_dragon"
    Kraken = "kraken"
    Kreearra = "kreearra"
    KrilTsutsaroth = "kril_tsutsaroth"
    Mimic = "mimic"
    Nex = "nex"
    Nightmare = "nightmare"
    PhosanisNightmare = "phosanis_nightmare"
    Obor = "obor"
    PhantomMuspah = "phantom_muspah"
    Sarachnis = "sarachnis"
    Scorpia = "scorpia"
    Skotizo = "skotizo"
    Spindel = "spindel"
    Tempoross = "tempoross"
    TheGauntlet = "the_gauntlet"
    TheCorruptedGauntlet = "the_corrupted_gauntlet"
    TheLeviathan = "the_leviathan"
    TheWhisperer = "the_whisperer"
    TheatreOfBlood = "theatre_of_blood"
    TheatreOfBloodHard = "theatre_of_blood_hard_mode"
    ThermonuclearSmokeDevil = "thermonuclear_smoke_devil"
    TombsOfAmascut = "tombs_of_amascut"
    TombsOfAmascutExpert = "tombs_of_amascut_expert"
    TzKalZuk = "tzkal_zuk"
    TzTokJad = "tztok_jad"
    Vardorvis = "vardorvis"
    Venenatis = "venenatis"
    Vetion = "vetion"
    Vorkath = "vorkath"
    Wintertodt = "wintertodt"
    Zalcano = "zalcano"
    Zulrah = "zulrah"


class ComputedMetrics(Metric):
    """A metric that is computed, i.e. efficient hours played and
    bossed.
    """

    Ehp = "ehp"
    Ehb = "ehb"

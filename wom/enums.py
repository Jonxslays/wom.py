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

import random
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseEnum):
            return self.value == other.value  # type: ignore[no-any-return]

        if isinstance(other, str):
            return self.value == other  # type: ignore[no-any-return]

        return super().__eq__(other)

    def __hash__(self) -> int:
        return hash(self.value)

    @classmethod
    def at_random(cls: t.Type[T]) -> T:
        """Generates a random variant of this enum.

        Returns:
            The randomly generated enum.
        """
        return random.choice(tuple(cls))


class Period(BaseEnum):
    """A period of time used by the API."""

    FiveMins = "five_min"
    Day = "day"
    Week = "week"
    Month = "month"
    Year = "year"


class Metric(BaseEnum):
    """Represents all metrics including skills, bosses, activities, and
    computed metrics.
    """

    # Skills
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

    # Activities
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
    CollectionsLogged = "collections_logged"
    ColosseumGlory = "colosseum_glory"
    LastManStanding = "last_man_standing"
    PvpArena = "pvp_arena"
    SoulWarsZeal = "soul_wars_zeal"
    GuardiansOfTheRift = "guardians_of_the_rift"

    # Bosses
    AbyssalSire = "abyssal_sire"
    AlchemicalHydra = "alchemical_hydra"
    Amoxliatl = "amoxliatl"
    Araxxor = "araxxor"
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
    Hueycoatl = "the_hueycoatl"
    KalphiteQueen = "kalphite_queen"
    KingBlackDragon = "king_black_dragon"
    Kraken = "kraken"
    Kreearra = "kreearra"
    KrilTsutsaroth = "kril_tsutsaroth"
    LunarChests = "lunar_chests"
    Mimic = "mimic"
    Nex = "nex"
    Nightmare = "nightmare"
    PhosanisNightmare = "phosanis_nightmare"
    Obor = "obor"
    PhantomMuspah = "phantom_muspah"
    Sarachnis = "sarachnis"
    Scorpia = "scorpia"
    Scurrius = "scurrius"
    Skotizo = "skotizo"
    SolHeredit = "sol_heredit"
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

    # Computed Metrics
    Ehp = "ehp"
    Ehb = "ehb"


ComputedMetrics: t.FrozenSet[Metric] = frozenset({Metric.Ehp, Metric.Ehb})
"""Set containing all the types of computed metrics."""

Skills: t.FrozenSet[Metric] = frozenset(
    {
        Metric.Overall,
        Metric.Attack,
        Metric.Defence,
        Metric.Strength,
        Metric.Hitpoints,
        Metric.Ranged,
        Metric.Prayer,
        Metric.Magic,
        Metric.Cooking,
        Metric.Woodcutting,
        Metric.Fletching,
        Metric.Fishing,
        Metric.Firemaking,
        Metric.Crafting,
        Metric.Smithing,
        Metric.Mining,
        Metric.Herblore,
        Metric.Agility,
        Metric.Thieving,
        Metric.Slayer,
        Metric.Farming,
        Metric.Runecrafting,
        Metric.Hunter,
        Metric.Construction,
    }
)
"""Set containing skills."""

Activities: t.FrozenSet[Metric] = frozenset(
    {
        Metric.LeaguePoints,
        Metric.BountyHunterHunter,
        Metric.BountyHunterRogue,
        Metric.ClueScrollsAll,
        Metric.ClueScrollsBeginner,
        Metric.ClueScrollsEasy,
        Metric.ClueScrollsMedium,
        Metric.ClueScrollsHard,
        Metric.ClueScrollsElite,
        Metric.ClueScrollsMaster,
        Metric.CollectionsLogged,
        Metric.ColosseumGlory,
        Metric.LastManStanding,
        Metric.PvpArena,
        Metric.SoulWarsZeal,
        Metric.GuardiansOfTheRift,
    }
)
"""Set containing activities."""

Bosses: t.FrozenSet[Metric] = frozenset(
    {
        Metric.AbyssalSire,
        Metric.AlchemicalHydra,
        Metric.Amoxliatl,
        Metric.Araxxor,
        Metric.Artio,
        Metric.BarrowsChests,
        Metric.Bryophyta,
        Metric.Callisto,
        Metric.Calvarion,
        Metric.Cerberus,
        Metric.ChambersOfXeric,
        Metric.ChambersOfXericChallenge,
        Metric.ChaosElemental,
        Metric.ChaosFanatic,
        Metric.CommanderZilyana,
        Metric.CorporealBeast,
        Metric.CrazyArchaeologist,
        Metric.DagannothPrime,
        Metric.DagannothRex,
        Metric.DagannothSupreme,
        Metric.DerangedArchaeologist,
        Metric.DukeSucellus,
        Metric.GeneralGraardor,
        Metric.GiantMole,
        Metric.GrotesqueGuardians,
        Metric.Hespori,
        Metric.Hueycoatl,
        Metric.KalphiteQueen,
        Metric.KingBlackDragon,
        Metric.Kraken,
        Metric.Kreearra,
        Metric.KrilTsutsaroth,
        Metric.LunarChests,
        Metric.Mimic,
        Metric.Nex,
        Metric.Nightmare,
        Metric.PhosanisNightmare,
        Metric.Obor,
        Metric.PhantomMuspah,
        Metric.Sarachnis,
        Metric.Scorpia,
        Metric.Scurrius,
        Metric.Skotizo,
        Metric.SolHeredit,
        Metric.Spindel,
        Metric.Tempoross,
        Metric.TheGauntlet,
        Metric.TheCorruptedGauntlet,
        Metric.TheLeviathan,
        Metric.TheWhisperer,
        Metric.TheatreOfBlood,
        Metric.TheatreOfBloodHard,
        Metric.ThermonuclearSmokeDevil,
        Metric.TombsOfAmascut,
        Metric.TombsOfAmascutExpert,
        Metric.TzKalZuk,
        Metric.TzTokJad,
        Metric.Vardorvis,
        Metric.Venenatis,
        Metric.Vetion,
        Metric.Vorkath,
        Metric.Wintertodt,
        Metric.Zalcano,
        Metric.Zulrah,
    }
)
"""Set containing bosses."""

from enum import Enum
from typing import List, Dict

class AttackType(str, Enum):
    SYSTEM_PROMPT_OVERRIDE = "system_prompt_override"
    ROLE_MANIPULATION = "role_manipulation"
    CONTEXT_POISONING = "context_poisoning"
    OUTPUT_MANIPULATION = "output_manipulation"
    JAILBREAK = "jailbreak"

# Dictionary mapping attack types to lists of regex patterns
ATTACK_PATTERNS: Dict[AttackType, List[str]] = {
    AttackType.SYSTEM_PROMPT_OVERRIDE: [
        r"ignore.*(?:previous|all).*instructions",
        r"ignore.*(?:system|safety).*guidelines?",
        r"disregard.*(?:previous|all).*instructions",
        r"forget.*(?:previous|all).*instructions",
        r"override.*(?:system|safety).*instructions",
        r"reveal.*(?:system|hidden).*prompt",
        r"what.*are.*your.*instructions",
    ],
    AttackType.ROLE_MANIPULATION: [
        r"you.*are.*no.*longer.*(?:a|an|the).*",
        r"act.*as.*(?:a|an).*",
        r"pretend.*to.*be.*",
        r"roleplay.*as.*",
        r"from.*now.*on.*you.*are.*",
        r"stay.*in.*character",
    ],
    AttackType.OUTPUT_MANIPULATION: [
        r"output.*(?:as|in).*json", # Context dependent, but can be used to bypass
        r"output.*the.*following.*code",
        r"print.*(?:the|this).*",
        r"repeat.*after.*me",
    ],
    AttackType.JAILBREAK: [
        r"do.*anything.*now",
        r"dan.*mode",
        r"jailbreak",
        r"unfiltered",
        r"uncensored",
        r"always.*say.*yes",
    ]
}

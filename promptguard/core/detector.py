import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from .patterns import ATTACK_PATTERNS, AttackType
from .heuristics import HeuristicsEngine

@dataclass
class Config:
    sensitivity: float = 0.7
    enable_pattern_matching: bool = True
    enable_heuristics: bool = True
    enable_context_validation: bool = False # Not implemented in this version
    custom_patterns: List[str] = field(default_factory=list)
    application_context: Optional[str] = None
    block_threshold: float = 7.0
    review_threshold: float = 4.0

class PromptGuard:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.heuristics = HeuristicsEngine()
        
        # Compile patterns
        self._compiled_patterns = {}
        if self.config.enable_pattern_matching:
            for attack_type, patterns in ATTACK_PATTERNS.items():
                self._compiled_patterns[attack_type] = [
                    re.compile(p, re.IGNORECASE) for p in patterns
                ]
            
            # Add custom patterns under a generic category if they exist
            if self.config.custom_patterns:
                self._compiled_patterns["custom"] = [
                     re.compile(p, re.IGNORECASE) for p in self.config.custom_patterns
                ]

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze the input text for prompt injection attacks.
        """
        score = 0.0
        detected_patterns = []
        explanation = []
        
        # Layer 1: Pattern Matching
        if self.config.enable_pattern_matching:
            for category, patterns in self._compiled_patterns.items():
                for pattern in patterns:
                    if pattern.search(text):
                        # Base score for a pattern match. Multiple matches increase score.
                        score += 5.0 
                        detected_patterns.append(category if isinstance(category, str) else category.value)
                        explanation.append(f"Matched pattern in category: {category}")
                        break # Only match once per category to avoid double counting too aggressively? 
                              # Actually, let's break per category to avoid matching 10 variations of "ignore"
        
        # Layer 2: Heuristics
        if self.config.enable_heuristics:
            heuristic_result = self.heuristics.analyze(text)
            # Heuristics return a 0-1 score, we scale it to be meaningful (e.g. up to 3 points)
            score += heuristic_result["score"] * 3.0
            if heuristic_result["flags"]:
                explanation.append(f"Heuristics flags: {', '.join(heuristic_result['flags'])}")

        # Normalize score to 0-10
        score = min(score, 10.0)
        
        # Determine recommendation
        recommendation = "ALLOW"
        if score >= self.config.block_threshold:
            recommendation = "BLOCK"
        elif score >= self.config.review_threshold:
            recommendation = "REVIEW"
            
        return {
            "is_suspicious": score > 0,
            "risk_score": round(score, 1),
            "confidence": min(score / 10.0 + 0.1, 1.0) if score > 0 else 1.0, # Crude confidence metric
            "detected_patterns": list(set(detected_patterns)),
            "recommendation": recommendation,
            "explanation": "; ".join(explanation) if explanation else "No suspicious content detected"
        }

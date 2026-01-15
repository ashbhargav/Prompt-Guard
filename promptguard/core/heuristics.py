from typing import Dict, Any

class HeuristicsEngine:
    """
    Analyzes prompts for structural anomalies and other heuristic indicators
    of potential attacks.
    """
    
    def analyze(self, text: str) -> Dict[str, Any]:
        result = {
            "score": 0.0,
            "flags": []
        }
        
        # Check 1: Length anomalies (very short or very long prompts might be suspicious in certain contexts)
        # For general purpose, we might not penalize length heavily, but let's add a small check
        if len(text) > 10000:
             result["flags"].append("unusually_long_prompt")
             # No score increase for now, just flag
             
        # Check 2: Repetitive characters (often used in buffer overflow attempts or confusion)
        if self._has_repetitive_chars(text):
            result["score"] += 0.2
            result["flags"].append("repetitive_characters")
            
        # Check 3: Suspicious keyword density (rudimentary)
        # If the input has a high density of imperatives like "ignore", "forget", "override"
        imperatives = ["ignore", "forget", "override", "bypass", "hack"]
        count = sum(1 for word in text.lower().split() if word in imperatives)
        if count > 2:
             result["score"] += 0.3 * (count - 2) # Increase score for each extra imperative
             result["flags"].append("high_imperative_count")

        # Cap score at 1.0 (heuristics are just one part)
        result["score"] = min(result["score"], 1.0)
        
        return result

    def _has_repetitive_chars(self, text: str, threshold: int = 15) -> bool:
        """Check for long sequences of the same character."""
        count = 0
        last_char = ''
        for char in text:
            if char == last_char:
                count += 1
                if count >= threshold:
                    return True
            else:
                count = 1
                last_char = char
        return False

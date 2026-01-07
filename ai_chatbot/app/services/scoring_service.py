class ScoringService:
    """
    Handles lead scoring and status transitions.
    AI never decides score. This service does.
    """

    INTENT_SCORES = {
        "demo": 40,
        "pricing": 25,
        "feature": 15,
        "objection": 10,
        "casual": 5
    }

    INTEREST_BONUS = {
        "high": 20,
        "medium": 10,
        "low": 0
    }

    def calculate_score(self, intent: str, interest_level: str) -> int:
        """
        Calculate lead score based on intent and interest level
        """

        base_score = self.INTENT_SCORES.get(intent, 0)
        bonus_score = self.INTEREST_BONUS.get(interest_level, 0)

        return base_score + bonus_score

    def determine_status(self, total_score: int) -> str:
        """
        Decide lead status based on total score
        """

        if total_score >= 60:
            return "hot"
        elif total_score >= 30:
            return "warm"
        else:
            return "cold"

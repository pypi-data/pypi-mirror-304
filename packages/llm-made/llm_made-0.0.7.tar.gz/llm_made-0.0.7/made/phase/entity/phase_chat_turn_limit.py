from dataclasses import dataclass


@dataclass
class PhaseChatTurnLimit:
    demand_analysis: int = 2
    language_choose: int = 2
    coding: int = 5
    code_complete: int = 3
    code_review_comment: int = 1
    code_review_modification: int = 1
    test_error_summary: int = 1
    test_modification: int = 1
    manual: int = 4

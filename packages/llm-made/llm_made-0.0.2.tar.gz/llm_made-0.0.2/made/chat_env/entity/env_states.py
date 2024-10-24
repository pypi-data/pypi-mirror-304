from dataclasses import dataclass, field
from typing import Dict


@dataclass
class EnvStates:
    task_description: str = ""
    modality: str = ""
    ideas: str = ""
    language: str = ""
    review_comments: str = ""
    error_summary: str = ""
    test_reports: str = ""
    codes: Dict[str, str] = field(default_factory=dict)
    manual: str = ""
    requirements: str = ""

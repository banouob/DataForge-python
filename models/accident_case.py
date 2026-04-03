from __future__ import annotations
from typing import List
from models.person import Person


class AccidentCase:
    def __init__(self):
        self.case_number: str = ''
        self.persons: List[Person] = []

    def is_valid(self) -> bool:
        return bool(self.case_number)

    def add_person(self, person: Person):
        self.persons.append(person)

"""
===========================================================
Birth Rule Registry

Contains all rules executed for Birth datasets.
===========================================================
"""

from black import schema

from crdqe.rules.birth.date_of_birth import DateOfBirthRule
from crdqe.rules.birth.education import EducationRule
from crdqe.rules.birth.marital_status import MaritalStatusRule
from crdqe.rules.birth.nationality import NationalityRule
from crdqe.rules.birth.occupation import OccupationRule
from crdqe.rules.birth.place_consistency import PlaceConsistencyRule
from crdqe.rules.birth.place_of_birth import PlaceOfBirthRule
from crdqe.rules.birth.place_type import PlaceTypeRule
from crdqe.rules.birth.registration_date import RegistrationDateRule
from crdqe.rules.birth.residence import ResidenceRule
from crdqe.rules.birth.status import StatusRule
from crdqe.rules.birth.sex import SexRule
from crdqe.rules.birth.nature_of_birth import NatureOfBirthRule
from crdqe.rules.birth.birth_weight import BirthWeightRule
from crdqe.rules.birth.mother_age import MotherAgeRule
from crdqe.rules.birth.date_consistency import DateConsistencyRule
from crdqe.rules.birth.entry_number import EntryNumberRule
from crdqe.rules.birth.duplicate_entry_number import DuplicateEntryNumberRule


RULES = [
    DateOfBirthRule,
    RegistrationDateRule,
    DateConsistencyRule,
    StatusRule,
    SexRule,
    NatureOfBirthRule,
    BirthWeightRule,
    MotherAgeRule,
    PlaceOfBirthRule,
    PlaceTypeRule,
    PlaceConsistencyRule,
    OccupationRule,
    EducationRule,
    NationalityRule,
    ResidenceRule,
    MaritalStatusRule,
    EntryNumberRule,
    DuplicateEntryNumberRule,
    
]
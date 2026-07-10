"""
===========================================================
Birth Rule Registry

Contains all rules executed for Birth datasets.
===========================================================
"""

from crdqe.rules.birth.date_of_birth import DateOfBirthRule
from crdqe.rules.birth.occupation import OccupationRule
from crdqe.rules.birth.place_of_birth import PlaceOfBirthRule
from crdqe.rules.birth.registration_date import RegistrationDateRule
from crdqe.rules.birth.residence import ResidenceRule
from crdqe.rules.birth.status import StatusRule
from crdqe.rules.birth.sex import SexRule
from crdqe.rules.birth.nature_of_birth import NatureOfBirthRule
from crdqe.rules.birth.birth_weight import BirthWeightRule
from crdqe.rules.birth.mother_age import MotherAgeRule
from crdqe.rules.birth.date_consistency import DateConsistencyRule

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
    OccupationRule,
    ResidenceRule,

]
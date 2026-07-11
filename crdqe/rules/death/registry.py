from crdqe.rules.death.date_consistency import DateConsistencyRule

from crdqe.rules.death.date_of_death import DateOfDeathRule
from crdqe.rules.death.entry_number import EntryNumberRule
from crdqe.rules.death.registration_date import RegistrationDateRule
from crdqe.rules.death.status import StatusRule

from crdqe.rules.death.sex import SexRule
from crdqe.rules.death.age import AgeRule
from crdqe.rules.death.age_unit import AgeUnitRule

from crdqe.rules.death.place_of_death import PlaceOfDeathRule
from crdqe.rules.death.place_type import PlaceTypeRule

from crdqe.rules.death.marital_status import MaritalStatusRule
from crdqe.rules.death.residence import ResidenceRule

from crdqe.rules.death.id_number import IDNumberRule
from crdqe.rules.death.cause_of_death import CauseOfDeathRule
from crdqe.rules.death.certification import CertificationRule


RULES = [
    DateOfDeathRule,
    RegistrationDateRule,
    DateConsistencyRule,
    StatusRule,
    IDNumberRule,
    SexRule,
    AgeRule,
    AgeUnitRule,
    PlaceOfDeathRule,
    PlaceTypeRule,
    ResidenceRule,
    MaritalStatusRule,
    CauseOfDeathRule,
    CertificationRule,
    EntryNumberRule,
]
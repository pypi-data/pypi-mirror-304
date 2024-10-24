from __future__ import absolute_import

import pkg_resources
from permamodel.components.bmi_frost_number import BmiFrostnumberMethod as FrostNumber
from permamodel.components.bmi_Ku import BmiKuModel as KuEnhanced
from permamodel.components.bmi_Ku_component import BmiKuMethod as Ku

FrostNumber.__name__ = "FrostNumber"
FrostNumber.METADATA = pkg_resources.resource_filename(__name__, "data/FrostNumber")
Ku.__name__ = "Ku"
Ku.METADATA = pkg_resources.resource_filename(__name__, "data/Ku")
KuEnhanced.__name__ = "KuEnhanced"
KuEnhanced.METADATA = pkg_resources.resource_filename(__name__, "data/KuEnhanced")

__all__ = [
    "FrostNumber",
    "Ku",
    "KuEnhanced",
]

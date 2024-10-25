# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT
# VERSION = (0, 0, 2)   # del blank lines
# VERSION = (0, 0, 3)   # separate all types/exx into static.py!


# =====================================================================================================================
# TEMPLATE
# from .STATIC import (
#     # TYPES
#     # EXX
# )
# from .main import (
#     # BASE
#     # AUX
# )
# ---------------------------------------------------------------------------------------------------------------------
from .static import (
    # TYPES
    # EXX
    Exx__AnnotNotDefined,
)
from .annot_1_aux import (
    # BASE
    AnnotAux,
    # AUX
)
from .annot_3_iter_values import AnnotValuesIter
from .annot_2_all_defined import (
    # BASE
    AnnotAllDefined,
    # AUX
)
from .annot_4_cls_keys_as_values import (
    # BASE
    AnnotClsKeysAsValues,
    # AUX
    AnnotClsKeysAsValues_Meta,
)
# ---------------------------------------------------------------------------------------------------------------------
from .cmp import (
    # BASE
    CmpInst,
    # AUX
    # TYPES
    # EXX
)
from .number import (
    # BASE
    NumberArithmTranslateToAttr,
    # AUX
    # TYPES
    TYPE__NUMBER,
    # EXX
    Exx__NumberArithm_NoName,
)
# ---------------------------------------------------------------------------------------------------------------------
from .getattr_0_echo import (
    # BASE
    GetattrEcho,
    GetattrEchoSpace,
    # AUX
    # TYPES
    # EXX
)
from .getattr_1_aux import (
    # BASE
    GetattrAux,
    # AUX
    # TYPES
    # EXX
)
from .getattr_2_anycase import (
    # BASE
    GetattrAnycase,
    # AUX
    # TYPES
    # EXX
)
from .getattr_3_prefix_1_inst import (
    # BASE
    GetattrPrefixInst,
    GetattrPrefixInst_RaiseIf,
    # AUX
    # TYPES
    # EXX
    Exx__GetattrPrefix,
    Exx__GetattrPrefix_RaiseIf,
)
from .getattr_3_prefix_2_cls import GetattrPrefixCls_MetaTemplate

# ---------------------------------------------------------------------------------------------------------------------
from .middle_group import (
    # BASE
    ClsMiddleGroup,
    # AUX
    # TYPES
    # EXX
)


# =====================================================================================================================

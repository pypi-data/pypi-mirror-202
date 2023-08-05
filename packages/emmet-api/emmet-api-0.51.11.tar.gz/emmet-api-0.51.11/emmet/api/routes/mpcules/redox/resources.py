from maggma.api.resource import ReadOnlyResource
from emmet.core.molecules.redox import RedoxDoc

from maggma.api.query_operator import (
    NumericQuery,
    PaginationQuery,
    SortQuery,
    SparseFieldsQuery
)

from emmet.api.routes.mpcules.redox.query_operators import (
    RedoxPotentialQuery
)
from emmet.api.routes.mpcules.molecules.query_operators import (
    MultiMPculeIDQuery,
    ExactCalcMethodQuery,
    FormulaQuery,
    ChemsysQuery,
    ElementsQuery,
    ChargeSpinQuery
)
from emmet.api.routes.mpcules.utils import MultiPropertyIDQuery
from emmet.api.core.settings import MAPISettings
from emmet.api.core.global_header import GlobalHeaderProcessor


def redox_resource(redox_store):
    resource = ReadOnlyResource(
        redox_store,
        RedoxDoc,
        query_operators=[
            MultiMPculeIDQuery(),
            ExactCalcMethodQuery(),
            FormulaQuery(),
            ChemsysQuery(),
            ElementsQuery(),
            ChargeSpinQuery(),
            MultiPropertyIDQuery(),
            RedoxPotentialQuery(),
            NumericQuery(model=RedoxDoc),
            SortQuery(),
            PaginationQuery(),
            SparseFieldsQuery(RedoxDoc, default_fields=["molecule_id", "property_id", "solvent", "last_updated"],),
        ],
        header_processor=GlobalHeaderProcessor(),
        tags=["MPcules Redox"],
        sub_path="/redox/",
        disable_validation=True,
        timeout=MAPISettings().TIMEOUT,
    )

    return resource

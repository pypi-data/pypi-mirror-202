from emmet.core.summary import SummaryDoc

from maggma.api.query_operator import (
    PaginationQuery,
    SortQuery,
    SparseFieldsQuery,
    NumericQuery,
)
from maggma.api.resource import ReadOnlyResource, AggregationResource
from emmet.api.routes.materials.query_operators import (
    DeprecationQuery,
    ElementsQuery,
    FormulaQuery,
    ChemsysQuery,
    SymmetryQuery,
)
from emmet.api.routes.oxidation_states.query_operators import PossibleOxiStateQuery
from emmet.core.summary import SummaryStats
from emmet.api.routes.summary.hint_scheme import SummaryHintScheme
from emmet.api.routes.summary.query_operators import (
    HasPropsQuery,
    MaterialIDsSearchQuery,
    SearchIsStableQuery,
    SearchIsTheoreticalQuery,
    SearchMagneticQuery,
    SearchHasReconstructedQuery,
    SearchStatsQuery,
    SearchESQuery,
)

from emmet.api.core.global_header import GlobalHeaderProcessor
from emmet.api.core.settings import MAPISettings

timeout = MAPISettings().TIMEOUT


def summary_resource(summary_store):
    resource = ReadOnlyResource(
        summary_store,
        SummaryDoc,
        query_operators=[
            MaterialIDsSearchQuery(),
            FormulaQuery(),
            ChemsysQuery(),
            ElementsQuery(),
            PossibleOxiStateQuery(),
            SymmetryQuery(),
            SearchIsStableQuery(),
            SearchIsTheoreticalQuery(),
            SearchMagneticQuery(),
            SearchESQuery(),
            NumericQuery(model=SummaryDoc, excluded_fields=["composition"]),
            SearchHasReconstructedQuery(),
            HasPropsQuery(),
            DeprecationQuery(),
            SortQuery(),
            PaginationQuery(),
            SparseFieldsQuery(SummaryDoc, default_fields=["material_id"]),
        ],
        hint_scheme=SummaryHintScheme(),
        header_processor=GlobalHeaderProcessor(),
        tags=["Summary"],
        disable_validation=True,
        timeout=timeout
    )

    return resource


def summary_stats_resource(summary_store):
    resource = AggregationResource(
        summary_store,
        SummaryStats,
        pipeline_query_operator=SearchStatsQuery(SummaryDoc),
        tags=["Summary"],
        sub_path="/stats/",
        header_processor=GlobalHeaderProcessor(),
        timeout=timeout
    )

    return resource

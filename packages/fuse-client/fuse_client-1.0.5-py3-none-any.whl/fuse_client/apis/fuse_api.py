# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from fuse_client.models.extra_models import TokenModel  # noqa: F401
from fuse_client.models.create_asset_report_request import CreateAssetReportRequest
from fuse_client.models.create_asset_report_response import CreateAssetReportResponse
from fuse_client.models.create_link_token_request import CreateLinkTokenRequest
from fuse_client.models.create_link_token_response import CreateLinkTokenResponse
from fuse_client.models.create_session_request import CreateSessionRequest
from fuse_client.models.create_session_response import CreateSessionResponse
from fuse_client.models.delete_financial_connection_response import DeleteFinancialConnectionResponse
from fuse_client.models.exchange_financial_connections_public_token_request import ExchangeFinancialConnectionsPublicTokenRequest
from fuse_client.models.exchange_financial_connections_public_token_response import ExchangeFinancialConnectionsPublicTokenResponse
from fuse_client.models.get_asset_report_request import GetAssetReportRequest
from fuse_client.models.get_asset_report_response import GetAssetReportResponse
from fuse_client.models.get_entity_response import GetEntityResponse
from fuse_client.models.get_financial_connection_response import GetFinancialConnectionResponse
from fuse_client.models.get_financial_connections_account_details_request import GetFinancialConnectionsAccountDetailsRequest
from fuse_client.models.get_financial_connections_account_details_response import GetFinancialConnectionsAccountDetailsResponse
from fuse_client.models.get_financial_connections_accounts_request import GetFinancialConnectionsAccountsRequest
from fuse_client.models.get_financial_connections_accounts_response import GetFinancialConnectionsAccountsResponse
from fuse_client.models.get_financial_connections_balance_request import GetFinancialConnectionsBalanceRequest
from fuse_client.models.get_financial_connections_balance_response import GetFinancialConnectionsBalanceResponse
from fuse_client.models.get_financial_connections_owners_request import GetFinancialConnectionsOwnersRequest
from fuse_client.models.get_financial_connections_owners_response import GetFinancialConnectionsOwnersResponse
from fuse_client.models.get_financial_connections_transactions_request import GetFinancialConnectionsTransactionsRequest
from fuse_client.models.get_financial_connections_transactions_response import GetFinancialConnectionsTransactionsResponse
from fuse_client.models.get_financial_institution_response import GetFinancialInstitutionResponse
from fuse_client.models.get_investment_holdings_request import GetInvestmentHoldingsRequest
from fuse_client.models.get_investment_holdings_response import GetInvestmentHoldingsResponse
from fuse_client.models.get_investment_transactions_request import GetInvestmentTransactionsRequest
from fuse_client.models.get_investment_transactions_response import GetInvestmentTransactionsResponse
from fuse_client.models.get_liabilities_request import GetLiabilitiesRequest
from fuse_client.models.get_liabilities_response import GetLiabilitiesResponse
from fuse_client.models.migrate_financial_connections_token_request import MigrateFinancialConnectionsTokenRequest
from fuse_client.models.migrate_financial_connections_token_response import MigrateFinancialConnectionsTokenResponse
from fuse_client.models.refresh_asset_report_request import RefreshAssetReportRequest
from fuse_client.models.sync_financial_connections_data_response import SyncFinancialConnectionsDataResponse
from fuse_client.security_api import get_token_fuseApiKey, get_token_fuseClientId

router = APIRouter()


@router.post(
    "/v1/asset_report/create",
    responses={
        200: {"model": CreateAssetReportResponse, "description": "Response"},
    },
    tags=["Fuse"],
    response_model_by_alias=True,
)
async def create_asset_report(
    create_asset_report_request: CreateAssetReportRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> CreateAssetReportResponse:
    """Use this endpoint to generate an Asset Report for a user."""
    ...


@router.post(
    "/v1/link/token",
    responses={
        200: {"model": CreateLinkTokenResponse, "description": "Response"},
    },
    tags=["Fuse"],
    response_model_by_alias=True,
)
async def create_link_token(
    create_link_token_request: CreateLinkTokenRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> CreateLinkTokenResponse:
    """Create a link token to start the process of a user connecting to a specific financial institution."""
    ...


@router.post(
    "/v1/session",
    responses={
        200: {"model": CreateSessionResponse, "description": "Response"},
    },
    tags=["Fuse"],
    response_model_by_alias=True,
)
async def create_session(
    create_session_request: CreateSessionRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> CreateSessionResponse:
    """Creates a session that returns a client_secret which is required as a parameter when initializing the Fuse SDK."""
    ...


@router.delete(
    "/v1/financial_connections/{financial_connection_id_to_delete}",
    responses={
        200: {"model": DeleteFinancialConnectionResponse, "description": "Success"},
    },
    tags=["Fuse"],
    summary="Delete a financial connection",
    response_model_by_alias=True,
)
async def delete_financial_connection(
    financial_connection_id_to_delete: str = Path(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> DeleteFinancialConnectionResponse:
    ...


@router.post(
    "/v1/financial_connections/public_token/exchange",
    responses={
        200: {"model": ExchangeFinancialConnectionsPublicTokenResponse, "description": "Response"},
    },
    tags=["Fuse"],
    response_model_by_alias=True,
)
async def exchange_financial_connections_public_token(
    exchange_financial_connections_public_token_request: ExchangeFinancialConnectionsPublicTokenRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> ExchangeFinancialConnectionsPublicTokenResponse:
    """API to exchange a public token for an access token and financial connection id"""
    ...


@router.post(
    "/v1/asset_report",
    responses={
        200: {"model": GetAssetReportResponse, "description": "Response"},
    },
    tags=["Fuse"],
    response_model_by_alias=True,
)
async def get_asset_report(
    get_asset_report_request: GetAssetReportRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetAssetReportResponse:
    """Retrieves the Asset Report in JSON format."""
    ...


@router.get(
    "/v1/entities/{entity_id}",
    responses={
        200: {"model": GetEntityResponse, "description": "Success"},
    },
    tags=["Fuse"],
    summary="Get entity",
    response_model_by_alias=True,
)
async def get_entity(
    entity_id: str = Path(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetEntityResponse:
    """An entity is automatically created after a successful connection. The id of the entity is what is set when calling the &#39;create session&#39; endpoint"""
    ...


@router.get(
    "/v1/financial_connections/{financial_connection_id}",
    responses={
        200: {"model": GetFinancialConnectionResponse, "description": "Success"},
    },
    tags=["Fuse"],
    summary="Get financial connection details",
    response_model_by_alias=True,
)
async def get_financial_connection(
    financial_connection_id: str = Path(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetFinancialConnectionResponse:
    ...


@router.post(
    "/v1/financial_connections/accounts/details",
    responses={
        200: {"model": GetFinancialConnectionsAccountDetailsResponse, "description": "Success"},
    },
    tags=["Fuse"],
    summary="Get account details",
    response_model_by_alias=True,
)
async def get_financial_connections_account_details(
    get_financial_connections_account_details_request: GetFinancialConnectionsAccountDetailsRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetFinancialConnectionsAccountDetailsResponse:
    ...


@router.post(
    "/v1/financial_connections/accounts",
    responses={
        200: {"model": GetFinancialConnectionsAccountsResponse, "description": "Successful response"},
    },
    tags=["Fuse"],
    summary="Get accounts",
    response_model_by_alias=True,
)
async def get_financial_connections_accounts(
    get_financial_connections_accounts_request: GetFinancialConnectionsAccountsRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetFinancialConnectionsAccountsResponse:
    ...


@router.post(
    "/v1/financial_connections/balances",
    responses={
        200: {"model": GetFinancialConnectionsBalanceResponse, "description": "Successful response"},
    },
    tags=["Fuse"],
    summary="Get balances",
    response_model_by_alias=True,
)
async def get_financial_connections_balances(
    get_financial_connections_balance_request: GetFinancialConnectionsBalanceRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetFinancialConnectionsBalanceResponse:
    ...


@router.post(
    "/v1/financial_connections/owners",
    responses={
        200: {"model": GetFinancialConnectionsOwnersResponse, "description": "Success"},
    },
    tags=["Fuse"],
    summary="Get account owners",
    response_model_by_alias=True,
)
async def get_financial_connections_owners(
    get_financial_connections_owners_request: GetFinancialConnectionsOwnersRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetFinancialConnectionsOwnersResponse:
    ...


@router.post(
    "/v1/financial_connections/transactions",
    responses={
        200: {"model": GetFinancialConnectionsTransactionsResponse, "description": "Success"},
    },
    tags=["Fuse"],
    summary="Get transactions",
    response_model_by_alias=True,
)
async def get_financial_connections_transactions(
    get_financial_connections_transactions_request: GetFinancialConnectionsTransactionsRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetFinancialConnectionsTransactionsResponse:
    ...


@router.get(
    "/v1/financial_connections/institutions/{institution_id}",
    responses={
        200: {"model": GetFinancialInstitutionResponse, "description": "Financial institution metadata"},
    },
    tags=["Fuse"],
    summary="Get a financial institution",
    response_model_by_alias=True,
)
async def get_financial_institution(
    institution_id: str = Path(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetFinancialInstitutionResponse:
    """Receive metadata for a financial institution"""
    ...


@router.post(
    "/v1/financial_connections/investments/holdings",
    responses={
        200: {"model": GetInvestmentHoldingsResponse, "description": "Successful response"},
    },
    tags=["Fuse"],
    summary="Get investment holdings",
    response_model_by_alias=True,
)
async def get_investment_holdings(
    get_investment_holdings_request: GetInvestmentHoldingsRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetInvestmentHoldingsResponse:
    ...


@router.post(
    "/v1/financial_connections/investments/transactions",
    responses={
        200: {"model": GetInvestmentTransactionsResponse, "description": "Successful response"},
    },
    tags=["Fuse"],
    summary="Get investment transactions",
    response_model_by_alias=True,
)
async def get_investment_transactions(
    get_investment_transactions_request: GetInvestmentTransactionsRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetInvestmentTransactionsResponse:
    ...


@router.post(
    "/v1/financial_connections/migrate",
    responses={
        200: {"model": MigrateFinancialConnectionsTokenResponse, "description": "Success"},
    },
    tags=["Fuse"],
    summary="Migrate financial connection",
    response_model_by_alias=True,
)
async def migrate_financial_connection(
    migrate_financial_connections_token_request: MigrateFinancialConnectionsTokenRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> MigrateFinancialConnectionsTokenResponse:
    """This endpoint migrates financial connections from Plaid or MX into the unified Fuse API. It accepts a POST request with connection data, aggregator, entity, and Fuse products, and responds with a JSON payload containing the migrated connection&#39;s data, access token, ID, and request ID."""
    ...


@router.post(
    "/v1/asset_report/refresh",
    responses={
        200: {"model": CreateAssetReportResponse, "description": "Response"},
    },
    tags=["Fuse"],
    response_model_by_alias=True,
)
async def refresh_asset_report(
    refresh_asset_report_request: RefreshAssetReportRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> CreateAssetReportResponse:
    """Refreshes the Asset Report in JSON format."""
    ...


@router.post(
    "/v1/financial_connections/sync",
    responses={
        200: {"model": SyncFinancialConnectionsDataResponse, "description": "Successfully synchronized transactions"},
    },
    tags=["Fuse"],
    summary="Sync financial connections data",
    response_model_by_alias=True,
)
async def sync_financial_connections_data(
    body:  = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> SyncFinancialConnectionsDataResponse:
    """Call this endpoint upon receiving a financial_connection.sync_data webhook. This will keep the financial connections data up to date."""
    ...


@router.post(
    "/v1/financial_connections/liabilities",
    responses={
        200: {"model": GetLiabilitiesResponse, "description": "Successful response"},
    },
    tags=["Fuse"],
    summary="Get liabilities",
    response_model_by_alias=True,
)
async def v1_financial_connections_liabilities_post(
    get_liabilities_request: GetLiabilitiesRequest = Body(None, description=""),
    token_fuseApiKey: TokenModel = Security(
        get_token_fuseApiKey
    ),
    token_fuseClientId: TokenModel = Security(
        get_token_fuseClientId
    ),
) -> GetLiabilitiesResponse:
    ...

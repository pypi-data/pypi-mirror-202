import typing_extensions

from fuse_client.paths import PathValues
from fuse_client.apis.paths.v1_financial_connections_accounts_details import V1FinancialConnectionsAccountsDetails
from fuse_client.apis.paths.v1_financial_connections_owners import V1FinancialConnectionsOwners
from fuse_client.apis.paths.v1_financial_connections_accounts import V1FinancialConnectionsAccounts
from fuse_client.apis.paths.v1_asset_report_create import V1AssetReportCreate
from fuse_client.apis.paths.v1_asset_report_refresh import V1AssetReportRefresh
from fuse_client.apis.paths.v1_asset_report import V1AssetReport
from fuse_client.apis.paths.v1_financial_connections_balances import V1FinancialConnectionsBalances
from fuse_client.apis.paths.v1_entities_entity_id import V1EntitiesEntityId
from fuse_client.apis.paths.v1_financial_connections_public_token_exchange import V1FinancialConnectionsPublicTokenExchange
from fuse_client.apis.paths.v1_financial_connections_sync import V1FinancialConnectionsSync
from fuse_client.apis.paths.v1_financial_connections_institutions_institution_id import V1FinancialConnectionsInstitutionsInstitutionId
from fuse_client.apis.paths.v1_financial_connections_financial_connection_id_to_delete import V1FinancialConnectionsFinancialConnectionIdToDelete
from fuse_client.apis.paths.v1_financial_connections_financial_connection_id import V1FinancialConnectionsFinancialConnectionId
from fuse_client.apis.paths.v1_financial_connections_migrate import V1FinancialConnectionsMigrate
from fuse_client.apis.paths.v1_financial_connections_investments_holdings import V1FinancialConnectionsInvestmentsHoldings
from fuse_client.apis.paths.v1_financial_connections_investments_transactions import V1FinancialConnectionsInvestmentsTransactions
from fuse_client.apis.paths.v1_financial_connections_liabilities import V1FinancialConnectionsLiabilities
from fuse_client.apis.paths.v1_link_token import V1LinkToken
from fuse_client.apis.paths.v1_session import V1Session
from fuse_client.apis.paths.v1_financial_connections_transactions import V1FinancialConnectionsTransactions

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS_DETAILS: V1FinancialConnectionsAccountsDetails,
        PathValues.V1_FINANCIAL_CONNECTIONS_OWNERS: V1FinancialConnectionsOwners,
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS: V1FinancialConnectionsAccounts,
        PathValues.V1_ASSET_REPORT_CREATE: V1AssetReportCreate,
        PathValues.V1_ASSET_REPORT_REFRESH: V1AssetReportRefresh,
        PathValues.V1_ASSET_REPORT: V1AssetReport,
        PathValues.V1_FINANCIAL_CONNECTIONS_BALANCES: V1FinancialConnectionsBalances,
        PathValues.V1_ENTITIES_ENTITY_ID: V1EntitiesEntityId,
        PathValues.V1_FINANCIAL_CONNECTIONS_PUBLIC_TOKEN_EXCHANGE: V1FinancialConnectionsPublicTokenExchange,
        PathValues.V1_FINANCIAL_CONNECTIONS_SYNC: V1FinancialConnectionsSync,
        PathValues.V1_FINANCIAL_CONNECTIONS_INSTITUTIONS_INSTITUTION_ID: V1FinancialConnectionsInstitutionsInstitutionId,
        PathValues.V1_FINANCIAL_CONNECTIONS_FINANCIAL_CONNECTION_ID_TO_DELETE: V1FinancialConnectionsFinancialConnectionIdToDelete,
        PathValues.V1_FINANCIAL_CONNECTIONS_FINANCIAL_CONNECTION_ID: V1FinancialConnectionsFinancialConnectionId,
        PathValues.V1_FINANCIAL_CONNECTIONS_MIGRATE: V1FinancialConnectionsMigrate,
        PathValues.V1_FINANCIAL_CONNECTIONS_INVESTMENTS_HOLDINGS: V1FinancialConnectionsInvestmentsHoldings,
        PathValues.V1_FINANCIAL_CONNECTIONS_INVESTMENTS_TRANSACTIONS: V1FinancialConnectionsInvestmentsTransactions,
        PathValues.V1_FINANCIAL_CONNECTIONS_LIABILITIES: V1FinancialConnectionsLiabilities,
        PathValues.V1_LINK_TOKEN: V1LinkToken,
        PathValues.V1_SESSION: V1Session,
        PathValues.V1_FINANCIAL_CONNECTIONS_TRANSACTIONS: V1FinancialConnectionsTransactions,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS_DETAILS: V1FinancialConnectionsAccountsDetails,
        PathValues.V1_FINANCIAL_CONNECTIONS_OWNERS: V1FinancialConnectionsOwners,
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS: V1FinancialConnectionsAccounts,
        PathValues.V1_ASSET_REPORT_CREATE: V1AssetReportCreate,
        PathValues.V1_ASSET_REPORT_REFRESH: V1AssetReportRefresh,
        PathValues.V1_ASSET_REPORT: V1AssetReport,
        PathValues.V1_FINANCIAL_CONNECTIONS_BALANCES: V1FinancialConnectionsBalances,
        PathValues.V1_ENTITIES_ENTITY_ID: V1EntitiesEntityId,
        PathValues.V1_FINANCIAL_CONNECTIONS_PUBLIC_TOKEN_EXCHANGE: V1FinancialConnectionsPublicTokenExchange,
        PathValues.V1_FINANCIAL_CONNECTIONS_SYNC: V1FinancialConnectionsSync,
        PathValues.V1_FINANCIAL_CONNECTIONS_INSTITUTIONS_INSTITUTION_ID: V1FinancialConnectionsInstitutionsInstitutionId,
        PathValues.V1_FINANCIAL_CONNECTIONS_FINANCIAL_CONNECTION_ID_TO_DELETE: V1FinancialConnectionsFinancialConnectionIdToDelete,
        PathValues.V1_FINANCIAL_CONNECTIONS_FINANCIAL_CONNECTION_ID: V1FinancialConnectionsFinancialConnectionId,
        PathValues.V1_FINANCIAL_CONNECTIONS_MIGRATE: V1FinancialConnectionsMigrate,
        PathValues.V1_FINANCIAL_CONNECTIONS_INVESTMENTS_HOLDINGS: V1FinancialConnectionsInvestmentsHoldings,
        PathValues.V1_FINANCIAL_CONNECTIONS_INVESTMENTS_TRANSACTIONS: V1FinancialConnectionsInvestmentsTransactions,
        PathValues.V1_FINANCIAL_CONNECTIONS_LIABILITIES: V1FinancialConnectionsLiabilities,
        PathValues.V1_LINK_TOKEN: V1LinkToken,
        PathValues.V1_SESSION: V1Session,
        PathValues.V1_FINANCIAL_CONNECTIONS_TRANSACTIONS: V1FinancialConnectionsTransactions,
    }
)

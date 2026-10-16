# Official sources and claim mapping

Audit date: 16 October 2026. Harvard author–date format. All commercial, cost, risk, workforce and behavioral parameters are illustrative assumptions or explicit derivations. Sources verify only the claims identified below.

## G1 — Google (2006)

Get your people talking.

Official source: https://googleblog.blogspot.com/2006/08/get-your-people-talking.html

Supported use: Historical entry into hosted enterprise applications in 2006.

Access audit: VERIFIED: original official announcement retrieved; dated 28 August 2006.

## G2 — Google (n.d.-a)

Google Workspace pricing.

Official source: https://workspace.google.com/pricing.html

Supported use: Product/bundle and current plan/commitment checks only. USD 7 and 14 are scenario inputs, not verified quotes.

Access audit: VERIFIED: official pricing page retrieved. Annual-commitment standard USD 7/14 displayed, with separate promotions; five-year flat prices remain assumptions.

## G3 — Google (n.d.-b)

Google Workspace Marketplace.

Official source: https://developers.google.com/workspace/marketplace

Supported use: Third-party app distribution and integration ecosystem; no installed-base or network-effect estimate.

Access audit: VERIFIED: official Marketplace overview retrieved; third-party apps and add-on publishing documented.

## G4 — Google (n.d.-c)

Gmail API: Python quickstart.

Official source: https://developers.google.com/workspace/gmail/api/quickstart/python

Supported use: OAuth scopes, credentials and Gmail label-list API in official sample.

Access audit: VERIFIED: official developer page and official GitHub source both retrieved.

Official documentation/sample source: https://raw.githubusercontent.com/googleworkspace/python-samples/main/gmail/quickstart/quickstart.py

## G5 — Google (n.d.-d)

Admin SDK Directory API: Python quickstart.

Official source: https://developers.google.com/workspace/admin/directory/v1/quickstart/python

Supported use: Directory user-list API, OAuth scope and credential dependency.

Access audit: VERIFIED: official developer page and official GitHub source both retrieved.

Official documentation/sample source: https://raw.githubusercontent.com/googleworkspace/python-samples/main/admin_sdk/directory/quickstart.py

## G6 — Google (n.d.-e)

Google Drive API: Python quickstart.

Official source: https://developers.google.com/workspace/drive/api/quickstart/python

Supported use: Drive file metadata access through a scoped API; not proof of full-fidelity migration.

Access audit: VERIFIED: official developer page and official GitHub source both retrieved.

Official documentation/sample source: https://raw.githubusercontent.com/googleworkspace/python-samples/main/drive/quickstart/quickstart.py

## M1 — Microsoft (n.d.-a)

Exchange Server licensing overview.

Official source: https://www.microsoft.com/en-us/microsoft-365/exchange/microsoft-exchange-server-licensing-licensing-overview

Supported use: Licensing due diligence only. USD 12,000/year is an illustrative allowance, not a vendor quotation.

Access audit: PENDING: commercial page returned HTTP 403 after network restoration. SE entitlements and underlying Windows/CAL coverage need a current quote; no price or exact entitlement claim is used.

## M2 — Microsoft (n.d.-b)

New-Mailbox (ExchangePowerShell).

Official source: https://learn.microsoft.com/powershell/module/exchangepowershell/new-mailbox

Supported use: Official applicability lists both Exchange Server SE and Exchange Online; mailbox and user-account creation.

Access audit: VERIFIED: official MicrosoftDocs source retrieved; rendered Learn page not accessed.

Official documentation/sample source: https://raw.githubusercontent.com/MicrosoftDocs/office-docs-powershell/main/exchange/exchange-ps/ExchangePowerShell/New-Mailbox.md

## M3 — Microsoft (n.d.-c)

New-MigrationBatch (ExchangePowerShell).

Official source: https://learn.microsoft.com/powershell/module/exchangepowershell/new-migrationbatch

Supported use: Batched migration requests, endpoints and environment-specific parameters.

Access audit: VERIFIED: official MicrosoftDocs source retrieved; rendered Learn page not accessed.

Official documentation/sample source: https://raw.githubusercontent.com/MicrosoftDocs/office-docs-powershell/main/exchange/exchange-ps/ExchangePowerShell/New-MigrationBatch.md

## M4 — Microsoft (n.d.-d)

Exchange Online service description.

Official source: https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-service-description

Supported use: Exchange Online as the procurement comparator; current price/features not asserted.

Access audit: VERIFIED: official Learn service description retrieved. Commercial pricing page returned HTTP 403; no Exchange Online price is modeled.

## M5 — Microsoft (n.d.-e)

Exchange Server architecture.

Official source: https://learn.microsoft.com/en-us/exchange/architecture/architecture?view=exchserver-2019

Supported use: Server-side architecture and deployment responsibilities; SE applicability requires checking.

Access audit: VERIFIED: official Learn architecture page retrieved; current page applies to Subscription Edition.

## M6 — Microsoft (n.d.-f)

What is new in Exchange Server Subscription Edition (SE).

Official source: https://learn.microsoft.com/en-us/exchange/new-features/new-features?view=exchserver-2019

Supported use: Current Exchange Server/SE product context; no retirement or release-date assertion is made.

Access audit: VERIFIED: official Learn SE page retrieved; no retirement or release-date assertion used.

## Interpretation limits

The Google page displays standard annual-commitment USD 7 and USD 14 levels alongside promotions and differing features. The five-year model assumes flat prices and excludes promotional discounts. No five-year guaranteed quote was obtained.

The Microsoft commercial licensing overview returned HTTP 403. No exact licensing entitlement or price is claimed. The USD 12,000 annual allowance requires current SE, Windows/CAL and subscription/Software Assurance due diligence before procurement.

Quickstarts were inspected as documentation only. No live tenant, credentials, customer migration or API endpoint was tested. No observed vendor CAC, churn, market-share or financial dataset was used.
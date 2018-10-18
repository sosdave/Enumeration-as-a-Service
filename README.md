# Enumeration as a Service

## Description

Enumeration as a Service (eaas.py) in a script that queries the DNS server of a particular domain looking for indications that the domain may be utilizing SaaS offerings. This analysis is performed on TXT, CNAME, A and MX Records. Query results, as well as highlighted results of interest are returned to the user.

## Usage

`./eaas.py <domain.com>`

## To Do

- Add known IP address ranges for lookups for SPF records (currently reliant on DNS)
- Checking for dependencies and prompting for install if not available on current machine
- Add "Verbose Mode" to allow user to decide whether or they want detailed responses
- Summary of findings at the end of the query for easier viewing
- Add any additional SaaS offerings which may have been overlooked (There are likely _many_)

## Current Checks

#### Google
- `google-site-verification` TXT Record
- `google.com` in SPF Record
- `google.com` in MX Record
- `googlemail.com` in MX Record
- A records which have the term `GOOGLE` in the ASN Provider

#### Microsoft
- `MS` TXT record [Documentation](https://support.office.com/en-us/article/gather-the-information-you-need-to-create-office-365-dns-records-77f90d4a-dc7f-4f09-8972-c1b03ea85a67)
- CNAME Record pointing to `outlook`
- `protection.outlook.com` in SPF record
- `protection.outlook.com` in SPF Record
- A records which have the term `MICROSOFT` in the ASN Provider

##### DocuSign
- `docusign` TXT Record [Documentation](https://support.docusign.com/en/guides/org-admin-guide-domains)

#### Facebook
- `facebook-domain-verification` TXT Record [Documentation](https://developers.facebook.com/docs/sharing/domain-verification/)

#### Adobe
- `adobe-sign-verification` TXT Record [Documentation](https://helpx.adobe.com/sign/help/domain_claiming.html)
- `adobe-idp-site-verification` TXT Record [Documentation](https://helpx.adobe.com/ca/enterprise/using/verify-domain-ownership.html)

#### Atlassian
- `atlassian-domain-verification` TXT Record [Documentation](https://confluence.atlassian.com/cloud/domain-verification-873871234.html)

#### Yandex
- `yandex-verification` TXT Record [Documention]()
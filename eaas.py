#!/usr/local/bin/python3
import dns.resolver, warnings,sys
from ipwhois import IPWhois

domain = sys.argv[1]

txtrecords = {
    "docusign":"This record is used as proof of domain ownership for DocuSign product offerings. This indicates the domain likely uses DocuSign as an e-signature solution.",
    "facebook-domain-verification":"This record is used as proof of domain ownership for use in the Facebook Business Manager.",
    "google-site-verification":"This record is used as proof of ownership for Google G Suite product offerings, however it might simply be verification for Google Analytics.",
    "adobe-sign-verification":"This record is used as proof of ownership of a domain for the Adobe Sign product offering. This indicates the domain likely uses Adobe Sign as an e-signature solution.",
    "atlassian-domain-verification":"This record verifies domain ownership with Atlassian. This indicates the domain might be sending managed emails from an Atlassian property and likely utilizes Atalassian product offerings such as Jira of Confluence.",
    "MS":"This record is used as proof of domain ownership by the Microsoft Office 365 product offering. This indicates a probable usage of at least some Office 365 products.",
    "adobe-idp-site-verification":"This record is used as proof of ownership for use in the Adobe Enterprise Products product offerings.",
    "yandex-verification":"This record is used as proof of ownership of a domain for Yandex. This indicates a probable usage of the Yandex Webmaster Tools.",
    "_amazonses":"Amazon Simple Email Services",
    "logmein-verification-code":"This record is used as proof of ownership for a domain for LogMeIn services. The presence of this record indicates the owner of the domain is likely using LogMeIn for remote troubleshooting.",
    "citrix-verification-code":"This record indicates the domain might be associated with utilizing Citrix Services.",
    "pardot":"This record indicates the domain might be utilizing Pardot B2B Marketing tools from Salesforce.com.",
    "zuora":"This record indicates the domain might be utilizing Zuora subscription management software."
}

cnamerecords = {
    "autodiscover.":"This domain appears to be outsourcing Microsoft Exchange.",
    "lyncdiscover.":"This domain appears to be outsourcing Microsoft Lync.",
    "sip.":"This domain appears to be outsourcing Microsoft SIP Services.",
    "enterpriseregistration.":"This domain appears to be outsourcing Mobile Device Management (MDM) services.",
    "enterpriseenrollment.":"This domain appears to be outsourcing Mobile Device Management (MDM) services.",
    "adfs.":"Active Directory Federated Services",
    "sts.":"Security Token Service"
}

asnproviders = {
    "MICROSOFT":"Microsoft Corporation",
    "GOOGLE":"Google (Alphabet) Corporation",
    "AirWatch LLC":"AirWatch Mobile Device Management"
}

cnameproviders = {
    "outlook":"Microsoft Office 365 (Managed Exchange)",
    "awmdm.com":"Airwatch Mobile Device Management (MDM)",
    "lync.com":"Microsoft Hosted Lync"
}

spfrecords = {
    "_spf.salesforce.com":"Domain is allowing emails to be sent from Salesforce.com. This indicates a high liklihood of subscription to Salesforce services.",
    "_spf.google.com":"Domain is allowing emails to be sent from Google.com. This indicates the domain may utilize Gmail or other G-Suite product offerings.",
    "protection.outlook.com":"Domain is allowing emails to be sent from Microsoft.com. This strongly indicates the domain is utilzing Microsoft Hosted Exchange.",
    "service-now.com":"Domain is allowing emails to be sent from service-now.com. This strongly indicates the domain is using the Service Now helpdesk platform.",
    "mailsenders.netsuite.com":"Domain is allowing emails to be sent from NetSuite. This strongly indicates the domain is using NetSuite product offerings (ERP / Cloud Accounting).",
    "mktomail.com":"Domain is allowing emails to be sent from Marketo. This strongly indicates the domain is using the Marketo Marketing and Lead Generation platform.",
    "spf.mandrillapp.com":"Domain is allowing emails to be sent from Mandrill (MailChimp). This strongly indicates the domain is using the Mandrill product offering for transactional email.",
    "pphosted.com":"Domain is allowing emails to be sent from Proof Point. This strongly indicates the domain is utilizing Proof Point Managed email services.",
    "zendesk.com":"Domain is allowing emails to be sent from Zendesk. This strongly indicates the domain is utilizing Zendesk for help desk and ticketing purposes.",
    "mcsv.net":"Domain is allowing emails to be sent from MailChimp. This strongly indicates the domain is utilizing MailChimp for email marketing.",
    "freshdesk.com":"Domain is allowing emails to be sent from Freshdesk. This strongly indicates the domain is utilizing FreshDesk for helpdesk and ticketing services."
}

mxrecords = {
    "google.com":"Google server as an email server.\n    └── [*] This strongly indicates the domain is utilizing Google as an email server.",
    "googlemail.com":"Google server as an email server.\n    └── [*] This strongly indicates the domain is utilizing Google as an email server.",
    "pphosted.com":"Proof Point server as an email server.\n    └── [*] This strongly indicates that Proof Point Managed Email Hosting is being used.",
    "zoho.com":"ZOHO server as an email server.\n    └── [*] This strongly indicates that ZOHO is being utilized for email services.",
    "protection.outlook.com":"Microsoft server as an email server.\n    └── [*] This strongly indicates the domain is utilzing Microsoft Hosted Exchange."
}

misctxt = {
    "pardot":"Pardot Business-to-Business Marketing by Salesforce"
}

def displayhelp():
    print("EaaS - Enumeration as a Service.")
    print("Usage : ./eaas.py [domain]")

# Function to query TXT DNS entries
def querytxt():
    print("\n")
    print("[*] Querying TXT DNS entries.")
    print("=========================================================")
    answers = dns.resolver.query(domain,"TXT")
    for rdata in answers:
        # Examine various TXT based records for the domain
        for key, value in txtrecords.items():
            if key in rdata.to_text():
                print("[INFO] \033[33m\"{}\"\033[0;0m Record Found.".format(key))
                print("    └── \033[32m[+]\033[0;0m {}".format(value))
        # Examine SPF records for the domain
        for spfkey, spfvalue in spfrecords.items():
            if spfkey in rdata.to_text():
                print("[INFO] \033[33m\"{}\"\033[0;0m SPF Record found.\n    └── \033[32m[+]\033[0;0m {}".format(spfkey,spfvalue))

# Function to query and examine CNAME records for the chosen domain
def querycname():
    print("\n")
    print("[*] Querying CNAME DNS entries.")
    print("=========================================================")
    for key, value in cnamerecords.items():
        lookup = key + domain
        try:
            answers = dns.resolver.query(lookup, 'CNAME')
            for rdata in answers:
                print("[INFO] \033[33m\"{}\"\033[0;0m CNAME record found.".format(key[:-1]))
                print("    └── [INFO] CNAME record points to \033[33m{}\033[0;0m".format(rdata.target))
                for cnamekey, cnamevalue in cnameproviders.items():
                    if cnamekey in rdata.target.to_text():
                        print("    └── \033[32m[+]\033[0;0m Domain appears to be outsourcing services to \033[33m{}\033[0;0m.".format(cnamevalue))
        except:
            pass

# Function to query and exmaine A records for the chosen domain.
def queryarecords():
    print("\n")
    print("[*] Querying A record DNS entries.")
    print("=========================================================")
    for key, value in cnamerecords.items():
        lookup = key + domain
        try:
            answers = dns.resolver.query(lookup, 'A')
            for rdata in answers:
                print("[INFO] \033[33m\"{}\"\033[0;0m Record Found resolving to \033[33m{}\033[0;0m.".format(key[:-1],rdata.address))
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UserWarning)
                    obj = IPWhois(str(rdata.address))
                    results = obj.lookup_rdap()
                    print("    └── [INFO] IP Address resolves to an ASN owned by \033[33m{}\033[0;0m".format(results['asn_description']))
                    for asnkey, asnvalue in asnproviders.items():
                        if asnkey in format(results['asn_description']):
                            print("    └── \033[32m[+]\033[0;0m {} Services appear to be provided by \033[33m{}\033[0;0m.".format(value,asnvalue))
        except:
            pass

# Function to query and examine the MX records for the chosen domain.
def querymxrecords():
    print("\n")
    print("[*] Querying MX record DNS entries.")
    print("=========================================================")
    try:
        answers = dns.resolver.query(domain, 'MX')
        for rdata in answers:
            print("[INFO] MX Record : \033[33m{}\033[0;0m".format(rdata.exchange))
            for mxkey, mxvalue in mxrecords.items():
                if mxkey in rdata.exchange.to_text():
                    print("    └── \033[32m[+]\033[0;0m : This MX Record indicates a strong probability that the domain is using a {} for hosted email solutions, however it might just be using the MX for mail filtering.".format(mxvalue))
    except:
        pass

if __name__ == "__main__":
    if len(sys.argv) == 1:
        displayhelp()
        sys.exit()
    else:
        print("[*] EaaS - Enumeration as a Service script started.")
        print("[*] Performing queries on domain \033[33m{}\033[0;0m".format(domain))
        querytxt()
        querycname()
        queryarecords()
        querymxrecords()
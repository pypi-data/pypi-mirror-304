var store = [{
        "title": "DEFCON31 - ELF 64-bit Stack Based Buffer Overflow",
        "excerpt":"DEFCON 31 - ELF 64-bit Stack Based Buffer Overflow I recently had the pleasure of attending DEFCON31 at Caesars Forum in Las Vegas. A few of us on the Red Team decided to participate in one of the many CTFs being held there, Operation Cybershock CTF brought to you by...","categories": ["research"],
        "tags": [],
        "url": "/research/2023-09-05-defcon31-hackthebox-ctf/",
        "teaser": null
      },{
        "title": "Defeating MFA Number Challenges through Phishing",
        "excerpt":"Defeating MFA “Number Challenges” through Phishing Push verifications with an extra “number challenge” step have become a popular multi-factor authentication strategy. But, does this extra step actually offer any added protection against hackers? Push verifications are a preferred multi-factor authentication choice for many organizations. They offer convenience and greater security...","categories": ["research"],
        "tags": [],
        "url": "/research/2023-09-06-defeating-mfa-number-challenges/",
        "teaser": null
      },{
        "title": "Thinking About CVE-2023-21967, an OpenJDK Vulnerability",
        "excerpt":"Security professionals are inundated with CVEs; the National Vulnerability Database reports receiving over 2,466 to analyze in August 2023 alone.1 It remains an important skill to triage and remediate vulnerabilities most important to your products and environment. Part of this involves technically analyzing publicly available vulnerability data to make an...","categories": ["research"],
        "tags": [],
        "url": "/research/2023-10-06-openjdk-vuln-reproduction-CVE-2023-21967/",
        "teaser": null
      },{
        "title": "Practical Jazzer for the Snazzy Fuzzer",
        "excerpt":"Fuzzing is an automated methodology that attempts to identify bugs within software, especially security vulnerabilities. We on the Security Research Team at ServiceNow utilize the fuzzer Jazzer internally for specific use cases. Jazzer is a coverage-guided, in-process fuzzer for the JVM platform developed by Code Intelligence. It is based on...","categories": ["research"],
        "tags": [],
        "url": "/research/2024-07-09-jazzer-practical-tips/",
        "teaser": null
      },{
        "title": "A Rhino of a Problem - Assembling Call Stacks for Rhino Polyglot Code",
        "excerpt":"Complex systems involving polyglot programming introduce unique issues for security professionals because of the interactions between different languages. To better understand such a system and its security mechanisms, it is often required for security professionals to trace call flows through the language boundaries of polyglot code. Unfortunately, the language boundaries...","categories": ["research"],
        "tags": [],
        "url": "/research/2024-07-29-a-rhino-of-a-problem/",
        "teaser": null
      },{
        "title": "SootUp vs. Soot - Is The New Static Analysis Library Ready For Use?",
        "excerpt":"Soot,1 a tool for statically analyzing Java code, has recently been supplanted by SootUp.2 SootUp is marketed as the next generation of Soot and developed by the same authors as Soot. But how exactly is SootUp different from Soot? Do the major capabilities of Soot still exist in SootUp? How...","categories": ["research"],
        "tags": [],
        "url": "/research/2024-08-07-sootup-vs-soot/",
        "teaser": null
      },{
        "title": "SNulk - ServiceNow Bulk Submit Tool for Table Records",
        "excerpt":"Have you ever needed to automate the creation of a large number of similar records in a ServiceNow table? Do you wish you could easily cherry pick data from the rows in a Excel spreadsheet or Pandas Dataframe and transform the data into new ServiceNow table records? SNulk, the ServiceNow...","categories": ["research"],
        "tags": [],
        "url": "/research/2024-10-31-snulk/",
        "teaser": null
      },{
        "title": "CVE-2022-39048",
        "excerpt":"PUBLISHED Summary Cross-Site Scripting (XSS) vulnerability in ServiceNow UI page assessment_redirect Description A XSS vulnerability was identified in the ServiceNow UI page assessment_redirect. To exploit this vulnerability, an attacker would need to persuade an authenticated user to click a maliciously crafted URL. Successful exploitation potentially could be used to conduct...","categories": [],
        "tags": [],
        "url": "/snadvisories/2023-04-10-CVE-2022-39048/",
        "teaser": null
      },{
        "title": "CVE-2022-46886",
        "excerpt":"PUBLISHED Summary There exists an open redirect within the response list update functionality of ServiceNow. This allows attackers to redirect users to arbitrary domains when clicking on a URL within a service-now domain. Description There exists an open redirect within the response list update functionality of ServiceNow. This allows attackers...","categories": [],
        "tags": [],
        "url": "/snadvisories/2023-04-14-CVE-2022-46886/",
        "teaser": null
      },{
        "title": "CVE-2022-46389",
        "excerpt":"PUBLISHED Summary Cross-Site Scripting (XSS) vulnerability found on logout functionality Description There exists a reflected XSS within the logout functionality of ServiceNow versions lower than Quebec Patch 10 Hotfix 11b, Rome Patch 10 Hotfix 3b, San Diego Patch 9, Tokyo Patch 4, and Utah GA. This enables an unauthenticated remote...","categories": [],
        "tags": [],
        "url": "/snadvisories/2023-04-17-CVE-2022-46389/",
        "teaser": null
      },{
        "title": "CVE-2023-1209",
        "excerpt":"PUBLISHED Summary Cross-Site Scripting (XSS) vulnerabilities exist in ServiceNow records allowing an authenticated attacker to inject arbitrary scripts. Description Cross-Site Scripting (XSS) vulnerabilities exist in ServiceNow records allowing an authenticated attacker to inject arbitrary scripts. Severity 4.3 (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N) Affected Versions This vulnerability is present in the following Affected Product(s) listed...","categories": [],
        "tags": [],
        "url": "/snadvisories/2023-05-23-CVE-2023-1209/",
        "teaser": null
      },{
        "title": "CVE-2022-43684",
        "excerpt":"PUBLISHED Summary ACL bypass in Reporting functionality Description ServiceNow has released patches and an upgrade that address an Access Control List (ACL) bypass issue in ServiceNow Core functionality. Additional Details This issue is present in the following supported ServiceNow releases: Quebec prior to Patch 10 Hot Fix 8b Rome prior...","categories": [],
        "tags": [],
        "url": "/snadvisories/2023-06-13-CVE-2022-43684/",
        "teaser": null
      },{
        "title": "CVE-2023-1298",
        "excerpt":"PUBLISHED Summary ServiceNow has released upgrades and patches that address a Reflected Cross-Site scripting (XSS) vulnerability that was identified in the ServiceNow Polaris Layout. This vulnerability would enable an authenticated user to inject arbitrary scripts. Description ServiceNow has released upgrades and patches that address a Reflected Cross-Site scripting (XSS) vulnerability...","categories": [],
        "tags": [],
        "url": "/snadvisories/2023-07-06-CVE-2023-1298/",
        "teaser": null
      },{
        "title": "CVE-2023-3414",
        "excerpt":"PUBLISHED Summary Cross-Site Request Forgery (CSRF) in Jenkins Plug-in for ServiceNow DevOps Description A cross-site request forgery vulnerability exists in versions of the Jenkins Plug-in for ServiceNow DevOps prior to 1.38.1 that, if exploited successfully, could cause the unwanted exposure of sensitive information. To address this issue, apply the 1.38.1 version...","categories": [],
        "tags": [],
        "url": "/snadvisories/2023-07-26-CVE-2023-3414/",
        "teaser": null
      },{
        "title": "CVE-2023-3442",
        "excerpt":"PUBLISHED Summary Missing Authorization in Jenkins plug-in for ServiceNow DevOps Description A missing authorization vulnerability exists in versions of the Jenkins Plug-in for ServiceNow DevOps prior to 1.38.1 that, if exploited successfully, could cause the unwanted exposure of sensitive information. To address this issue, apply the 1.38.1 version of the Jenkins...","categories": [],
        "tags": [],
        "url": "/snadvisories/2023-07-26-CVE-2023-3442/",
        "teaser": null
      },]

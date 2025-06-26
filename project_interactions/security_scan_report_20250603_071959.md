# Security Scan Report

**Scan Time:** 2025-06-03 07:19:59  
**Files Scanned:** 4  
**Total Vulnerabilities:** 17

## Summary by Severity

| Severity | Count |
|----------|-------|
| CRITICAL | 4 |
| HIGH | 12 |
| MEDIUM | 1 |
| LOW | 0 |
| INFO | 0 |

## Compliance Status

| Standard | Status |
|----------|--------|
| OWASP | ❌ Non-compliant |
| PCI-DSS | ❌ Non-compliant |
| HIPAA | ❌ Non-compliant |

## Detailed Findings

### Command Injection

**File:** `/tmp/tmp89jn4k5x/app.py`  
**Line:** 21  
**Severity:** CRITICAL  
**Confidence:** 90%  
**CWE:** CWE-78  

**Code:**
```
subprocess.run("echo " + filename, shell=True)
```

**Remediation:** Use subprocess with shell=False and validate input

---

### Hardcoded Secret

**File:** `/tmp/tmp89jn4k5x/app.py`  
**Line:** 9  
**Severity:** CRITICAL  
**Confidence:** 95%  
**CWE:** CWE-798  

**Code:**
```
DB_PASSWORD = "****"
```

**Remediation:** Use environment variables or secure key management

---

### Hardcoded Secret

**File:** `/tmp/tmp89jn4k5x/app.py`  
**Line:** 10  
**Severity:** CRITICAL  
**Confidence:** 95%  
**CWE:** CWE-798  

**Code:**
```
AWS_ACCESS_KEY_ID = "****"
```

**Remediation:** Use environment variables or secure key management

---

### Command Injection

**File:** `/tmp/tmp89jn4k5x/app.py`  
**Line:** 34  
**Severity:** CRITICAL  
**Confidence:** 100%  
**CWE:** CWE-95  

**Code:**
```
return eval(expression)
```

**Remediation:** Avoid eval/exec or use ast.literal_eval for safe evaluation

---

### Path Traversal

**File:** `/tmp/tmp89jn4k5x/app.py`  
**Line:** 29  
**Severity:** HIGH  
**Confidence:** 60%  
**CWE:** CWE-22  

**Code:**
```
with open(f"uploads/{user_path}", 'r') as f:
```

**Remediation:** Validate and sanitize file paths

---

### Cross Site Scripting

**File:** `/tmp/tmp89jn4k5x/frontend.js`  
**Line:** 8  
**Severity:** HIGH  
**Confidence:** 70%  
**CWE:** CWE-79  

**Code:**
```
document.write('<div class="message">' + msg + '</div>');
```

**Remediation:** Sanitize user input and use textContent instead of innerHTML

---

### Cross Site Scripting

**File:** `/tmp/tmp89jn4k5x/frontend.js`  
**Line:** 17  
**Severity:** HIGH  
**Confidence:** 70%  
**CWE:** CWE-79  

**Code:**
```
eval(code);
```

**Remediation:** Sanitize user input and use textContent instead of innerHTML

---

### Injection

**File:** `/tmp/tmp89jn4k5x/app.py`  
**Line:** 14  
**Severity:** HIGH  
**Confidence:** 80%  
**CWE:** CWE-89  

**Code:**
```
query = f"SELECT * FROM users WHERE id = {user_id}"
```

**Remediation:** Use parameterized queries or ORM

---

### Xml External Entities

**File:** `/tmp/tmp89jn4k5x/XmlParser.java`  
**Line:** 2  
**Severity:** HIGH  
**Confidence:** 90%  
**CWE:** CWE-611  

**Code:**
```
import javax.xml.parsers.DocumentBuilderFactory;
```

**Remediation:** Disable external entity processing in XML parser

---

### Xml External Entities

**File:** `/tmp/tmp89jn4k5x/XmlParser.java`  
**Line:** 9  
**Severity:** HIGH  
**Confidence:** 90%  
**CWE:** CWE-611  

**Code:**
```
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
```

**Remediation:** Disable external entity processing in XML parser

---

### Using Components With Known Vulnerabilities

**File:** `/tmp/tmp89jn4k5x/package.json`  
**Line:** 1  
**Severity:** HIGH  
**Confidence:** 90%  
**CVE:** CVE-2020-8203  

**Code:**
```
lodash: 4.17.15
```

**Remediation:** Update lodash to version >= 4.17.19

---

### Using Components With Known Vulnerabilities

**File:** `/tmp/tmp89jn4k5x/package.json`  
**Line:** 1  
**Severity:** HIGH  
**Confidence:** 90%  
**CVE:** CVE-2020-7598  

**Code:**
```
minimist: 1.2.0
```

**Remediation:** Update minimist to version >= 1.2.5

---

### Using Components With Known Vulnerabilities

**File:** `/tmp/tmp89jn4k5x/requirements.txt`  
**Line:** 1  
**Severity:** HIGH  
**Confidence:** 100%  
**CVE:** CVE-2019-19844  

**Code:**
```
django<2.2
```

**Remediation:** Update django to latest version

---

### Using Components With Known Vulnerabilities

**File:** `/tmp/tmp89jn4k5x/requirements.txt`  
**Line:** 1  
**Severity:** HIGH  
**Confidence:** 100%  
**CVE:** CVE-2018-1000656  

**Code:**
```
flask<0.12.3
```

**Remediation:** Update flask to latest version

---

### Using Components With Known Vulnerabilities

**File:** `/tmp/tmp89jn4k5x/requirements.txt`  
**Line:** 1  
**Severity:** HIGH  
**Confidence:** 100%  
**CVE:** CVE-2018-18074  

**Code:**
```
requests<2.20.0
```

**Remediation:** Update requests to latest version

---

### Using Components With Known Vulnerabilities

**File:** `/tmp/tmp89jn4k5x/requirements.txt`  
**Line:** 1  
**Severity:** HIGH  
**Confidence:** 100%  
**CVE:** CVE-2020-14343  

**Code:**
```
pyyaml<5.4
```

**Remediation:** Update pyyaml to latest version

---

### Weak Cryptography

**File:** `/tmp/tmp89jn4k5x/app.py`  
**Line:** 25  
**Severity:** MEDIUM  
**Confidence:** 90%  
**CWE:** CWE-327  

**Code:**
```
return hashlib.md5(password.encode()).hexdigest()
```

**Remediation:** Use stronger algorithms like SHA-256 or AES

---


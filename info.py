import socket
import requests
import whois

print("Example: google.com")
domain = input("Enter a Domain Name: ")
print("\n\n")

# Find IP
def getIP(domain):
    try:
        ip = socket.gethostbyname(domain)
        print("| IP Address:", ip)
    except socket.gaierror as e:
        print("IP not Found:", e)

# Get HTTP headers
def getHTTPHeaders(domain):
    try:
        r = requests.get("http://" + domain)  
        if r.status_code == 200: 
            print("| HTTP Headers:")
            for header, value in r.headers.items():
               print("|  - {}: {}".format(header, value))
    except Exception as e:
        print("HTTP Headers not Found:", e)

# Get WHOIS Info
def getWHOISInfo(domain):
    try:
        whois_result = ""
        py = whois.whois(domain)
        
        whois_result += "| Name: {}\n".format(py.name)
        whois_result += "| Registrar: {}\n".format(py.registrar)
        whois_result += "| Creation Date: {}\n".format(py.creation_date)
        whois_result += "| Expiry Date: {}\n".format(py.expiration_date)
        whois_result += "| Country: {}\n".format(py.country)
        whois_result += "| Registrant: {}\n".format(py.registrant)
        whois_result += "| Registrant Country: {}\n".format(py.registrant_country)
        print(whois_result)
       
    except Exception as e:
       print("WHOIS not found:", e)

# Port scan 
def portScan(domain):
    try:
        ip = socket.gethostbyname(domain)
        open_ports = []

        top_ports = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3389]  
        for port in top_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            # Returns an error indicator
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            s.close()

        if open_ports:
            print("| Open ports:" , open_ports)
        else:
            print("| No open ports found.")

    except socket.gaierror as e:
        print("Error resolving domain:", e)
    except KeyboardInterrupt:
        print("\nExiting Program !!!")
    except socket.error:
        print("\nServer not responding !!!")

# find robot.txt 
def find_robottxt(domain):
    url=f"http://{domain}/robots.txt"
    try:
        r=requests.get(url)
        if r.status_code==200:
            print("Robots.txt found: " + r.text)
        else:
            print("Robots.txt not found.")    
    except Exception as e:
        print("Error fetching robots.txt:", e)

# finding CMS 
def findCMS(domain):
    try:
        r = requests.get("http://" + domain)  
        if r.status_code == 200:
            html_content = r.text
            if 'wp-content' in html_content:
                print("WordPress detected.")
            elif 'Joomla' in html_content:
                print("Joomla detected.")
            elif 'Drupal' in html_content:
                print("Drupal detected.")
            elif 'Magento' in html_content:
                print("Magento detected.")
            elif 'Shopify' in html_content:
                print("Shopify detected.")
            elif 'Squarespace' in html_content:
                print("Squarespace detected.")
            elif 'Wix' in html_content:
                print("Wix detected.")
            elif 'Blogger' in html_content:
                print("Blogger detected.")
            elif 'TYPO3' in html_content:
                print("TYPO3 detected.")
            elif 'PrestaShop' in html_content:
                print("PrestaShop detected.")
            else:
                print("CMS not detected.")
        else:
            print("Error: Unable to fetch website content.")
    except Exception as e:
         print("Error: Unable to fetch website content", e)
 
#finding subdomains     
def findSubdomains(domain, wordlist, outputfile):
    try:    
        foundsubs = []
        with open(wordlist, 'r') as file:
            subdomains_to_check = [line.strip() for line in file]

        with open(outputfile, 'w') as out_file:  # Open the output file for writing
            for subdomain in subdomains_to_check:
                url = f"http://{subdomain}.{domain}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        print(url)
                        out_file.write(url + '\n')  # Write to the output file
                        foundsubs.append(url)            
                except requests.ConnectionError:
                    continue
    except Exception as e:
        print("Unable to Resolve Subdomains:", e)          

#finding Vulnerablity
def checkVulnearblity(urls_file):
    def check_xss(url):
        payload = "<script>alert('XSS')</script>"
        response = requests.get(url, params={"input": payload})
        if payload in response.text:
            print(f"XSS vulnerability found in URL: {url}")
        else:
            print(f"No XSS vulnerability found in URL: {url}")

    print("Subdomain Enumeration is starting...")

    
    with open(urls_file, 'r') as file:
        for url in file:
            url = url.strip()  
            print(f"Checking URL: {url}")
            check_xss(url)


print("[+] Finding IP...")
getIP(domain)
print("IP Address Found. \n\n")

print("[+] Finding HTTP Headers...")
getHTTPHeaders(domain)  
print("HTTP Headers Found. \n\n")

print("[+] Finding Whois Info... ")
getWHOISInfo(domain)
print("WHOIS Found. \n\n")

print("[+] Content Management System(CMS)...")
findCMS(domain)
print("Process Completed \n\n")

print("[+] Finding Port Scan...")
print("Port scanning is starting...")
portScan(domain)
print("Port scanning is complete. \n\n")

print("[+] Finding Robots.txt...")
find_robottxt(domain)
print("Process Completed \n\n")

print("[+] Finding Subdomains...")
print("Subdomain Enumeration is starting...")
wordlist="wordlist.txt"
subdomains="subdomains.txt"
findSubdomains(domain,wordlist,subdomains)
print("Process Completed \n\n")

print("[+] Checking Vulnerablity...")
checkVulnearblity(subdomains)
print("\n")
print("Web Enumeration is complete.\n")
print("Happy Hacking :) \n")
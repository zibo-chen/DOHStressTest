from concurrent import futures
import requests
import base64

doh_url = "https://dns.alidns.com/dns-query" #你的doh地址
rr = "A"
max_workers = 320 #最大线程数

def search_doh_dns(domain):
    import dns.message
    message = dns.message.make_query(domain, rr)
    dns_req = base64.b64encode(message.to_wire()).decode("UTF8").rstrip("=")
    r = requests.get(doh_url + "?dns=" + dns_req,
                     headers={"Content-type": "application/dns-message"})

    dns_ip = []
    for answer in dns.message.from_wire(r.content).answer:
        dns = answer.to_text().split()
        dns_ip.append(dns[4])
    print(domain,dns_ip)


if __name__ == '__main__':
    with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in open('accelerated-domains.china.conf.txt'):
            domain = i[8:-17]
            executor.submit(search_doh_dns, domain)


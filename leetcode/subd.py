from collections import defaultdict
from typing import List


def subdomainVisits(cpdomains: List[str]) -> List[str]:
    dom_to_frq = defaultdict(int)
    for line in cpdomains:
        num, domain = line.split(" ")
        num = int(num)
        # find dots
        start = 0
        while start < len(domain):
            start = domain.find(".", start)
            if start == -1:
                break
            dom_to_frq[domain[start+1:]] += num
            start += 1
        dom_to_frq[domain] += num
    return [f"{v} {k}" for k, v in dom_to_frq.items()]



i = ["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"]
o = subdomainVisits(i)
#print(o)

def repeatedNTime(A):
    pass

a = [5,1,5,2,5,3,5,4]
print(repeatedNTime(a))

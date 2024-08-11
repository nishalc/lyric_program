import requests

def main():
    proxies_all = open("proxies_all.txt", "r").read().strip().split("\n")
    proxies_good = []
    unchecked = set(proxies_all) # limited to 10 to avoid too many requests 
    working = set() 
    not_working = set() 

    def reset_proxy(proxy): 
        unchecked.add(proxy) 
        working.discard(proxy) 
        not_working.discard(proxy) 

    def set_working(proxy): 
        unchecked.discard(proxy) 
        working.add(proxy) 
        not_working.discard(proxy) 

    def set_not_working(proxy): 
        unchecked.discard(proxy) 
        working.discard(proxy) 
        not_working.add(proxy)

    def test_proxy(proxy):
        try: 
            # Send proxy requests to the final URL 
            response = requests.get("http://ident.me/", proxies={'http': f"http://{proxy}"}, timeout=30) 
            if response.status_code in [200, 301, 302, 307, 404]: 
                set_working(proxy)
                print(proxy, "good")
            else: 
                set_not_working(proxy)
                print("bad") 
        except Exception as e: 
            set_not_working(proxy)
            print(e)
            print("bad")

    for ip in list(unchecked):
        test_proxy(ip)

    print(f"Of {len(proxies_all)} checked, {len(working)} are good")
    with open("proxies_good.txt", "w") as f:  # dump data in text file
        for good_ip in list(working):
            f.write(good_ip)
            f.write("\n")

if __name__=="__main__":
    main()



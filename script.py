import requests
import re
import sys

def get_m3u8_link():
    session = requests.Session()
    
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    url_main = "https://www.adintrend.tv/hd/ch39?t=live"
    headers["referer"] = "https://www.adintrend.tv/hd/ch1?t=live"
    
    try:
        print("[*] Đang truy cập trang chính...")
        res_main = session.get(url_main, headers=headers, timeout=15)
        res_main.raise_for_status()
    except Exception as e:
        print(f"[!] Lỗi khi truy cập trang chính: {e}")
        sys.exit(1)

    # BƯỚC 1: Trích xuất tham số từ Javascript thay vì từ thẻ iframe
    try:
        cxid = re.search(r'cxid=([a-zA-Z0-9]+)', res_main.text).group(1)
        tmpx = re.search(r'tmpx=([0-9\.]+)', res_main.text).group(1)
        dtime = re.search(r'dtime=([^"&]+)', res_main.text).group(1)
        
        # Lắp ráp lại URL iframe theo đúng format của web
        iframe_url = f"https://www.adintrend.tv/hd/live/i.php?ch=39&cxid={cxid}&testx=&tmpx={tmpx}&ccc=VN&device=desktop&dtime={dtime}&platform=Win32&touch=0"
        print(f"[*] Đã lắp ráp link iframe thành công: {iframe_url}")
        
    except AttributeError:
        print("[!] Không tìm thấy tham số JS. Có thể web đã đổi cấu trúc hoặc chặn IP.")
        sys.exit(1)

    # BƯỚC 2: Truy cập link iframe để lấy link .m3u8
    headers["referer"] = url_main
    headers["sec-fetch-dest"] = "iframe"
    
    try:
        print("[*] Đang truy cập iframe...")
        res_iframe = session.get(iframe_url, headers=headers, timeout=15)
        res_iframe.raise_for_status()
    except Exception as e:
        print(f"[!] Lỗi khi truy cập iframe: {e}")
        sys.exit(1)

    # Tìm link m3u8
    m3u8_match = re.search(r'src:\s*["\']([^"\']+\.m3u8[^"\']*)["\']', res_iframe.text)
    
    if not m3u8_match:
        print("[!] Không tìm thấy link .m3u8 trong iframe.")
        sys.exit(1)
        
    m3u8_url = m3u8_match.group(1)
    print("\n[+] THÀNH CÔNG! Link M3U8 của bạn là:")
    print("-" * 50)
    print(m3u8_url)
    print("-" * 50)
    
    with open("stream_link.txt", "w", encoding="utf-8") as f:
        f.write(m3u8_url)

if __name__ == "__main__":
    get_m3u8_link()

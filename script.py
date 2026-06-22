import requests
import re
import sys

def get_m3u8_link():
    # Sử dụng Session để giữ kết nối và cookies (nếu có)
    session = requests.Session()
    
    # Headers giả lập trình duyệt dựa trên curl của bạn
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1"
    }

    # BƯỚC 1: Lấy nội dung trang chính để tìm link iframe
    url_main = "https://www.adintrend.tv/hd/ch39?t=live"
    headers["Referer"] = "https://www.adintrend.tv/hd/ch1?t=live"
    
    try:
        print("[*] Đang truy cập trang chính...")
        res_main = session.get(url_main, headers=headers, timeout=10)
        res_main.raise_for_status()
    except Exception as e:
        print(f"[!] Lỗi khi truy cập trang chính: {e}")
        sys.exit(1)

    # Tìm URL của iframe (chứa i.php)
    # Tìm chuỗi có dạng: src="https://www.adintrend.tv/hd/live/i.php?..."
    iframe_match = re.search(r'<iframe[^>]*src="([^"]+i\.php[^"]+)"', res_main.text)
    
    if not iframe_match:
        print("[!] Không tìm thấy thẻ iframe trong mã nguồn.")
        sys.exit(1)
        
    # Thay thế &amp; thành & để tạo thành URL hợp lệ
    iframe_url = iframe_match.group(1).replace("&amp;", "&")
    print(f"[*] Đã lấy được link iframe: {iframe_url}")

    # BƯỚC 2: Truy cập link iframe để lấy link .m3u8
    headers["Referer"] = url_main
    headers["Sec-Fetch-Dest"] = "iframe"
    
    try:
        print("[*] Đang truy cập iframe...")
        res_iframe = session.get(iframe_url, headers=headers, timeout=10)
        res_iframe.raise_for_status()
    except Exception as e:
        print(f"[!] Lỗi khi truy cập iframe: {e}")
        sys.exit(1)

    # Tìm link m3u8 trong đoạn mã JavaScript của videojs
    # Tìm chuỗi có dạng: src: "https://...m3u8..."
    m3u8_match = re.search(r'src:\s*"([^"]+\.m3u8[^"]*)"', res_iframe.text)
    
    if not m3u8_match:
        print("[!] Không tìm thấy link .m3u8 trong nội dung iframe.")
        sys.exit(1)
        
    m3u8_url = m3u8_match.group(1)
    print("\n[+] THÀNH CÔNG! Link M3U8 của bạn là:")
    print("-" * 50)
    print(m3u8_url)
    print("-" * 50)
    
    # Bạn có thể lưu link này vào một file txt để các bước sau của Github Actions sử dụng
    with open("stream_link.txt", "w", encoding="utf-8") as f:
        f.write(m3u8_url)

if __name__ == "__main__":
    get_m3u8_link()

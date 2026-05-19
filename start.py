#!/usr/bin/env python3
"""
페이스 디비디비딥 로컬 실행 스크립트
- assets/ 이미지가 없으면 컬러 플레이스홀더를 자동 생성합니다
- http://localhost:8080 에서 게임을 실행합니다
"""
import os, http.server, socketserver, webbrowser, threading, time

ASSETS = {
    "neutral.jpg":    ((180, 140, 120), "NEUTRAL"),
    "wink_left.jpg":  ((120, 160, 200), "WINK L"),
    "wink_right.jpg": ((200, 160, 120), "WINK R"),
    "tongue.jpg":     ((200, 120, 140), "TONGUE"),
}

def make_placeholder_images():
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs("assets", exist_ok=True)
    for fname, (color, label) in ASSETS.items():
        path = os.path.join("assets", fname)
        if not os.path.exists(path):
            img = Image.new("RGB", (400, 400), color)
            draw = ImageDraw.Draw(img)
            draw.rectangle([10, 10, 389, 389], outline=(255, 255, 255), width=4)
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            except:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), label, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((400 - w) // 2, (400 - h) // 2), label, fill=(255, 255, 255), font=font)
            img.save(path, "JPEG")
            print(f"  생성됨: {path}")
        else:
            print(f"  존재함: {path}")

PORT = 8080

def find_free_port(start):
    import socket
    for p in range(start, start + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", p)) != 0:
                return p
    return start

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # 로그 억제

print("=" * 50)
print("  페이스 디비디비딥")
print("=" * 50)
print("\n[1/2] 이미지 파일 확인 중...")
make_placeholder_images()
print("\n💡 실제 얼굴 사진으로 바꾸려면:")
print("   assets/ 폴더에 neutral.jpg, wink_left.jpg,")
print("   wink_right.jpg, tongue.jpg 를 복사하세요.\n")

PORT = find_free_port(PORT)

print(f"[2/2] 서버 시작: http://localhost:{PORT}")
print("      브라우저가 자동으로 열립니다.")
print("      종료: Ctrl+C\n")

def open_browser():
    time.sleep(0.8)
    webbrowser.open(f"http://localhost:{PORT}")

threading.Thread(target=open_browser, daemon=True).start()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n서버 종료.")

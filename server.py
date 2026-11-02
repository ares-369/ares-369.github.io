#!/usr/bin/env python3
"""
Prabhu Manikandan Viswanathan — Portfolio Production Server & Local Admin Studio
Serves public portfolio + LAN-restricted In-Browser Live Editor with continuous GitHub sync
"""

import http.server
import socketserver
import os
import sys
import json
import subprocess
import urllib.parse
import ipaddress
import threading

PORT = 8089
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "portfolio_data.json")
SECRET_KEY = "proxc-threat-hunter"

LAN_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/24"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"), # Tailscale CGNAT
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
]

def is_lan_or_authorized(client_ip, query_params, headers):
    # Check secret key in query
    if query_params.get("key", [""])[0] == SECRET_KEY:
        return True

    # Check X-Forwarded-For or X-Real-IP from NPM
    forwarded = headers.get("X-Forwarded-For", "")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    elif "X-Real-IP" in headers:
        client_ip = headers["X-Real-IP"].strip()

    try:
        ip_obj = ipaddress.ip_address(client_ip)
        for net in LAN_NETWORKS:
            if ip_obj in net:
                return True
    except ValueError:
        pass

    return False

def run_git_sync(commit_msg="Update via Admin Studio"):
    try:
        subprocess.run(["python3", os.path.join(BASE_DIR, "build_site.py")], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR)
        # Push in background
        subprocess.run(["git", "push", "github", "main"], cwd=BASE_DIR)
        subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR)
    except Exception as e:
        print(f"Sync error: {e}", file=sys.stderr)

class PortfolioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_HEAD(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        q = urllib.parse.parse_qs(parsed.query)
        if path in ["/admin", "/admin/", "/edit", "/editor"]:
            client_ip = self.client_address[0]
            if not is_lan_or_authorized(client_ip, q, self.headers):
                self.send_response(403)
                self.end_headers()
                return
            editor_path = os.path.join(BASE_DIR, "editor.html")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(os.path.getsize(editor_path)))
            self.end_headers()
            return
        return super().do_HEAD()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        q = urllib.parse.parse_qs(parsed.query)

        # Admin Editor Endpoint
        if path in ["/admin", "/admin/", "/edit", "/editor"]:
            client_ip = self.client_address[0]
            if not is_lan_or_authorized(client_ip, q, self.headers):
                self.send_response(403)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"""<!DOCTYPE html>
<html>
<head><title>403 Forbidden</title><style>body{background:#07090e;color:#f8fafc;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;}div{text-align:center;padding:30px;border:1px solid #d4a03e;border-radius:8px;}h1{color:#ef4444;margin:0 0 10px 0;}p{color:#94a3b8;}</style></head>
<body><div><h1>403 Forbidden</h1><p>Portfolio Admin Studio is restricted to the local network authorized administrative access.</p></div></body></html>""")
                return

            editor_path = os.path.join(BASE_DIR, "editor.html")
            with open(editor_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        # API: Get Data JSON
        if path == "/api/get-data":
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        q = urllib.parse.parse_qs(parsed.query)
        client_ip = self.client_address[0]

        if not is_lan_or_authorized(client_ip, q, self.headers):
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode("utf-8"))
            return

        # API: Save Data JSON
        if path == "/api/save-data":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)
            try:
                data = json.loads(post_body.decode("utf-8"))
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f, indent=2)

                # Rebuild site and trigger background sync
                threading.Thread(target=run_git_sync, args=("Update portfolio content via Admin Studio",)).start()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "Saved and syncing to GitHub & Homelab in background!"
                }).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        # API: Trigger Manual Sync
        if path == "/api/sync":
            threading.Thread(target=run_git_sync, args=("Manual sync triggered from Admin Studio",)).start()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Manual sync initiated!"}).encode("utf-8"))
            return

        # API: Upload CV PDF
        if path == "/api/upload-cv":
            content_type = self.headers.get("Content-Type", "")
            content_length = int(self.headers.get("Content-Length", 0))
            raw_data = self.rfile.read(content_length)

            try:
                # Find PDF binary boundary inside multipart or raw
                pdf_start = raw_data.find(b"%PDF-")
                if pdf_start != -1:
                    pdf_end = raw_data.rfind(b"%%EOF")
                    if pdf_end != -1:
                        pdf_bytes = raw_data[pdf_start:pdf_end + 5]
                    else:
                        pdf_bytes = raw_data[pdf_start:]
                    
                    cv_path = os.path.join(BASE_DIR, "Prabhu_Manikandan_Viswanathan_CV.pdf")
                    with open(cv_path, "wb") as f:
                        f.write(pdf_bytes)

                    threading.Thread(target=run_git_sync, args=("Update CV PDF via Admin Studio",)).start()

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "message": "CV PDF updated and syncing!"}).encode("utf-8"))
                    return
                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid PDF file uploaded"}).encode("utf-8"))
                    return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def main():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), PortfolioHandler) as httpd:
        print(f"Portfolio production server & Admin Studio listening on port {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()

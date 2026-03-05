FROM kalilinux/kali-rolling:latest

# Set environment
ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update && apt-get install -y \
    openssh-server \
    nmap \
    wireshark \
    git \
    python3-pip \
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    novnc \
    websockify \
    wget \
    curl \
    sublist3r \
    dirb \
    && rm -rf /var/lib/apt/lists/*

# Configure SSH
RUN mkdir -p /var/run/sshd
RUN echo 'root:toor' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# Configure VNC
RUN mkdir -p /root/.vnc
RUN echo 'toor' | vncpasswd -f > /root/.vnc/passwd
RUN chmod 600 /root/.vnc/passwd

# Fix novnc installation - copy from /usr/share/webapps/novnc to /usr/share/novnc
RUN mkdir -p /usr/share/novnc
RUN if [ -d "/usr/share/webapps/novnc/usr/share/novnc" ]; then \
        cp -r /usr/share/webapps/novnc/usr/share/novnc/* /usr/share/novnc/; \
    elif [ -d "/usr/share/webapps/novnc" ]; then \
        cp -r /usr/share/webapps/novnc/* /usr/share/novnc/; \
    fi
RUN if [ ! -f "/usr/share/novnc/vnc.html" ]; then \
        echo "vnc.html not found, creating simple redirect" && \
        cat > /usr/share/novnc/vnc.html << 'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kali Linux - VNC</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #2c3e50;
            color: #ecf0f1;
            text-align: center;
            margin: 0;
            padding: 50px;
        }
        .container {
            background-color: #34495e;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            max-width: 600px;
            margin: 0 auto;
        }
        h1 { color: #e74c3c; margin-bottom: 20px; }
        .info { background: #4a6741; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .warning { background: #f39c12; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .code { background: #34495e; padding: 5px 10px; border-radius: 3px; font-family: monospace; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Kali Linux - VNC Access</h1>
        <div class="info">
            <p><strong>Instructions for VNC Client:</strong></p>
            <p>1. Open your VNC client (RealVNC, TigerVNC, etc.)</p>
            <p>2. Connect to: <span class="code">localhost:6080</span></p>
            <p>3. Enter password: <span class="code">toor</span></p>
        </div>
        <div class="warning">
            <p>⚠️ <strong>Web Browser Access Not Available</strong> ⚠️</p>
            <p>noVNC web interface is not properly configured in this lab.</p>
            <p>Please use a dedicated VNC client for access.</p>
        </div>
        <div class="info">
            <p><strong>Alternative: SSH Access</strong></p>
            <p>Connect via SSH: <span class="code">ssh root@localhost -p 2222</span></p>
            <p>Password: <span class="code">toor</span></p>
        </div>
        <p><small>Lab Unit 1 - Reconnaissance & Enumeration</small></p>
    </div>
</body>
</html>
HTML
    fi

# Create VNC startup script
RUN cat > /root/start_vnc.sh << 'EOL'
#!/bin/bash
echo "Starting VNC server on :1..."
tightvncserver :1 -geometry 1280x720 -depth 24

echo "Checking VNC server..."
ss -tulpn | grep 5901 || true

echo "Starting websockify..."
websockify -D --web=/usr/share/novnc 0.0.0.0:8080 localhost:5901

echo "Services started successfully!"
echo "SSH: ssh root@localhost -p 2222"
echo "VNC: localhost:6080 (VNC client required, password: toor)"

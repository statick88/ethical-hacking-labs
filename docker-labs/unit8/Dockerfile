FROM kalilinux/kali-rolling

# Update and install packages
RUN apt-get update && apt-get install -y \
    openssh-server \
    nmap \
    python3-pip \
    powershell \
    git \
    zip \
    unzip \
    wget \
    curl \
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    novnc \
    websockify \
    && rm -rf /var/lib/apt/lists/*

# Install PowerSploit
RUN mkdir -p /root/tools && cd /root/tools && \
    git clone https://github.com/PowerShellMafia/PowerSploit.git

# Install Mimikatz
RUN wget -O /root/tools/mimikatz.exe https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20210512/mimikatz_trunk.zip && \
    unzip /root/tools/mimikatz.exe -d /root/tools/mimikatz && \
    rm /root/tools/mimikatz.exe

# Configure SSH
RUN mkdir -p /var/run/sshd
RUN echo 'root:toor' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# Configure VNC
RUN mkdir -p /root/.vnc
RUN echo 'toor' | vncpasswd -f > /root/.vnc/passwd
RUN chmod 600 /root/.vnc/passwd

# Create VNC startup script
RUN cat > /root/start_vnc.sh << 'EOL'
#!/bin/bash
tightvncserver :1 -geometry 1280x720 -depth 24
websockify -D --web=/usr/share/novnc/ 8080 localhost:5901
EOL

RUN chmod +x /root/start_vnc.sh

# Expose ports
EXPOSE 22
EXPOSE 8080

# Start services
CMD service ssh start && /root/start_vnc.sh && tail -f /dev/null

FROM kalilinux/kali-rolling

# Update and install packages
RUN apt-get update && apt-get install -y \
    openssh-server \
    python3-pip \
    git \
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    novnc \
    websockify \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install AI libraries
RUN pip3 install openai python-dotenv numpy pandas scikit-learn

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

FROM python:3.12-slim

# Set build arguments
ARG RELEASE_VERSION
ENV RELEASE_VERSION=${RELEASE_VERSION}

#  Install dependencies
RUN apt-get update && \
    apt-get install -y sudo wget libegl1 libopengl0 libxcb-cursor0 xz-utils fontconfig libxkbcommon0 libglx0 libnss3 gosu && \
    rm -rf /var/lib/apt/lists/*

# Install Calibre
RUN wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin
ENV LD_LIBRARY_PATH="/opt/calibre/lib:${LD_LIBRARY_PATH}"
ENV PATH="/opt/calibre/bin:${PATH}"

# Create directories and set permissions
COPY . /convertbooks
WORKDIR /convertbooks

# Make the script executable
RUN chmod +x thewicklowwolf-init.sh

# Expose port
EXPOSE 5000

# Start the app
ENTRYPOINT ["./thewicklowwolf-init.sh"]

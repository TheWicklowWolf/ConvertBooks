FROM python:3.12-slim

# Create User
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID general_user && \
    useradd -m -u $UID -g $GID general_user

# Install dependencies
RUN apt-get update && apt-get install -y sudo wget libegl1 libopengl0 libxcb-cursor0 xz-utils fontconfig libxkbcommon0 libglx0 libnss3

# Install Calibre
RUN wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin
ENV LD_LIBRARY_PATH="/opt/calibre/lib:${LD_LIBRARY_PATH}"
ENV PATH="/opt/calibre/bin:${PATH}"

# Create directories and set permissions
COPY . /convertbooks
WORKDIR /convertbooks
RUN chown -R general_user:general_user /convertbooks

# Switch user
USER general_user

# Specify the default command
CMD ["python", "ConvertBooks.py"]

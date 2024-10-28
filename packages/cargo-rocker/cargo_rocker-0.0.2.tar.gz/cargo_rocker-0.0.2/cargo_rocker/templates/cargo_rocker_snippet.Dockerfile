
#TODO install using rustup instead to get latest version
RUN apt-get update && apt-get install -y --no-install-recommends cargo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

#Alternative method not working yet
# RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
# Add .cargo/bin to PATH
# ENV PATH="/root/.cargo/bin:${PATH}"
FROM docker.io/rust:1.91.1-slim@sha256:5218a2b4b4cb172f26503ac2b2de8e5ffd629ae1c0d885aff2cbe97fd4d1a409

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

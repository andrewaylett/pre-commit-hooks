FROM docker.io/rust:1.90.0-slim@sha256:1219c0b5980e8310eb8e08a7fec9e2159ffc9f166cc9999ddb13604c43cd0eb6

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

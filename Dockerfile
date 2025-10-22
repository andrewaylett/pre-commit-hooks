FROM docker.io/rust:1.90.0-slim@sha256:0458e8607a3ce7a6f632dbfeb9a00a167bca0698bf19371f010c3ff3173d7cc7

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

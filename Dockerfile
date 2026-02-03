FROM docker.io/rust:1.93.0-slim@sha256:33d792786bc9abe7a17431938a17f41af781c83c2123ea620292a1ed381b6aea

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

FROM docker.io/rust:1.92.0-slim@sha256:6cff8a33b03d328aa58d00dedda6a3c5bbee4b41e21533932bffd90d7d58f9c4

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

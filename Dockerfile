FROM docker.io/rust:1.94.0-slim@sha256:f7bf1c266d9e48c8d724733fd97ba60464c44b743eb4f46f935577d3242d81d0

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

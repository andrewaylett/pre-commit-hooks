FROM docker.io/rust:1.92.0-slim@sha256:82dcd8ffae4a456f02582c457f87c35c189fe8cd381c0d76d81b95a1c324b440

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

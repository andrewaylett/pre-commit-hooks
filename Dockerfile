FROM docker.io/rust:1.95.0-slim@sha256:a6ed0cbc27f063c367aee8373f35fdf4dcf8be7596c4d19d6643e3252e514c2e

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

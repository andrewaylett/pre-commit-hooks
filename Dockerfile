FROM docker.io/rust:1.93.0-slim@sha256:df6ca8f96d338697ccdbe3ccac57a85d2172e03a2429c2d243e74f3bb83ba2f5

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

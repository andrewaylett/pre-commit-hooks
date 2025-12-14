FROM docker.io/rust:1.92.0-slim@sha256:0d8bf269f3ab28ddcdc3a182f519d7499daee82ce2faa4008048ae8adf6977e7

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

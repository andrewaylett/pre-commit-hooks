FROM docker.io/rust:1.94.1-slim@sha256:48150eec4f1e854ec689c7ca4c16d35193c4ea19dde13b6df515192707229ff8

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

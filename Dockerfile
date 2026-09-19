FROM docker.io/rust:1.98.1-slim@sha256:8ce659250d9f7783105e69af45d78c0b2308bf78bd5640182986944efe3a4579

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

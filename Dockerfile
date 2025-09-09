FROM docker.io/rust:1.89.0-slim@sha256:7ced053d0ec96d243d49a633dd7ee3f25e4055f172a898c8770e8ebc2ef86262

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

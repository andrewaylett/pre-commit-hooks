FROM docker.io/rust:1.99.1-slim@sha256:4195a35184f0f4e8964c0208f3b2427b4b7581933878ef44344e6125cdc76269

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

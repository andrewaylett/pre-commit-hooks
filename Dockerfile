FROM docker.io/rust:1.89.0-slim@sha256:6275519394d00d1f0a9ee15894c5851f4d6fdefc30648bc446b39c6eaf29c364

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

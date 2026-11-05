FROM docker.io/rust:1.99.1-slim@sha256:59f72d5265cfcf281fcfa4d990e75f09c53f911def9913c47a4a89dca690a887

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

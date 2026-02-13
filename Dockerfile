FROM docker.io/rust:1.93.1-slim@sha256:be030f67af64b7a5d35a69db45933f5c4589a16303e0ea4a6e3746b42b0679b9

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

FROM docker.io/rust:1.97.1-slim@sha256:b5b16ce96388d90eb217e162d4729b05c964c5c2388db28f70fbb8a4a66e1d26

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

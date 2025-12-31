FROM docker.io/rust:1.92.0-slim@sha256:567029e780d80f75d2c43d7b2cfe8c2bb5a2c7de2b719799b82ee2e97858d84a

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

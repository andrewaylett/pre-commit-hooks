FROM docker.io/rust:1.94.1-slim@sha256:a08d20a404f947ed358dfb63d1ee7e0b88ecad3c45ba9682ccbf2cb09c98acca

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

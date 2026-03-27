FROM docker.io/rust:1.94.1-slim@sha256:1d0000a49fb62f4fde24455f49d59c6c088af46202d65d8f455b722f7263e8f8

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

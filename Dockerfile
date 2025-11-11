FROM docker.io/rust:1.91.1-slim@sha256:cef0ec962e08d8b5dcba05604189e5751c1bd3ec7d12db0a93e4215468d4ac4a

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

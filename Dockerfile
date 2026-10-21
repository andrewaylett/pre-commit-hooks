FROM docker.io/rust:1.99.1-slim@sha256:00544ccc9431a2fe93e65185d21381b0a039342f5cefcf84fbddac273c9e573d

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

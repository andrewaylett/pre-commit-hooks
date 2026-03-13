FROM docker.io/rust:1.94.0-slim@sha256:7d3701660d2aa7101811ba0c54920021452aa60e5bae073b79c2b137a432b2f4

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

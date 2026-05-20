FROM docker.io/rust:1.95.0-slim@sha256:ee4fa026a11f9e8b1b00568364a880dc720409bb94b0e6800f63f974f9c909d5

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

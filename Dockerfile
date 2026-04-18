FROM docker.io/rust:1.95.0-slim@sha256:319f354c6f068b01c19292555033a0e6133b4249a893c479aec3b0b8ab2f660a

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

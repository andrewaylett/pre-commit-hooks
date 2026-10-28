FROM docker.io/rust:1.99.1-slim@sha256:45afd9478205dcdf7f98b099019fee773a33644cf69ac0a3b862eb31d2a1ccef

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

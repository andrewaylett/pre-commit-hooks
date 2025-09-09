FROM docker.io/rust:1.89.0-slim@sha256:5af71cbdfd7f555a7c46a6d03eac95abf403bb8f8126bafb8bc0afa1f081810d

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

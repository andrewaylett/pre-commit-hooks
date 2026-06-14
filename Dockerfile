FROM docker.io/rust:1.96.0-slim@sha256:3b05f7c617a200c41c3506097f0d15fc193a1c93bfd8f141007b47cac8f95d3c

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

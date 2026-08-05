FROM docker.io/rust:1.97.1-slim@sha256:69153971349358535be9821190190f026a761f690c6b58c68a914d14ab2d610a

RUN rustup component add clippy rustfmt

ENTRYPOINT ["/usr/local/cargo/bin/cargo"]

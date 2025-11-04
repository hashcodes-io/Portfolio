# Architecture
This demo intentionally stays small and auditable. Key components:

- **ipnet_demo.ipam**: Core allocation logic, thread-safe, stores allocations in SQLite.
- **ipnet_demo.api**: FastAPI microservice exposing simple REST operations used by developer tools/CI.
- **CI pipeline**: Lints, tests, and builds an image. Replace `docker build` step with `docker/publish` or `helm` steps for production.#

# TODO Add how to use
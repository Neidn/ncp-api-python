# CHANGELOG


## v0.2.0 (2026-07-28)

### Bug Fixes

- Add future annotations and __version__ to __all__ in package init
  ([`afc5222`](https://github.com/Neidn/ncp-api-python/commit/afc5222ad4cc0323e655870eba6620807b7e0c54))

- Add httpx client lifecycle management and async network-error tests
  ([`d106a44`](https://github.com/Neidn/ncp-api-python/commit/d106a444f3e6f51360fee487a3bfd7a2456cadc8))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Correct HMAC signature format and include query params in signing
  ([`2d4cd6c`](https://github.com/Neidn/ncp-api-python/commit/2d4cd6cda48501bc084a213bce558fc9e8763878))

Two bugs causing 401 auth failures: 1. string_to_sign used \n between method and URL; NCP expects a
  space 2. GET query params were not included in the signed URL — httpx appends them after signing,
  so the server received a URL that didn't match the signature

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_01HQLhFH766hkFhr1epC4bxx

- Exclude markdown from ruff format and commit uv.lock for reproducible CI
  ([`973dab8`](https://github.com/Neidn/ncp-api-python/commit/973dab897d56a143ddf906189f32defd8b6325b7))

CI's ruff format --check . was failing on README.md and docs/*.md because uv.lock was gitignored, so
  every CI run re-resolved dependencies from scratch and could silently pick up a newer ruff release
  (0.16.0 vs the 0.15.18 used locally) with different default file-discovery behavior for Markdown.
  Excluding *.md from ruff format makes this version-proof, and committing uv.lock pins CI to the
  same resolved dependency set as local dev so this class of drift can't recur.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_01HQLhFH766hkFhr1epC4bxx

- Resolve ruff lint violations blocking CI release pipeline
  ([`fc26520`](https://github.com/Neidn/ncp-api-python/commit/fc2652022e44d0ddff9c6b9a2efb40ffcd6b0883))

E501 line-too-long in test_adapters_object_storage.py and F811 duplicate make_server_api definition
  in test_adapters_server.py were failing the lint job, which gated typecheck/test/release and
  stopped version tags from being cut since the last release.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_01HQLhFH766hkFhr1epC4bxx

### Chores

- Update gitignore (add .idea, .coverage; note uv.lock)
  ([`cc8e7c0`](https://github.com/Neidn/ncp-api-python/commit/cc8e7c0175ff5f2d2aad029b64de80531714e9ba))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Documentation

- Add NCP API base layer design spec
  ([`999735d`](https://github.com/Neidn/ncp-api-python/commit/999735da7a952399e870ce6f5f8d26954740c0b4))

- Add NCP API base layer implementation plan
  ([`0711ade`](https://github.com/Neidn/ncp-api-python/commit/0711ade11a8873a8b0fae3673efd382a02a77eab))

- Expand error handling section in README with retry examples
  ([`aa0a64a`](https://github.com/Neidn/ncp-api-python/commit/aa0a64a04c683042c6da12b38ea7267f8884b03f))

Add NcpRateLimitError usage, error_code distinction for auth errors, and retry patterns (tenacity +
  manual backoff)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Features

- Add adapter scaffolding and NcpClient entry point
  ([`e54aa49`](https://github.com/Neidn/ncp-api-python/commit/e54aa49af498ad45934df8d8b5964b7509f46a40))

Creates PublicAdapter/GovAdapter/FinAdapter subclasses, NcpClient with env resolution (param →
  NCP_ENV → "public"), and updates package __init__.py. Also fixes ruff lint issues in prior-task
  test files.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add BlockStorageApi, CloudCacheApi, and CloudRedisApi adapters; update NcpClient to include new
  services and enhance integration tests
  ([`15c2966`](https://github.com/Neidn/ncp-api-python/commit/15c2966afbe03e18f0807a202feb21843ff07549))

- Add CloudInsightApi with query_data_multiple
  ([`e28717b`](https://github.com/Neidn/ncp-api-python/commit/e28717b5a9291eea86e52b61aa9d0a7ac5a6a4cb))

- CloudInsightApi uses _service_base_url (https://cw.apigw.ntruss.com) - POST
  /cw_fea/real/cw/api/data/query/multiple with JSON body - MetricInfo dataclass: prod_key, metric,
  interval, dimensions, aggregation, query_aggregation - Supports up to 20 metrics per call, returns
  list of dps results - Wired into PublicAdapter, GovAdapter, FinAdapter - Exposed as
  client.cloud_insight property

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add CloudMongoDbApi and CloudMysqlApi adapters; update dependencies and tests
  ([`33f7f45`](https://github.com/Neidn/ncp-api-python/commit/33f7f45c7e8768a6ff8e47f0e04a39d76d8b2fea))

- Add CloudPostgresqlApi adapter for managing PostgreSQL instances; update README and tests
  ([`86ea728`](https://github.com/Neidn/ncp-api-python/commit/86ea728e5179e4c8781672b51a8a84fbbb0c2520))

- Add exception hierarchy and environment config
  ([`a520d26`](https://github.com/Neidn/ncp-api-python/commit/a520d26beb53f478fec1ee0babb26e5d4171ee36))

- Add get_system_schema_key_list and aget_system_schema_key_list methods to CloudInsightApi; enhance
  tests for schema key list retrieval
  ([`192da47`](https://github.com/Neidn/ncp-api-python/commit/192da47b2475ceebe1da245e56cb09e24e604f00))

- Add HmacSigner for NCP HMAC-SHA256 authentication
  ([`365dfcd`](https://github.com/Neidn/ncp-api-python/commit/365dfcd91842298161265cb96a7b3a634a3eaaf3))

- Add integration tests for Auto Scaling, Cloud Hadoop, Cloud MSSQL, CDN, CDSS, SES, and Classic
  Cloud DB services; enhance README with key methods for supported APIs
  ([`05636e1`](https://github.com/Neidn/ncp-api-python/commit/05636e1640a2c26ef9941797d8714174773074cd))

- Add LoadBalancerApi adapter; update NcpClient and tests for load balancer instance retrieval
  ([`a16e5a3`](https://github.com/Neidn/ncp-api-python/commit/a16e5a3ae4d4dab4e95cc1a2bc732613a4186013))

- Add NasApi and ObjectStorageApi adapters; update NcpClient and README with new functionalities
  ([`aa5bfe8`](https://github.com/Neidn/ncp-api-python/commit/aa5bfe8ca66f01de0cf7e11ab9de326403448828))

- Add NcpHttpAdapter with HMAC auth and error mapping
  ([`ddef9c6`](https://github.com/Neidn/ncp-api-python/commit/ddef9c6acbe91fcc3101838e0a2a48cde7d6f5a3))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add NcpRateLimitError and error_code to NcpAuthError
  ([`43a1a5e`](https://github.com/Neidn/ncp-api-python/commit/43a1a5e6b9c6c63754e58693d14a72ae3727c491))

Map NCP gateway error codes to exception types: - NcpAuthError now carries error_code (200=auth
  failed, 210=permission denied) - NcpRateLimitError(NcpApiError) for HTTP 429 (400/410/420
  returnCodes) - _handle_response branches on 401 and 429 before generic NcpApiError

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add network interface and access control group list retrieval methods; enhance async support for
  access control group rules
  ([`cc7bb82`](https://github.com/Neidn/ncp-api-python/commit/cc7bb82c7c71f0261b23cb512a0e63afe6ec7d7e))

- Add NksApi adapter for managing NKS clusters and nodes; update README and integration tests
  ([`4de03d1`](https://github.com/Neidn/ncp-api-python/commit/4de03d14e2448e2cde42d9bd36918aa1b2799bf4))

- Add ResourceManagerApi and CloudActivityTracerApi adapters
  ([`0ee527b`](https://github.com/Neidn/ncp-api-python/commit/0ee527b2842f18adca685e61686170eee0b7d953))

Enables looking up NCP resources by nrn/type/name (Resource Manager) and querying who performed an
  action on a resource (Cloud Activity Tracer), e.g. to find who created a given server instance.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_01HQLhFH766hkFhr1epC4bxx

- Add ServerApi with getServerInstanceList and README
  ([`5386dba`](https://github.com/Neidn/ncp-api-python/commit/5386dbabc9ea5f6a64e3b552037d007e99307696))

- Add ServerApi (path_prefix /vserver/v2) shared across all three environments - Wire self.server
  into PublicAdapter, GovAdapter, FinAdapter - Expose client.server property on NcpClient - Support
  all documented query params including .N array format - Add sync + async variants with 9 tests -
  Add README.md with usage, environment, error handling examples - Add CLAUDE.md with dev commands
  and architecture guide

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add target group list and detail retrieval methods for LoadBalancerApi and NasApi; enhance async
  support for NAS volume instance ratings
  ([`9bcef79`](https://github.com/Neidn/ncp-api-python/commit/9bcef796068be59e2a11449d3db1d637763d9b72))

- Remove outdated usage examples from README; streamline documentation for clarity
  ([`826a0c8`](https://github.com/Neidn/ncp-api-python/commit/826a0c8f867079863b665a664c1fa68c7ae322fa))

- Update NksApi to use environment-specific base URLs and add region support for KRS in cluster list
  retrieval tests
  ([`4ce6c28`](https://github.com/Neidn/ncp-api-python/commit/4ce6c281d8a81c3ddc2ff63adf82dbfe4c4ce3a6))

### Refactoring

- Improve code formatting and readability across multiple files
  ([`f4519a5`](https://github.com/Neidn/ncp-api-python/commit/f4519a5a9d8e176463c6c45114e4be24af214335))

- Inject Cloud Insight domain per-env via CLOUD_INSIGHT_BASE_URLS
  ([`5e628fd`](https://github.com/Neidn/ncp-api-python/commit/5e628fd07f6c970d23939b469e6fc3b74d7b2e28))

Remove _service_base_url class var from CloudInsightApi — domain is env-dependent, not fixed. Each
  env adapter now passes the correct Cloud Insight base URL from CLOUD_INSIGHT_BASE_URLS dict.
  Gov/Fin URLs are placeholders pending doc confirmation.

Also add Cloud Insight usage example to README.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>


## v0.1.0 (2026-06-19)

### Chores

- Add gitignore, wire pytest-cov, add pythonpath config
  ([`622840f`](https://github.com/Neidn/ncp-api-python/commit/622840fb9ca0541998dcf40fe7c208703b40dda7))

- Exclude .superpowers/ from git tracking
  ([`7c2068a`](https://github.com/Neidn/ncp-api-python/commit/7c2068ae10c5e5eded4873357a1ecc3a67ba7773))

### Documentation

- Add dev harness implementation plan
  ([`1da6176`](https://github.com/Neidn/ncp-api-python/commit/1da6176e8ad35d35a52fae7f4041a17c52ec13aa))

- Add development harness design spec
  ([`20b9c63`](https://github.com/Neidn/ncp-api-python/commit/20b9c638e3c2a4f174186f2aa9254df0232e181f))

- Fix workflow job parallelism in harness spec
  ([`771e04d`](https://github.com/Neidn/ncp-api-python/commit/771e04d450fb47ef357824b1b56cd6196a936a56))

### Features

- Add GitHub Actions CI/CD workflow
  ([`778a19b`](https://github.com/Neidn/ncp-api-python/commit/778a19b90e0178705994378b5f92ec0f1654d7ed))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Add Makefile with dev shortcuts
  ([`6877825`](https://github.com/Neidn/ncp-api-python/commit/6877825e930733ebe14aae2a4b070c4686aad931))

- Scaffold src-layout package with dev tooling config
  ([`7049d3a`](https://github.com/Neidn/ncp-api-python/commit/7049d3a96976ae32acc07a13c6cdb16ee8b7ed5d))

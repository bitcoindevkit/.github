## Hey there 👋

![An image of the bitcoin development kit logo](https://github.com/bitcoindevkit/.github/blob/master/profile/bdk-banner.png?raw=true)

Bitcoin Development Kit (BDK) is a suite of software libraries that allows you to build secure, feature-rich, and cross-platform Bitcoin wallets.

Most of the BDK projects are based on the powerful [`rust-bitcoin`](https://github.com/rust-bitcoin/rust-bitcoin) and [`rust-miniscript`](https://github.com/rust-bitcoin/rust-miniscript) libraries.

The home page for the overarching BDK project and the BDK Foundation that supports it is [bitcoindevkit.org](https://bitcoindevkit.org/).

### Project Tiers

We provide the technical infrastructure to maintain a number of software and documentation projects across different maturity levels and support models. To help you navigate these projects, we've categorized them along two dimensions: Maturity Level (Stable or Experimental) and Support Model (Foundation or Community). See "The Book of BDK" [chapter on library tiers](https://bookofbdk.com/getting-started/tiers/#library-tiers) for more details.

#### Foundation Supported

##### Stable

- [bdk_wallet] - A modern, lightweight, descriptor-based wallet rust crate.
- [bdk_chain] - Tools for storing and indexing bitcoin blockchain data.
- [bdk_core] - A collection of core structures used by the [bdk_chain], [bdk_wallet], and BDK's chain data source crates.
- [bdk_esplora] - Extends the [esplora-client] crate with methods to fetch blockchain data for [bdk_chain] and [bdk_wallet] to consume.
- [bdk_electrum] - Extends the [electrum-client] crate with methods to fetch blockchain data for [bdk_chain] and [bdk_wallet] to consume.
- [bdk_bitcoind_rpc] - Emits blockchain data from the bitcoind RPC interface for [bdk_chain] and [bdk_wallet] to consume.
- [bdk_testenv] - A framework that provides the infrastructure for testing blockchain data source crates.
- [esplora-client] - Asynchronous and blocking clients and types for interacting with Esplora servers over HTTP.
- [electrum-client] - Bitcoin Electrum client crate that supports plaintext, TLS and Onion servers.
- [bdk-ffi] - A [bdk_wallet] wrapper that uses uniffi-rs to generate bindings for other languages.
- [bdk-jvm] - Kotlin JVM language bindings library for [bdk_wallet] generated with [bdk-ffi].
- [bdk-android] - Kotlin Android language bindings library for [bdk_wallet] generated with [bdk-ffi].
- [bdk-swift] - Swift language bindings library for [bdk_wallet] generated with [bdk-ffi].
- [book-of-bdk] - The documentation website for BDK project.

[bdk_wallet]: https://github.com/bitcoindevkit/bdk_wallet
[bdk_chain]: https://github.com/bitcoindevkit/bdk/tree/master/crates/chain
[bdk_core]: https://github.com/bitcoindevkit/bdk/tree/master/crates/core

[bdk_esplora]: https://github.com/bitcoindevkit/bdk/tree/master/crates/esplora
[bdk_electrum]: https://github.com/bitcoindevkit/bdk/tree/master/crates/electrum
[bdk_bitcoind_rpc]: https://github.com/bitcoindevkit/bdk/tree/master/crates/bitcoind_rpc

[bdk_testenv]: https://github.com/bitcoindevkit/bdk/tree/master/crates/testenv
[esplora-client]: https://github.com/bitcoindevkit/rust-esplora-client
[electrum-client]: https://github.com/bitcoindevkit/rust-electrum-client

[bdk-ffi]: https://github.com/bitcoindevkit/bdk-ffi
[bdk-jvm]: https://github.com/bitcoindevkit/bdk-jvm
[bdk-android]: https://github.com/bitcoindevkit/bdk-ffi/tree/master/bdk-android
[bdk-swift]: https://github.com/bitcoindevkit/bdk-swift

[book-of-bdk]: https://github.com/bitcoindevkit/book-of-bdk

##### Experimental

- [bdk_coin_select] - A zero-dependency crate for efficiently selecting inputs for making Bitcoin transactions.
- [bdk_file_store] - Persistence backend for storing chain data in a single file, not for mainnet use.
- [bdk_tx] - A minimal dependency crate that lets you build, update, and finalize PSBTs.
- [bdk_sp] - A crate to research the implementation of silent payment tools in BDK.
- [electrum_streaming_client] - Electrum client crate that honors the Electrum API’s push-based model.
- [bdk_sqlite] - SQLite blockchain and wallet data store crate for BDK using `sqlx`.
- [bdk-dart] - Dart language bindings library for [bdk_wallet] generated with [bdk-ffi].
- [bdk-rn] - React Native language bindings library for [bdk_wallet] generated with [bdk-ffi].
- [bdk-cli] - A CLI wallet library and REPL tool to demo and test the BDK library, not for mainnet use.
- [BDKSwiftExampleWallet] - An example native iOS wallet app built with [bdk-swift], not for mainnet use.
- [devkit-wallet] - An example native Android wallet built with [bdk-android], not for mainnet use.

[bdk_coin_select]: https://github.com/bitcoindevkit/coin-select
[bdk_file_store]: https://github.com/bitcoindevkit/bdk/tree/master/crates/file_store
[bdk_tx]: https://github.com/bitcoindevkit/bdk-tx
[bdk_sp]: https://github.com/bitcoindevkit/bdk-sp
[electrum_streaming_client]: https://github.com/bitcoindevkit/electrum_streaming_client
[bdk-bitcoind-client]: https://github.com/bitcoindevkit/bdk-bitcoind-client
[bdk_sqlite]: https://github.com/bitcoindevkit/bdk-sqlite
[bdk-dart]: https://github.com/bitcoindevkit/bdk-dart
[bdk-rn]: https://github.com/bitcoindevkit/bdk-rn
[bdk-cli]: https://github.com/bitcoindevkit/bdk-cli
[BDKSwiftExampleWallet]: https://github.com/bitcoindevkit/BDKSwiftExampleWallet
[devkit-wallet]: https://github.com/bitcoindevkit/devkit-wallet

#### Community Supported

##### Stable

- [bdk_kyoto] - BDK blockchain backend using P2P light client Kyoto.
- [bdk-python] - Python language bindings library for [bdk_wallet] generated with [bdk-ffi].
- [bdk-wasm] - WASM bindings library for [bdk_wallet] for JS and Node environments.
- [bdk-reserves] - A crate that implements proof-of-reserves for [bdk_wallet].
- [rust-cktap] - Coinkite Tap Protocol implementation for use with SATSCARD and TAPSIGNER products.
- [awesome-bdk] - A curated list of BDK resources, projects, codebases, and documentation.

[bdk_kyoto]:https://github.com/bitcoindevkit/bdk-kyoto
[bdk-python]: https://github.com/bitcoindevkit/bdk-python
[bdk-wasm]: https://github.com/bitcoindevkit/bdk-wasm
[bdk-reserves]: https://github.com/bitcoindevkit/bdk-reserves
[rust-cktap]: https://github.com/bitcoindevkit/rust-cktap
[awesome-bdk]: https://github.com/bitcoindevkit/awesome-bdk

##### Experimental

- [bdk_sqlx] - Postgres blockchain and wallet data store crate for BDK using `sqlx`.
- [bitcoin-ffi] - A light wrapping on rust-bitcoin required for use in uniffi-based libraries.
- [bdk-message-signer] - Crate to sign messages for proving fund availabilty or committing to a message.

[bdk_sqlx]: https://github.com/bitcoindevkit/bdk-sqlx
[bitcoin-ffi]: https://github.com/bitcoindevkit/bitcoin-ffi
[bdk-message-signer]: https://github.com/bitcoindevkit/bdk-message-signer

### 😃 Join our community

Community is fundamental to building and maintaining free and open source software and documentation. Please connect with 
us on GitHub and the BDK [discord server](https://discord.gg/UbTmGbNF3M)!

[https://bitcoindevkit.org]: https://bitcoindevkit.org

## Hey there 👋

![An image of the bitcoin development kit logo](https://github.com/bitcoindevkit/.github/blob/master/profile/bdk-banner.png?raw=true)

Bitcoin Development Kit (BDK) is a suite of software libraries that allows you to build secure, feature-rich, and cross-platform Bitcoin wallets.

Most of the BDK projects are based on the powerful [`rust-bitcoin`](https://github.com/rust-bitcoin/rust-bitcoin) and [`rust-miniscript`](https://github.com/rust-bitcoin/rust-miniscript) libraries.

The home page for the overarching BDK project and the BDK Foundation that supports it is [bitcoindevkit.org](https://bitcoindevkit.org/).

### Project Tiers

We provide the technical infrastructure to maintain a number of software and documentation projects across different maturity levels and support models. To help you navigate these projects, we've categorized them along two dimensions: Maturity Level (Stable or Experimental) and Support Model (Foundation or Community). See "The Book of BDK" [chapter on library tiers](https://bookofbdk.com/getting-started/tiers/#library-tiers) for more details.

The lead and secondary maintainers for each project are responsible for:

  - triaging new issues and PRs
  - providing guidance to contributors
  - reviewing and merging changes based on rough consensus
  - making and publishing releases

#### Foundation Supported

##### Stable

| Project                     | Lead Maintainer    | Secondary Maintainer   |
| --------------------------- | ------------------ | ---------------------- |
| [bdk_wallet]                | [ValuedMammal]     | [oleonardolima]        |
| [bdk_core]                  | [evanlinjin]       | [oleonardolima]        |
| [bdk_chain]                 | [evanlinjin]       | [oleonardolima]        |
| [bdk_esplora]               | [oleonardolima]    | [luisschwab]           |
| [bdk_electrum]              | [evanlinjin]       | [oleonardolima]        |
| [bdk_bitcoind_rpc]          | [evanlinjin]       | [ValuedMammal]         |
| [bdk_testenv]               | [tvpeter]          | [luisschwab]           |
| [esplora-client]            | [oleonardolima]    | [luisschwab]           |
| [electrum-client]           | [oleonardolima]    | [luisschwab]           |
| [bdk-ffi]                   | [thunderbiscuit]   | [reez]                 |
| [bdk-jvm]                   | [thunderbiscuit]   | [ItoroD]               |
| [bdk-android]               | [thunderbiscuit]   | [reez]                 |
| [bdk-swift]                 | [reez]             | [thunderbiscuit]       |
| [book-of-bdk]               | [thunderbiscuit]   | [reez]                 |

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

| Project                     | Lead Maintainer    | Secondary Maintainer   |
| --------------------------- | ------------------ | ---------------------- |
| [bdk_coin_select]           | [evanlinjin]       |                        |
| [bdk_file_store]            | [nymius]           |                        |
| [bdk_tx]                    | [ValuedMammal]     | [aagbotemi]            |
| [bdk_sp]                    | [nymius]           |                        |
| [electrum_streaming_client] | [evanlinjin]       | [oleonardolima]        |
| [bdk-bitcoind-client]       | [ValuedMammal]     | [tvpeter]              |
| [bdk_sqlite]                | [ValuedMammal]     |                        |
| [bdk-dart]                  | [reez]             | [Johnosezele]          |
| [bdk-rn]                    | [thunderbiscuit]   | [reez]                 |
| [bdk-cli]                   | [tvpeter]          |                        |
| [BDKSwiftExampleWallet]     | [reez]             |                        |
| [devkit-wallet]             | [thunderbiscuit]   |                        |

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

| Project                     | Lead Maintainer    | Secondary Maintainer   |
| --------------------------- | ------------------ | ---------------------- |
| [bdk_kyoto]                 | [rustaceanrob]     |                        |
| [bdk-python]                |                    |                        |
| [bdk-wasm]                  | [darioAnongba]     |                        |
| [bdk-reserves]              | [ulrichard]        |                        |
| [rust-cktap]                | [notmandatory]     |  [reez]                |
| [awesome-bdk]               | [thunderbiscuit]   |                        |

[bdk_kyoto]:https://github.com/bitcoindevkit/bdk-kyoto
[bdk-python]: https://github.com/bitcoindevkit/bdk-python
[bdk-wasm]: https://github.com/bitcoindevkit/bdk-wasm
[bdk-reserves]: https://github.com/bitcoindevkit/bdk-reserves
[rust-cktap]: https://github.com/bitcoindevkit/rust-cktap
[awesome-bdk]: https://github.com/bitcoindevkit/awesome-bdk

##### Experimental

| Project                     | Lead Maintainer        | Secondary Maintainer   |
| --------------------------- | ---------------------- | ---------------------- |
| [bdk_sqlx]                  | [matthiasdebernardini] |                        |
| [bitcoin-ffi]               |                        |                        |
| [bdk-message-signer]        | [aagbotemi]            |                        |

[bdk_sqlx]: https://github.com/bitcoindevkit/bdk-sqlx
[bitcoin-ffi]: https://github.com/bitcoindevkit/bitcoin-ffi
[bdk-message-signer]: https://github.com/bitcoindevkit/bdk-message-signer

### 😃 Join our community

Community is fundamental to building and maintaining free and open source software and documentation. Please connect with 
us on GitHub and the BDK [discord server](https://discord.gg/UbTmGbNF3M)!

[ValuedMammal]: https://github.com/ValuedMammal
[evanlinjin]: https://github.com/evanlinjin
[reez]: https://github.com/reez
[thunderbiscuit]: https://github.com/thunderbiscuit
[rustaceanrob]: https://github.com/rustaceanrob
[oleonardolima]: https://github.com/oleonardolima
[tvpeter]: https://github.com/tvpeter
[ItoroD]: https://github.com/ItoroD
[nymius]: https://github.com/nymius
[darioAnongba]: https://github.com/darioAnongba
[notmandatory]: https://github.com/notmandatory
[ulrichard]: https://github.com/ulrichard
[matthiasdebernardini]: https://github.com/matthiasdebernardini
[luisschwab]: https://github.com/luisschwab
[aagbotemi]: https://github.com/aagbotemi
[Johnosezele]: https://github.com/Johnosezele

[https://bitcoindevkit.org]: https://bitcoindevkit.org

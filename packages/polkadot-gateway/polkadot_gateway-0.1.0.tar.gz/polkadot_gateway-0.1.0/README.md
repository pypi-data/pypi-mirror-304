# polkadot-gateway

Abstractions for the Polkadot ecosystem. 

This package is a very opinionated wrapper around `py-substrate-interface`. It provides a simple synchronous interface for interacting with the Polkadot ecosystem. The `polkadot-gateway` package can automatically detect when the metadata is outdated and refresh it behind the scenes. This ensures that developers don’t have to manually handle metadata updates.

Note: Light client functionality is not yet supported. 

## Installation

`pip install polkadot-gateway`

## Usage

### Basic usage

```python

from polkadot import Polkadot

# Initialize Polkadot instance
polka = Polkadot()  # Defaults to the mainnet relay chain

# Optionally, specify a custom RPC endpoint or use a testnet
polka = Polkadot(endpoint="wss://rpc.polkadot.io")

# Get account balance
balance = polka.get_balance("12pDATAH2rCakrYjo6UoYFtmTEUpSyePTum8U5x9QdySZuqn")
print(f"Balance: {balance} DOT")

```

### Advanced usage

#### Advanced functions 

```python

from polkadot import Polkadot

# Staking
polka.nominate(nominator_keypair, ["Validator1", "Validator2"])

# Governance
polka.vote(proposal_hash, True, keypair)

```

### Parachain usage

Parachains can extend the functionality for their own chain very easily.

#### Acala Defi

```python

from polkadot.parachains import Acala

# Initialize Acala parachain interface
acala = Acala()

# Get balance in Acala (native token)
balance = acala.get_balance("account_address")
print(f"Balance: {balance} ACA")

# Swap tokens using Acala's DEX
acala.swap_tokens(sender_keypair, "DOT", "ACA", 10)

```

#### Moonbeam Contract calling


```python
from polkadot.parachains import Moonbeam

# Initialize Moonbeam parachain interface
moonbeam = Moonbeam()

# Interact with Moonbeam smart contracts
contract = moonbeam.get_contract("contract_address")
result = contract.call_method("methodName", params)
```
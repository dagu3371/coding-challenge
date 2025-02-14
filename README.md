## Context

[Rated](rated.network) offers a solution to the poor contextualization of validator quality. The solution is centered around reputation scores for machines and their operators, starting with the Ethereum Beacon Chain.

Rated seeks to embed a large swathe of available information from all layers of a given network, and compress it in an easily legible and generalizable reputation score that can act as an input to human workflows but most importantly, machines (e.g. an API that acts as an input to insurance or derivatives Smart Contracts).

## The Exercise

The purpose of this exercise is to manipulate an Ethereum transaction [dataset](https://github.com/rated-network/coding-challenge/blob/main/ethereum_txs.csv) using Python.

The following resources provide the required background:

- [ETH transaction](https://ethereum.org/en/developers/docs/transactions/)
- [Blockchain Explorer](https://etherscan.io/)
- [Gas fees](https://ethereum.org/en/developers/docs/gas/)
- [ETH Gas Tracker](https://etherscan.io/gastracker)
- [ETH units](https://gwei.io/)

## Guidelines

This solution should consist of 5 parts:

1. Assuming block length is 12 seconds, compute the approximate execution timestamp of each transaction.
2. Compute the gas cost of each transaction in Gwei (1e-9 ETH).
3. Using [Coingecko's](https://www.coingecko.com/en/api/documentation) API, retrieve the approximate price of ETH at transaction execution time and compute the dollar cost of gas used.
4. Populate a local database with the processed transactions.
5. Using the database in part 4, implement an API endpoint in a framework of your choosing that serves the following endpoints:

### Transactions API

API endpoint that returns a compact transaction view.
```
GET /transactions/:hash

{
  "hash": "0xaaaaa",
  "fromAddress": "0x000000",
  "toAddress": "0x000001",
  "blockNumber": 1234,
  "executedAt": "Jul-04-2022 12:02:24 AM +UTC",
  "gasUsed": 12345678,
  "gasCostInDollars": 4.23,
}
```

### Stats API

API endpoint that returns aggregated global transaction stats.
```
GET /stats

{
  "totalTransactionsInDB": 1234,
  "totalGasUsed": 1234567890,
  "totalGasCostInDollars": 12345
}

```

### What are we looking for?
We place a strong emphasis on delivering exceptional and reliable software. However, it's crucial to acknowledge that our applications will continuously evolve as we expand and refine our product offerings.

As a result, we prioritize flexibility and adaptability over purely architectural aesthetics. While we value elegant design, our focus remains on building resilient systems that can gracefully accommodate future changes and improvements.

Therefore, we recommend you to focus on code simplicity, readability and maintainability.

That being said,
* The solution should adhere to production-like coding standards.
* Your code must be delivered in a Github repository.
* Your code should include tests.
* Nice to have: `pydantic`, `FastAPI`, `pytest`.
* You will stand out by converting the CSV into an event stream and processing that stream.

Good luck!

## Solution Overview
The provided CSV data is streamed into a Kafka topic. The data is then processed and stored in a Postgres database. The API provides endpoints to retrieve transaction details and statistics.

## Running the application
### Docker
```
docker-compose up --build
```

### Accessing docker postgres
Once you have run the endpoints and have data you can log into the postgres on the docker container. Find the container id and login.

```
docker ps
docker exec -it <container_id> psql -U postgres -d ethereum_db
SELECT * FROM transactions;
```

### Tests
```
docker-compose build test
docker-compose run test
```

### Local build and test
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
pytest
curl http://localhost:8000/
```

## Endpoints
## Produce csv messages to Kafka
This endpoint reads messages from the Ethereum CSV, processes them, and stores them on a transactions Kafka topic. The execution timestamp and gas cost are calculated before storing.

```
curl http://localhost:8000/produce-to-kafka/
```

## Consume messages from Kafka event stream
This endpoint consumes messages from a Kafka topic and stores them in a Postgres Database.

```
curl http://localhost:8000/consume-from-kafka/
```

## Fetch Transaction by Hash
This endpoint fetches transactions stored in the Postgres database based on a given transaction hash

```
curl http://localhost:8000/transactions/0x6f218a5e009c56f8db17e933af7cc98360b699ae88cb85ef31c3eb351ecdee24
```

## Fetch Stats
This endpoint fetches statistics based on transactions stored in the Postgres database

```
curl http://localhost:8000/stats/
```

## Calculating Execution Time in a block
Some approximations have been made since it is difficult to know the exact time that a miner has finished mining a block. Given that the block length is 12 seconds we can presume that from any given block timestamp, i.e when the block was first mined, the transaction could have happened anytime in this 12 second window.
Based on the transaction index we can know the location of a transaction within a block. With this and the assumption that all transactions are evenly spaced out we define the approximate execution time as:

`block_timestamp + timedelta(seconds=transaction_index * BLOCK_LENGTH)`

## Calculating Gas Cost
First we convert gas cost wei `gas_used * gas_price`, then we convert to eth and multiply by the eth price to get a value in dollars.

## Nice to have
- Polling using Kafka connect for example so we aren't manually triggering the kafka source and sink operations
- Airflow to manage data quality
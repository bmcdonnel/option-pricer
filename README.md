# Overview
This project is a simple implementation of a binomial option contract pricing model. Currently there is no GUI, only CLI.

# Market Data
Pricing information about underlyings is currently using a free HTTP-based API provided by IEX Trading [documentation](https://iextrading.com/developer/docs/#getting-started). This is good enough for now, but it may be worth upgrading to a paid real-time market data stream.

Interest rate information is being pulled from another free HTTP-based API provided by Quandl (see the Treasury Yield Curve example [here](https://www.quandl.com/data/USTREASURY/YIELD-Treasury-Yield-Curve-Rates)).  
# Binomial Pricing
There are multiple variants of binomial pricing models, each differing in its definition of the 3 key input variables. The plan for this project is to implement both [Cox-Russ-Rubinstein](http://www.goddardconsulting.ca/option-pricing-binomial-index.html#crr) and [Jarrow-Rudd](http://www.goddardconsulting.ca/option-pricing-binomial-alts.html#jr) variants.

# Running the Application
Install docker for your system (instructions [here](https://docs.docker.com/install/)) and make sure the runtime has started.

Start the application:

```bash
$> make run
```

# Developing
To bring up the application container with a shell, do the following:

```bash
$> make console
docker-compose build
Building app
Step 1/11 : FROM python:3.6.5-stretch
 ---> 4231e6846106
...
...
...
Starting optionpricer_db_1 ... done
Waiting for database at db:5432 ... found
root@ae6009be9d64:/home/option_pricer#>
```

This is a prompt inside the application container. It has access to the database as well as all the necessary packages for the application to run. The `run.sh` script will run the application and the `test.sh` script will run the test suite.

Log output goes to `logs/application.log`

# TODO

## Phase 1: Realtime contract viewer
- Consume realtime IEX market data via websocket client
- Recalculate a single contract in realtime
- Push contract updates to browser via websockets
- 24/7 up-time service

## Phase 2: Application
- CI Builds
- Hosting
- Deployment

## Phase 3: Expanding calculations
- Limit time decay to just market hours and account for holidays
- Calculate implied volatility
- Calculate greeks
- Calculate all strikes in a given expiration
- Calculate all expirations for a given underlying
- Jarrow-Rudd implementation

## Phase 4: User experience
- Pricing sheet per underlying
- Graph vol smile, term structure

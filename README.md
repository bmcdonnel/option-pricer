# Overview
This project is a simple implementation of a binomial option contract pricing model. Currently there is no UI, only CLI.

# Market Data
Pricing information about underlyings is currently using a free HTTP-based API provided by IEX Trading [documentation](https://iextrading.com/developer/docs/#getting-started). This is good enough for now, but it may be worth upgrading to a paid real-time market data stream.

Interest rate information is being pulled from another free HTTP-based API provided by Quandl (see the Treasury Yield Curve example [here](https://www.quandl.com/data/USTREASURY/YIELD-Treasury-Yield-Curve-Rates)).

# Binomial Pricing
There are multiple variants of binomial pricing models, each differing in its definition of the 3 key input variables. The plan for this project is to implement both [Cox-Russ-Rubinstein](http://www.goddardconsulting.ca/option-pricing-binomial-index.html#crr) and [Jarrow-Rudd](http://www.goddardconsulting.ca/option-pricing-binomial-alts.html#jr) variants.

# Developing
Clone this repo and make sure you have Python 3 installed. Then, the `run.sh` script should bootstrap your local environment, install the needed packages, and kick off a calculation.

Example:

```bash
$> ./run.sh --underlying SPY --expiration 2018-04-20 --type C --strike 272.00
```

Currently the only output is in `logs/application.log`:

```bash
$> tail -f logs/application.log
2018-03-19 22:19:01,191 INFO Calculating price for SPY 2018-04-20 272.00 C
2018-03-19 22:19:01,430 INFO Got 124 daily quotes for SPY
2018-03-19 22:19:03,358 INFO Current interest rate: 0.020800
2018-03-19 22:19:03,359 INFO SPY volatility: 0.127482
2018-03-19 22:19:03,359 INFO u: 1.012830, d: 0.987333, p: 0.504972
```

# TODO
- finish Cox-Russ-Rubinstein implementation tree calcs
- Jarrow-Rudd implementation
- GUI for displaying the tree?
- Postgres data store for tracking model runs?

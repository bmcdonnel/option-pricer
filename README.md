# Overview
This project is a simple implementation of a binomial option contract pricing model. Currently there is no UI, only CLI.

# Market Data
Pricing information about underlyings is currently using a free HTTP-based API provided by IEX Trading [documentation](https://iextrading.com/developer/docs/#getting-started). This is good enough for now, but it may be worth upgrading to a paid real-time market data stream.

Interest rate information is being pulled from another free HTTP-based API provided by Quandl (see the Treasury Yield Curve example [here](https://www.quandl.com/data/USTREASURY/YIELD-Treasury-Yield-Curve-Rates)).

# Binomial Pricing
There are multiple variants of binomial pricing models, each differing in its definition of the 3 key input variables. The plan for this project is to implement both [Cox-Russ-Rubinstein](http://www.goddardconsulting.ca/option-pricing-binomial-index.html#crr) and [Jarrow-Rudd](http://www.goddardconsulting.ca/option-pricing-binomial-alts.html#jr) variants.

# Developing
Clone this repo and make sure you have Python 3 installed. Then, the `run.sh` script should bootstrap your local environment and install all the necessary packages.

Example:

```bash
$> ./run.sh --underlying SPY --expiration 2018-04-20 --type C --strike 272.50 --rate 0.0164
```

Currently the only output is in `logs/application.log`:

```bash
$> tail -f logs/application.log
2018-03-18 19:44:30,755 INFO Calculating price for SPY 2018-04-20 272.50 C
2018-03-18 19:44:31,606 INFO Got 100 daily quotes for SPY
2018-03-18 19:44:31,607 INFO SPY volatility: 0.142818
2018-03-18 19:44:31,607 INFO u: 1.014384, d: 0.985820, p: 0.502171
```

# TODO
- More logging
- finish Cox-Russ-Rubinstein implementation tree calcs
- Jarrow-Rudd implementation
- GUI for displaying the tree?
- Postgres data store for tracking model runs?

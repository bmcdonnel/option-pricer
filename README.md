# Overview
This project is a simple implementation of a binomial option contract pricing model. Currently there is no GUI, only CLI.

# Market Data
Pricing information about underlyings is currently using a free HTTP-based API provided by IEX Trading [documentation](https://iextrading.com/developer/docs/#getting-started). This is good enough for now, but it may be worth upgrading to a paid real-time market data stream.

Interest rate information is being pulled from another free HTTP-based API provided by Quandl (see the Treasury Yield Curve example [here](https://www.quandl.com/data/USTREASURY/YIELD-Treasury-Yield-Curve-Rates)).

# Binomial Pricing
There are multiple variants of binomial pricing models, each differing in its definition of the 3 key input variables. The plan for this project is to implement both [Cox-Russ-Rubinstein](http://www.goddardconsulting.ca/option-pricing-binomial-index.html#crr) and [Jarrow-Rudd](http://www.goddardconsulting.ca/option-pricing-binomial-alts.html#jr) variants.

# Developing
Clone this repo and make sure you have Python 3 installed. Then, the `run.sh` script should bootstrap your local environment, install the needed packages, and kick off a calculation.

Example:

```bash
$> ./run.sh --underlying SPY --expiration 2018-04-20 --type C --strike 270.00
SPY 20180420 270.00 C: $1.6133
```

Log output in `logs/application.log`:

```bash
$> tail -f logs/application.log
2018-04-01 21:39:51,686 INFO Calculating price for SPY 2018-04-20 270.00 C
2018-04-01 21:39:51,839 INFO Got 125 daily quotes
2018-04-01 21:39:51,840 INFO SPY volatility: 0.145737
2018-04-01 21:39:53,601 INFO Current interest rate: 0.020900 per year
2018-04-01 21:39:53,601 INFO Days to expiration: 18
2018-04-01 21:39:53,601 INFO Time steps: 100, 0.000718 years/step
2018-04-01 21:39:53,602 INFO Model inputs: u: 1.003913, d: 0.996102, p: 0.500945
2018-04-01 21:39:53,722 INFO Underlying price: $263.150000
2018-04-01 21:39:53,727 INFO Contract price: $1.613319
```

# TODO
- Jarrow-Rudd implementation
- GUI for displaying the tree?
- Postgres data store for tracking model runs?

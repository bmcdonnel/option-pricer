# Overview
This project is a simple implementation of a binomial option contract pricing model. Currently there is no UI, only CLI.

# Market Data
Pricing information about underlyings is currently using a free HTTP-based API provided by Alpha Vantage [documentation](https://www.alphavantage.co/documentation/). This is good enough for now, but it may be worth upgrading to a paid real-time market data stream.

# Binomial Pricing
There are multiple variants of binomial pricing models, each differing in its definition of the 3 key input variables. The plan for this project is to implement both [Cox-Russ-Rubinstein](http://www.goddardconsulting.ca/option-pricing-binomial-index.html#crr) and [Jarrow-Rudd](http://www.goddardconsulting.ca/option-pricing-binomial-alts.html#jr) variants.

# TODO
- More logging
- Cox-Russ-Rubinstein implementation tree calcs
- Jarrow-Rudd implementation
- US Treasury rate API?
- GUI for displaying the tree?
- Postgres data store for tracking model runs?

# Quant-Finance-project
**Modeling "The Smile"**
---

Abstract:
The market does not price options the way Black-Scholes assumes (with constant volatility). Instead, implied volatility varies sharply across strikes (the “smile”). We will construct candidate models, stress test them on volatile market days and by starving them of data, measure model quality with P&L consequences, and compare their results to a baseline Black-Scholes model.

--
Background

Stock options are financial contracts which give the buyer the right to purchase or sell stock at a given price at any time before a given expiration date. A contract granting the right to purchase stock is a "call option",  while a contract bestowing the right to sell is a "put option." Investors who purchase options contracts are most often interested in maximizing the return on their investments, so a common practice is to model the price of an option over time.

One of the most widely used models (albeit, often with minor modifications) is the Black-Scholes model. The Black-Scholes model takes as input parameters the stock price ($S_0$), the fixed purchase/selling price given in the contract ($K$), the risk-free interest rate ($r$), the time to expiration of the contract ($t$), and the volatility of the stock ($\sigma$). Then Black-Scholes outputs the expected price of the option. However, one major drawback of this model is that it assumes that volatility is constant in time. In reality, volatility is a stochastic process, which means that volatility will vary over time, and volatility is the only input of the Black-Scholes model which is not observable from market data. So, one can instead use the market price of an option to "reverse engineer" the volatility from the Black-Scholes model. The volatility which is obtained this way is the "implied volatility." In other words, when the volatility is equal to the implied volatility, the market price will be equal to the predicted output of the Black-Scholes model. If all other input parameters are fixed, then Black-Scholes will yield a single, unique implied volatility.

However, models produced using real-world data indicate a different trend. When plotting strike price ($K$) against the implied volatility (IV), one often observes a curved shape which turns up at both extremes of the range of strike prices, forming a smile. This suggests that the implied volatility is not constant, and that it depends on strike price. Interestingly, this phenomenon emerges not from mathematics, but from real-world options trading behavior. In particular, volatility smiles did not emerge in market data prior to the Crash of 1987. So, adjusting options pricing models to account for implied volatility smiles is a relatively new and still active area of research in quantitative finance. 

-- 
Data & Preparation 




--
Models

The goal of our project was to compare the efficacy of several different models. Each of our models was predicated on the assumption of no arbitrage in an effort to maintain consistency with Black-Scholes and with each other model. The models used are each summarized as follows:

1. Stochastic Volatility Inspired (SVI)
Stochastic Volatility Inspired (SVI) was originally created by Merrill Lynch in 1999 using the principles of the Heston model, and it now has many extensions including SSVI and SVI-JW. Due to its popularity at real-world options desks and its relative simplicity, this model will act as the "baseline" for our project when comparing the performance of other models.  SVI model takes the log-moneyness as its input, which in turn is a function of strike price ($K$) and forward ($F$) where $F = S e^{rt}$. There are multiple parametrizations of SVI, but the most commonly used for its versatility is the raw parametrization:

$$\delta(k) = a + b \left( \rho(k-m) + \sqrt{(k-m)^2 + \sigma^2} \right)$$
In our project, each of the parameters $a$, $b$, $\rho$, $m$, and $\sigma$ (not to be confused with the volatility) are determined by performing a least-squares fit against the implied volatility from the data set.

2. (Uran)


3. (Julius)


4. (Yvonne)


5. (Nico)



--
Analysis & Conclusions


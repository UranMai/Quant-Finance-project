# Quant-Finance-project
**Modeling "The Smile"**
---

Abstract:
The market does not price options the way Black-Scholes assumes (with constant volatility). Instead, implied volatility varies sharply across strikes (the “smile”). We will construct candidate models, stress test them on volatile market days and by starving them of data, measure model quality with P&L consequences, and compare their results to a baseline Black-Scholes model.

---
### Background

Stock options are financial contracts which give the buyer the right to purchase or sell stock at a given price at any time before a given expiration date. A contract granting the right to purchase stock is a "call option",  while a contract bestowing the right to sell is a "put option." Investors who purchase options contracts are most often interested in maximizing the return on their investments, so a common practice is to model the price of an option over time.

One of the most widely used models (albeit, often with minor modifications) is the Black-Scholes model. The Black-Scholes model takes as input parameters the stock price ($S_0$), the fixed purchase/selling price given in the contract ($K$), the risk-free interest rate ($r$), the time to expiration of the contract ($t$), and the volatility of the stock ($\sigma$). Then Black-Scholes outputs the expected price of the option. However, one major drawback of this model is that it assumes that volatility is constant in time. In reality, volatility is a stochastic process, which means that volatility will vary over time, and volatility is the only input of the Black-Scholes model which is not observable from market data. So, one can instead use the market price of an option to "reverse engineer" the volatility from the Black-Scholes model. The volatility which is obtained this way is the "implied volatility." In other words, when the volatility is equal to the implied volatility, the market price will be equal to the predicted output of the Black-Scholes model. If all other input parameters are fixed, then Black-Scholes will yield a single, unique implied volatility.

However, models produced using real-world data indicate a different trend. When plotting strike price ($K$) against the implied volatility (IV), one often observes a curved shape which turns up at both extremes of the range of strike prices, forming a smile. This suggests that the implied volatility is not constant, and that it depends on strike price. Interestingly, this phenomenon emerges not from mathematics, but from real-world options trading behavior. In particular, volatility smiles did not emerge in market data prior to the Crash of 1987. So, adjusting options pricing models to account for implied volatility smiles is a relatively new and still active area of research in quantitative finance. 

--- 
### Data & Preparation 

Due to restrictions on the size of our repository, the data used in this project is linked in a Google Drive folder: [https://drive.google.com/drive/u/0/folders/11Rpz_8LG4-GgNxxLdBaLD-Q2IyWzblP1. ]

The data set consists of end of day options data from the entire 2023 calendar year for AAPL, NVDA, QQQ, SLV, SPX, and TSLA. The original data came from OptionDX.com. Our data cleaning pipeline is included in our repository. Notably, we filtered out "junk" including zero/crossed bids, nonsensical IVs, expiries shorter than ~1 week or longer than a year, time-to-expiry and log-moneyness. 

Each of our models' efficacy will be partially determined by its consistency when starved of data. In particular, the models will be trained using a randomly selected 80% of the cases from a given day. Then, we will compare the model's prediction to the remaining 20% of the data points, called the "holdout" data points. The routine used to randomly split the data into a training set and the remaining holdout set for a given ticker is also included in our repository. 

---
### Models

The goal of our project was to compare the efficacy of several different models. Each of our models was predicated on the assumption of no arbitrage in an effort to maintain consistency with Black-Scholes and with each other model. The models used are each summarized as follows:

1. **Stochastic Volatility Inspired (SVI)** (Aurora)

Stochastic Volatility Inspired (SVI) was originally created by Merrill Lynch in 1999 using the principles of the Heston model, and it now has many extensions including SSVI and SVI-JW. Due to its popularity at real-world options desks and its relative simplicity, this model will act as the "baseline" for our project when comparing the performance of other models.  SVI model takes the log-moneyness as its input, which in turn is a function of strike price ($K$) and forward ($F$) where $F = S e^{rt}$. There are multiple parametrizations of SVI, but the most commonly used for its versatility is the raw parametrization:

$$w(k) = a + b \left( \rho(k-m) + \sqrt{(k-m)^2 + \sigma^2} \right)$$

In our project, each of the parameters $a$, $b$, $\rho$, $m$, and $\sigma$ (not to be confused with the volatility) are determined by performing a least-squares fit against the implied variance ($w = \sigma^2 T$) from the data set. SVI is implemented with greater documentation in `svi.ipynb`.

2. **Heston Stochastic Volatility Model** (Uran)

The Heston model assumes that the underlying asset price and the variance process follows the SDE:

$$dS_t = rS_t dt + \sqrt{v_t}S_t dW_t^S$$
$$dv_t = \kappa(\theta - v_t) dt + \sigma\sqrt{v_t} dW_t^v$$

The two Brownian motions are correlated:  

$$dW_t^S dW_t^v = \rho dt$$

Parameters:    
$v_0$	- Initial variance  
$\kappa$ - Speed of mean reversion  
$\theta$ - Long-run variance  
$\sigma$ - Volatility of variance  
$\rho$ - Correlation between asset and variance shocks  
$\lambda$ - Volatility risk premium  

In our implementation, the volatility risk premium is fixed at: $$\lambda = 0$$. The calibrated parameter vector is therefore: $$\Theta = (v_0, \kappa, \theta, \sigma, \rho)$$. Implementation in file `Heston_model.ipynb`.

3. **Gaussian Process Regression Surface Model** (Julius)

This model treats the implied volatility surface as a nonparametric regression problem on total variance. Let log-moneyness be $k = \log(K/F)$ and time-to-expiry be $\tau$. Rather than fitting IV directly, we model

$$w(k,\tau) = \sigma_{\text{impl}}(k,\tau)^2\,\tau$$

with a Gaussian Process prior:

$$w(\mathbf{x}) \sim \mathcal{GP}\big(m(\mathbf{x}),K(\mathbf{x},\mathbf{x}')\big), \qquad \mathbf{x}=(k,\tau).$$

In implementation, we use a constant-mean GP with a Matern covariance kernel plus a white-noise term, so the model can adapt to both smooth regions and local smile curvature while remaining numerically stable. Conditioning on observed market points gives the posterior mean surface and posterior uncertainty at unseen strikes and maturities. The implied volatility is then recovered as

$$\sigma_{\text{impl}}(k,\tau)=\sqrt{\frac{w(k,\tau)}{\tau}}.$$

At present, arbitrage conditions are checked diagnostically rather than imposed as hard constraints during training. The primary advantage of this approach is that it fits a probability distribution, rather than a single point esimate. This allows for uncertainty quantification and error bounds, which could inform decision making in practice. Implementation in `Gaussian_process.ipynb`.

4. **Deep Smoothing By Neural Network** (For no Arbitrage) (Yvonne)
Reproduced results from “Deep Smoothing of the Implied Volatility Surface” by Ackerer et al, performed a model risk study of implied volatility surface construction. Compared a classical parametric method (SVI), a plain neural network, and a no-arbitrage-constrained neural network (deep smoothing) on real SPX options on 2023-12-29.

Findings: 
- On fit (RMSE), SVI wins, it posts the lowest reconstruction error.
- But it does not require no-arbitrage, violating marketing principle. Similarly for the unconstrained vanilla NN, while it fits well, fits a surfaces that violate the butterfly no-arbitrage condition. 
- Deep smoothing’s no-arbitrage penalty term in the lose function drives the butterfly violation towards zero, at a small cost to RMSE cost. 

Detailed results in slides: https://docs.google.com/presentation/d/1Z2kijoJG47XhLJ9XLKOpwQzBNL_0fSX6K9suzaW-Lks/edit?slide=id.g3f7e755a775_1_0#slide=id.g3f7e755a775_1_0. Implementation in file `SmoothingbyNeuralNetwork.ipynb`

6. **Risk-Neutral Density Mixture (Bahra)** (Nico)

Instead of parametrizing the smile (SVI) or the price dynamics (Heston), this model parametrizes the **risk-neutral probability distribution itself**. By Breeden–Litzenberger, the density is the second strike-derivative of the call price (up to discounting), so a valid model must never imply negative probabilities ("butterfly arbitrage"). We therefore model the normalized underlying $x = S_T/F$ per expiry as a mixture of $M=3$ lognormals — component $i$ lognormal with **mean** $m_i$ and log-standard-deviation $s_i$ (so $m_i$ is $\mathbb E[x_i]$ itself, *not* the log-mean) — with the means free but rescaled so the forward is repriced *exactly*:

$$g_x(x) = \sum_{i=1}^{M}\pi_i \mathrm{LN}(x;\ m_i,\ s_i), \qquad \pi_i \ge 0,\quad \sum_i \pi_i = 1, \quad \mathbb E[x] = \sum_i \pi_i m_i = 1 .$$

Non-negativity of the density (no butterfly arbitrage) and the forward condition then hold **by construction** rather than by penalty or post-hoc check. Prices are closed-form — with $k = \log(K/F)$ the log-moneyness and $N$ the standard normal CDF, the normalized call $c = C/(e^{-rT}F)$ is

$$c(k) = \sum_{i=1}^{M}\pi_i\Big[ m_i N(d_{1,i}) - e^{k} N(d_{2,i}) \Big], \qquad d_{1,i} = \frac{\log m_i - k + s_i^2/2}{s_i}, \quad d_{2,i} = d_{1,i} - s_i$$

(no quadrature anywhere; at $m_i \equiv 1$ each term is plain Black–Scholes). The implied-volatility smile is recovered afterwards by inverting Black–Scholes in total variance, which is well-posed because that price is strictly increasing in total variance. Calibration is spread-weighted least squares per expiry on the visible 80% of each day. A small theorem motivates the free means: any *unit-mean* lognormal mixture satisfies put–call symmetry, forcing an exactly symmetric smile with zero skew for every $M$ — so freeing the (mean-corrected) means is precisely what makes equity skew representable. Implementation, holdout evaluation, a monthly robustness sweep with parameter-stability tracking, spread-noise uncertainty bands, and butterfly/calendar arbitrage checks with a certified calendar repair are in `Bahra_mixture_model.ipynb`.


--
### Analysis & Conclusions
To quantify the performance of each of the models in the previous section, we first verified how well each model fit the 20% of held out cases using a RMSE calculation. In addition, each model was trained and designed with an assumption of static-arbitrage, but we check how well each model conforms to this assumption by measuring butterfly arbitrage and calendar arbitrage violations, both from the market data set and from the model's results. A summary of our results follows: 

| Model Name | RMSE IV | Butterfly Violations | Calendar Violations | 
|------------|---------|----------------------|---------------------| 
| SVI        |  0.0497  |                      |         0            |  
| Heston     |  0.0183  |         0            |         0            |  
| Gaussian   |  0.00271    |       24               |          0           | 
| NN         |  0.0237  |            0          |          0           |  
| Bahra      |         |                      |                     |  

Further results may be found in each model's `.ipynb` file and/or in the slides deck linked at https://docs.google.com/presentation/d/1Z2kijoJG47XhLJ9XLKOpwQzBNL_0fSX6K9suzaW-Lks/edit?slide=id.g3f7e755a775_1_0#slide=id.g3f7e755a775_1_0 

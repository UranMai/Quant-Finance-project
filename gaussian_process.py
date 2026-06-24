import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, RBF, WhiteKernel, Matern
from sklearn.preprocessing import StandardScaler

"""
This script chooses a random ticker and date, then fits a 
Gaussian process to the implied volatility surface. 
Notes:
    - There is not yet any enforcement of no-arbitrage
    - The model learns total variance as a function of log-moneyness and 
        time-to-expiration. Implied volatility is recovered analytically:
            iv = sqrt(total_var / tau)
    - At the moment, most hyperparameters are chosen arbitrarily. We will wait 
        to tune hyperparameters until after no-arbitrage is enforced
"""


if "axes3d.mouserotationstyle" in plt.rcParams:
    plt.rcParams["axes3d.mouserotationstyle"] = "azel"

df = pd.read_parquet("Processed_data/surface_test.parquet")

ticker_date_combos = list(df.groupby(["ticker", "quote_date"]).size().index)
random_index = np.random.default_rng(1234).integers(len(ticker_date_combos))
ticker, date = ticker_date_combos[random_index]

surface_all_df = df[(df["ticker"] == ticker) & (df["quote_date"] == date)]

surface_df = surface_all_df.sample(50, random_state=0)
surface_compare_df = surface_all_df.drop(surface_df.index)

X = np.column_stack([
    surface_df["log_moneyness"].to_numpy(),
    surface_df["tau"].to_numpy()
])
y = surface_df["total_var"].to_numpy()
x_scaler = StandardScaler()
y_scaler = StandardScaler()
Xs = x_scaler.fit_transform(X)
ys = y_scaler.fit_transform(y.reshape(-1, 1)).ravel()

kernel = (
    ConstantKernel(1.0, (1e-3, 1e3))
    * RBF(length_scale=[1.0, 1.0], length_scale_bounds=(1e-3, 1e3))
    + WhiteKernel(noise_level=1e-4, noise_level_bounds=(1e-8, 1e-1))
)
gp = GaussianProcessRegressor(
    kernel=kernel,
    normalize_y=False,
    random_state=0
)
gp.fit(Xs, ys)

lm = np.linspace(surface_all_df["log_moneyness"].min(), surface_all_df["log_moneyness"].max(), 60)
tt = np.linspace(surface_all_df["tau"].min(), surface_all_df["tau"].max(), 60)
LM, TT = np.meshgrid(lm, tt)
Xg = np.column_stack([LM.ravel(), TT.ravel()])
Xg_s = x_scaler.transform(Xg)

pred = gp.predict(Xg_s, return_std=True)
mu_s, sigma_s = pred[0], pred[1]
mu = y_scaler.inverse_transform(mu_s.reshape(-1, 1)).ravel()
sigma = sigma_s * y_scaler.scale_[0] # type: ignore

MU = mu.reshape(LM.shape)
SIGMA = sigma.reshape(LM.shape)

iv_from_mu = np.sqrt(MU / TT)

fig = plt.figure(figsize=(14, 6))
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax2 = fig.add_subplot(1, 2, 2, projection="3d")
for i in range(2):
    ax = [ax1, ax2][i]
    predictions = [MU, iv_from_mu][i]
    z_axis_quantity = ["total_var", "iv"][i]
    surf = ax.plot_wireframe(
        LM, TT, predictions,
        rstride=3, cstride=3,
        color="black",
        linewidth=0.8,
        alpha=0.75,
    )
    ax.scatter(
        surface_compare_df["log_moneyness"],
        surface_compare_df["tau"],
        surface_compare_df[z_axis_quantity],
        color="tab:blue",
        s=14,
        alpha=0.7,
        depthshade=True,
        label="Held-out observations",
    )
    ax.scatter(
        surface_df["log_moneyness"],
        surface_df["tau"],
        surface_df[z_axis_quantity],
        color="red",
        s=30,
        alpha=0.9,
        depthshade=False,
        label="Training observations",
    )
    ax.set_xlabel("Log Moneyness")
    ax.set_ylabel("Time to Expiration (tau)")
    ax.legend(loc="upper left")
ax1.set_zlabel("Implied Total Variance")
ax1.set_title("Implied Total Variance Surface")
ax2.set_zlabel("Implied Volatility")
ax2.set_title("Implied Volatility Surface")
plt.suptitle(f"GP Fit + Observations: {ticker} ({date})")
plt.tight_layout()
plt.show()

weird_examples = [
    ("SLV", "2023-11-08")
]
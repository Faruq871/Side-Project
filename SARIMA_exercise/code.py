path = "cv_train.csv"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math, warnings
import numpy.linalg as la
import matplotlib; matplotlib.use("Agg")
from datetime import datetime, timedelta
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

H           = 12
START_TRAIN = "2010-01-01"   
W_PROFILE   = 5              # weighted model to 5 years later
PHI         = 0.8            # damping tren baseline
AMP_CAP     = 1.0            # margin extrapolation of growth (1.0 = level 2025)
EDGES       = (-45, -30, -15, 0, 15, 30, 45, 60) # slice month to group of day

df = pd.read_csv(path)
df["month"] = pd.to_datetime(df["month"], format="%m/%d/%Y")
y = df.set_index("month")["search"].astype(float).asfreq("MS")
assert y.notna().all(), "ada bulan yang hilang di data"
print(f"data: {len(y)} bulan, {y.index.min():%Y-%m} s.d. {y.index.max():%Y-%m}")

# ---------- 2. Hijirah Calendar ----------
def hijri_to_greg(yh, mh, dh):
    jd = dh + math.ceil(29.5*(mh-1)) + (yh-1)*354 + math.floor((3+11*yh)/30) + 1948439.5
    return pd.Timestamp(datetime(1970, 1, 1) + timedelta(days=float(jd - 2440587.5)))

ramadhan = {h: hijri_to_greg(h, 9, 1) for h in range(1420, 1460)}

def phase_features(idx, edges=EDGES):
    """the fraction of a day within a month that falls into each day-interval bin, measured from the beginning of ramadhan"""
    rows = []
    for m in idx:
        days = pd.date_range(m, m + pd.offsets.MonthEnd(1), freq="D")
        v = np.zeros(len(edges)-1)
        for rs in ramadhan.values():
            rel = (days - rs).days.values
            for k in range(len(edges)-1):
                v[k] += ((rel >= edges[k]) & (rel < edges[k+1])).sum()
        rows.append(v / len(days))
    cols = [f"p{edges[k]}_{edges[k+1]}" for k in range(len(edges)-1)]
    return pd.DataFrame(rows, index=idx, columns=cols)

FULL = pd.date_range(y.index.min(), y.index.max() + pd.offsets.MonthBegin(H), freq="MS")
X    = phase_features(FULL)
FUT  = X.loc[y.index.max() + pd.offsets.MonthBegin(1):]
AFFECTED = (X.sum(axis=1) > 0)

# ---------- 3. model ----------
def m_snaive(tr, h, xf):
    return np.array([tr.iloc[len(tr)-h + i % h] for i in range(h)], dtype=float)

def m_sarima(tr, h, xf):
    """baseline: seasonalitas Masehi is still same"""
    z = np.log1p(tr.loc["2007-01-01":])
    r = SARIMAX(z, order=(0,1,1), seasonal_order=(0,1,1,12),
                enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
    return np.expm1(r.forecast(h).values)

def m_hijri_amp(tr, h, xf):
    """SARIMAX log + Hijri phase + time interaction (peak amplitude grows, capped)"""
    z = np.log1p(tr.loc[START_TRAIN:]); Xt = X.loc[z.index]
    sc = lambda idx: np.asarray((idx - pd.Timestamp("2015-01-01")).days / 3652.5)
    A  = Xt.values * sc(Xt.index)[:, None]
    Af = np.minimum(xf.values * sc(xf.index)[:, None], AMP_CAP * xf.values)
    r = SARIMAX(z, exog=np.column_stack([Xt.values, A]), order=(0,1,1),
                enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
    return np.expm1(r.forecast(h, exog=np.column_stack([xf.values, Af])).values)

def m_hijri_profile(tr, h, xf):
    """log(y) = year-effect + beta*phase; beta is derived from the last W years,
       baseline is extrapolated using a damped trend"""
    z = np.log1p(tr); z = z[z.index >= tr.index.max() - pd.DateOffset(years=W_PROFILE-1)]
    Xu = X.loc[z.index]; uy = np.sort(np.unique(z.index.year.values))
    D  = pd.get_dummies(pd.Categorical(z.index.year.values, categories=uy)).values.astype(float)
    A  = np.column_stack([D, Xu.values])
    coef = la.solve(A.T@A + 1e-6*np.eye(A.shape[1]), A.T@z.values)
    beta = coef[len(uy):]
    base = pd.Series(z.values - Xu.values@beta, index=z.index)
    bt   = base[base.index >= base.index.max() - pd.DateOffset(years=4)]
    slope, intercept = np.polyfit(np.arange(len(bt)), bt.values, 1)
    anchor = intercept + slope*(len(bt)-1)
    out = []
    for i, m in enumerate(xf.index, start=1):
        lvl = anchor + slope*sum(PHI**j for j in range(1, i+1))
        out.append(max(np.expm1(lvl + xf.loc[m].values @ beta), 0.0))
    return np.array(out)

models = {"SeasonalNaive": m_snaive, "SARIMA_m12": m_sarima,
          "Hijri+amplitudo": m_hijri_amp, "Hijri+profil": m_hijri_profile}
def m_ensemble(tr, h, xf):
    return 0.5*m_hijri_amp(tr, h, xf) + 0.5*m_hijri_profile(tr, h, xf)
models["Ensemble (2 Hijiri)"] = m_ensemble

# ---------- 4. backtest rolling-origin ----------
ORIGINS = ["2019-12","2020-12","2021-12","2022-12","2023-12","2024-12"]
rows, err_store = [], {}
for name, f in models.items():
    E, EL, PK, AF = [], [], [], []
    for end in ORIGINS:
        tr = y.loc[:end]
        te = y.loc[end:].iloc[1:H+1]
        p  = f(tr, H, X.loc[te.index])
        e  = p - te.values
        E.append(e); EL.append(np.log1p(p) - np.log1p(te.values))
        PK.append(e[np.argmax(te.values)]); AF.append(AFFECTED.loc[te.index].values)
    E, EL, AF = np.array(E), np.array(EL), np.array(AF)
    rows.append({"model": name, "MAE": np.abs(E).mean(), "RMSE": np.sqrt((E**2).mean()),
                 "bias_bulan_puncak": np.mean(PK)})
    err_store[name] = (EL, AF)
print("\n=== BACKTEST (out-of-sample, 72 titik) ===")
print(pd.DataFrame(rows).round(2).sort_values("MAE").to_string(index=False))

# ---------- 5. forecast final + interval 80% empiris ----------
final_res = "Ensemble (2 Hijiri)"
pred = m_ensemble(y, H, FUT)
EL, AF = err_store[final_res]
qr = np.percentile(EL[AF], [10, 90]); qn = np.percentile(EL[~AF], [10, 90])
af = AFFECTED.loc[FUT.index].values
lo = np.expm1(np.log1p(pred) - np.where(af, qr[1], qn[1]))
hi = np.expm1(np.log1p(pred) - np.where(af, qr[0], qn[0]))
fc = pd.DataFrame({"forecast": pred.round(3), "lo80": np.maximum(lo,0).round(1),"hi80": hi.round(1)}, index=FUT.index.strftime("%Y-%m"))
fc.index.name = "month"
print("\n Forecast ")
print(fc.to_string())
for name, f in models.items():
    fc[name] = np.round(f(y, H, FUT), 1)

# ---------- 6. plot ----------
fig, ax = plt.subplots(figsize=(13,5))
ax.plot(y.index, y.values, label="aktual", lw=1.2)
ax.plot(FUT.index, pred, "o-", color="crimson", label="forecast ensemble")
ax.fill_between(FUT.index, np.maximum(lo,0), hi, color="crimson", alpha=.15, label="interval 80%")
ax.set_title("Search index monthly + forecast 12 month")
ax.legend()
fig.tight_layout()

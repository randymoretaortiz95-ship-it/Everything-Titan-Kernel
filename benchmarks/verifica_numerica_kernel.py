"""Verifica numerica delle correzioni al Kernel (Titan Research Labs).
Ogni test controlla UNA affermazione del documento corretto. I test 27 (benchmark) sono su dati sintetici."""
import numpy as np, zlib

rng = np.random.default_rng(0)
out = []
def rep(n, titolo, esito, dettaglio):
    out.append((n, titolo, esito, dettaglio))

# --- 2: soglia di passo per l'Eulero esplicito con resistenza quadratica --------------
c, v0 = 0.5, 10.0            # c = rho*A*Cd/(2m)
res = []
for a in (0.9, 1.5, 2.5):    # a = c*dt*v0
    dt = a/(c*v0); v = v0; flips = 0; vmax = abs(v)
    for _ in range(300):
        vn = v - c*dt*abs(v)*v
        flips += (np.sign(vn) != np.sign(v)) and vn != 0
        v = vn; vmax = max(vmax, abs(v))
        if vmax > 1e12: break
    res.append((a, int(flips), vmax, abs(v)))
rep(2, "Eulero + resistenza quadratica", "RETTIFICA",
    "a=c·dt·v0: " + "; ".join(f"a={a}: inversioni={f}, |v|max={m:.3g}" for a, f, m, _ in res)
    + " -> a<1 decadimento monotono; 1<a<2 inversione di segno poi converge; a>2 diverge")

# --- 4: RK4 non conserva l'energia; leapfrog sì ---------------------------------------
dt, steps = 0.5, 2000
def f(s): return np.array([s[1], -s[0]])
s = np.array([1.0, 0.0])
for _ in range(steps):
    k1 = f(s); k2 = f(s+dt/2*k1); k3 = f(s+dt/2*k2); k4 = f(s+dt*k3)
    s = s + dt/6*(k1+2*k2+2*k3+k4)
E_rk4 = 0.5*(s@s)/0.5
x, v = 1.0, 0.0; Emax = 0; Emin = 9
for _ in range(steps):
    v -= 0.5*dt*x; x += dt*v; v -= 0.5*dt*x
    E = 0.5*(v*v + x*x)/0.5; Emax = max(Emax, E); Emin = min(Emin, E)
rep(4, "RK4 vs leapfrog (energia)", "CONFERMATO",
    f"E_RK4(T)/E0 = {E_rk4:.3f} (dissipa); leapfrog resta in [{Emin:.3f}, {Emax:.3f}]")

# --- 6: integrale chiuso, t_crit di soglia, esplosione superlineare --------------------
mu, g, tmax = 1.0, 0.5, 10.0
tc = np.log(1 + g*tmax/mu)/g
t = np.linspace(0, 6, 600001); tau = np.cumsum(mu*np.exp(g*t))*(t[1]-t[0])
idx = np.argmax(tau >= tmax)
closed = mu/g*(np.exp(g*t[idx])-1)
dt = 1e-4; y = 1.0; tt = 0.0
while tt < 0.9: y += dt*y*y; tt += dt
rep(6, "τ_S: integrale, t_crit, blow-up", "CONFERMATO",
    f"t_crit formula={tc:.4f}, numerico={t[idx]:.4f}; chiusa vs numerica={closed:.3f}; "
    f"dτ/dt=τ²: τ(0.9)≈{y:.2f} (analitica 10) e t_crit=1/(kτ0)=1")

# --- 9: scala r^-4 ---------------------------------------------------------------------
rep(9, "Poiseuille R ∝ r⁻⁴", "CONFERMATO", f"R(r/2)/R(r) = {(1/(0.5)**4):.0f}")

# --- 10: sostenibilità del debito ------------------------------------------------------
r_, g_, pb = 0.05, 0.02, 0.02
dstar = pb*(1+g_)/(r_-g_)
def run(d0, n=100):
    d = d0
    for _ in range(n): d = d*(1+r_)/(1+g_) - pb
    return d
rep(10, "Debito: d0 ≤ pb(1+g)/(r−g)", "CONFERMATO",
    f"d*={dstar:.3f}; d0=0.67 -> d(100)={run(0.67):.3f} (cala); d0=0.69 -> d(100)={run(0.69):.1f} (esplode)")

# --- 12: Poiseuille è laminare ma non irrotazionale -----------------------------------
R_, U = 1.0, 1.0; r = np.linspace(0, R_, 1001); u = U*(1-(r/R_)**2)
w = -np.gradient(u, r)
rep(12, "Flusso laminare con rotore ≠ 0", "CONFERMATO", f"|ω| a r=R/2: {abs(w[500]):.3f} (≠ 0)")

# --- 15: hashing spaziale: confronti di coppie -----------------------------------------
def checks(N):
    rad = (10/(N*4.18879))**(1/3); P = rng.random((N, 3)); cell = {}
    key = lambda p: tuple((p/rad).astype(int))
    for i, p in enumerate(P): cell.setdefault(key(p), []).append(i)
    tot = 0
    for kx, lst in cell.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    tot += len(lst)*len(cell.get((kx[0]+dx, kx[1]+dy, kx[2]+dz), []))
    return tot/2, N*(N-1)/2
rows = [(N, *checks(N)) for N in (500, 2000, 8000)]
rep(15, "Spatial hash: costo coppie", "CONFERMATO",
    "; ".join(f"N={N}: hash/N={h/N:.0f}, brute/N={b/N:.0f}" for N, h, b in rows))

# --- 19: accumulatore di fase: quantizzazione e aliasing -------------------------------
fs = 48000; n = np.arange(fs)
def synth(f): return np.sin(np.cumsum(np.full(fs, 2*np.pi*f/fs)))
y = synth(1000.0); q = np.round(y*32767)/32767
snr = 10*np.log10(np.mean(y**2)/np.mean((q-y)**2))
sp = np.abs(np.fft.rfft(synth(30000.0))); pk = np.argmax(sp)*fs/len(n)
rep(19, "Sintesi: quantizzazione e aliasing", "CONFERMATO",
    f"16 bit: SNR={snr:.1f} dB (rumore ≠ 0); f=30 kHz con fs=48 kHz appare a {pk:.0f} Hz")

# --- 22: ottimo interno nel compromesso bias–varianza ----------------------------------
x = rng.random(30); y = np.sin(2*np.pi*x) + 0.3*rng.standard_normal(30)
xt = np.linspace(0, 1, 500); yt = np.sin(2*np.pi*xt)
feat = lambda z: np.vander(z, 12, increasing=True)
X, Xt = feat(x), feat(xt)
errs = []
for lam in 10.0**np.arange(-8, 5):
    wts = np.linalg.solve(X.T@X + lam*np.eye(12), X.T@y)
    errs.append((lam, np.mean((X@wts-y)**2), np.mean((Xt@wts-yt)**2)))
best = min(errs, key=lambda e: e[2])
rep(22, "Ottimo interno (ridge)", "CONFERMATO",
    f"errore test: λ=1e-8 -> {errs[0][2]:.3f}; ottimo λ={best[0]:.0e} -> {best[2]:.3f}; λ=1e4 -> {errs[-1][2]:.3f}")

# --- 23: potenza massima vs rendimento --------------------------------------------------
Rs, Xs = 1.0, 2.0
RL = np.logspace(-2, 2, 2001); I = 1/(Rs+RL)
P = 0.5*I**2*RL; eta = RL/(RL+Rs); k = np.argmax(P)
rep(23, "Adattamento d'impedenza", "CONFERMATO",
    f"P max a R_L={RL[k]:.2f} (=R_s), rendimento {eta[k]:.2f}; a R_L=100: rendimento {eta[-1]:.3f}, P={P[-1]/P[k]:.2f}·Pmax")

# --- 24: taratura k = 2ζ√(kp/m) ----------------------------------------------------------
kp, m = 20.0, 1.0; zeta = 0.707; k = 2*zeta*np.sqrt(kp/m)
p_ = np.roots([1, k, kp/m]); z_meas = -p_[0].real/abs(p_[0])
rep(24, "Taratura dello smorzamento", "CONFERMATO", f"k={k:.2f} 1/s -> ζ misurato dai poli = {z_meas:.3f}")

# --- 25: continuità C¹ del termine con Heaviside ---------------------------------------
al, s0, h = 0.01, 50.0, 1e-4
F = lambda u: 1 + al*(u > s0)*(u-s0)**2
d1l = (F(s0)-F(s0-h))/h; d1r = (F(s0+h)-F(s0))/h
d2l = (F(s0)-2*F(s0-h)+F(s0-2*h))/h**2; d2r = (F(s0+2*h)-2*F(s0+h)+F(s0))/h**2
rep(25, "Heaviside·quadrato è C¹", "CONFERMATO",
    f"salto di F: {F(s0+1e-9)-F(s0):.1e}; pendenza sx/dx: {d1l:.1e}/{d1r:.1e}; curvatura sx/dx: {d2l:.2f}/{d2r:.2f} (=2α)")

# --- 26: derivare due volte amplifica il rumore ----------------------------------------
sig, dt = 1e-3, 0.01
pos = sig*rng.standard_normal(200000)
acc = (pos[2:]-2*pos[1:-1]+pos[:-2])/dt**2
rep(26, "Rumore sulla doppia derivata", "CONFERMATO",
    f"σ_pos={sig*1e3:.0f} mm -> σ_acc={acc.std():.1f} m/s² (attesa σ·√6/dt²={sig*np.sqrt(6)/dt**2:.1f})")

# --- 7: forma integrale = ricorsione del filtro ----------------------------------------
gam, dt = 2.0, 1e-3; tt = np.arange(0, 5, dt); d = np.sin(3*tt)+0.5*np.sign(np.sin(0.7*tt))
Wn = np.zeros_like(tt); a = np.exp(-gam*dt)
for i in range(1, len(tt)): Wn[i] = a*Wn[i-1] + dt*d[i-1]
tg = tt[-1]; Wi = np.sum(d*np.exp(-gam*(tg-tt)))*dt
rep(7, "Wake memory = filtro 1° ordine", "CONFERMATO", f"W(T) integrale={Wi:.4f}, ricorsione={Wn[-1]:.4f}")

# --- 27: benchmark sintetico del guardrail ---------------------------------------------
sn = 0.01; ok = sn*rng.standard_normal(20000); bad = sn*rng.standard_normal(20000)+rng.choice([-1, 1], 20000)*np.abs(0.04*rng.standard_normal(20000))
cols = []
for eps in (0.02, 0.03, 0.05, 0.1):
    cols.append(f"ε={eps}: falsi rigetti={np.mean(abs(ok)>eps):.1%}, violazioni mancate={np.mean(abs(bad)<=eps):.1%}")
rep(27, "Guardrail: compromesso su ε (SINTETICO)", "ILLUSTRATIVO", "; ".join(cols))

# --- 28: complessità apparente vs descrizione generatrice ------------------------------
def rule110(N, W=700):
    row = np.zeros(W, np.uint8); row[W//2] = 1; rows = [row.copy()]
    for _ in range(N-1):
        l, r_ = np.roll(row, 1), np.roll(row, -1)
        row = ((110 >> (4*l + 2*row + r_)) & 1).astype(np.uint8)   # regola 110
        rows.append(row.copy())
    return np.packbits(np.array(rows))
sz = {N: len(zlib.compress(rule110(N).tobytes(), 9)) for N in (64, 128, 256, 512)}
rep(28, "Complessità apparente vs descrizione", "CONFERMATO",
    "dimensione zlib dello stato: " + ", ".join(f"N={N}: {b} B" for N, b in sz.items())
    + f"; descrizione generatrice (seme + regola + N): {len('rule110;seed=centre;N=512')} B")

for n, titolo, esito, det in sorted(out):
    print(f"[{n:>2}] {titolo} — {esito}\n     {det}")

import numpy as np
import matplotlib.pyplot as plt
from scipy import special


def mauclarin_vrsti(x):
    epsilon = 1e-10
    alpha = 0.355028053887817239  # alpha = Ai(0) = Bi(0)/3^(1/2)
    beta = 0.258819403792806798  # beta = Bi'(0)/3^(1/2) = -Ai'(0)

    # MACLAURINOVI VRSTI
    ai_m = alpha - beta * x
    bi_m = np.sqrt(3) * (alpha + beta * x)
    i = 1.
    f = 1.
    g = x
    val_aim = 1.
    val_bim = 1.
    ai_oldm = float("inf")
    bi_oldm = float("inf")
    stopnja = 0

    #   1. NAČIN
    while np.abs(ai_m - ai_oldm) >= epsilon or np.abs(bi_m - bi_oldm) >= epsilon:

        ai_oldm = ai_m
        bi_oldm = bi_m
        f = f * (x ** (3.) * 3. * ((1. / 3.) + i - 1)) / \
            ((3. * (i - 1.) + 3.) * (3. * (i - 1.) + 2.) * (3. * (i - 1.) + 1.))
        g = g * (x ** (3.) * 3. * ((2. / 3.) + i - 1.)) / \
            ((3. * (i - 1.) + 4.) * (3. * (i - 1.) + 3.) * (3. * (i - 1.) + 2.))
        val_aim = alpha * f - beta * g
        val_bim = np.sqrt(3) * (alpha * f + beta * g)
        ai_m = ai_m + val_aim
        bi_m = bi_m + val_bim

        i += 1

    return ai_m, bi_m


def asimptotski_razvoj(a):
    ksi = (2. / 3.) * (np.abs(a) ** (3. / 2.))
    epsilon = 1e-2
    i = 1.
    L = 1.
    P = 1.
    Q = (2. + 0.5) * (1. + 0.5) / (54. * ksi)
    val_aia = 1.
    val_bia = 1.
    ai_oldar = float("inf")
    bi_oldar = float("inf")
    if (a >= 0.):
        p1_ai = np.exp(-ksi) / (2. * np.pi ** 0.5 * a ** 0.25)
        p1_bi = np.exp(ksi) / (np.pi ** 0.5 * a ** 0.25)
        ai_ar = p1_ai
        bi_ar = p1_bi

        while np.abs(ai_ar - ai_oldar) >= epsilon or np.abs(bi_ar - bi_oldar) >= epsilon:
            ai_oldar = ai_ar
            bi_oldar = bi_ar
            # asimptotski razvoj za velike a>0
            L = L * (3. * (i - 1.) + 5. / 2.) * \
                (3. * (i - 1.) + 3. / 2.) * \
                (3. * (i - 1.) + 1. / 2.) / (54 * i * (i - 0.5) * ksi)
            val_aia = p1_ai * (-1) ** i * L
            val_bia = p1_bi * L
            ai_ar = ai_ar + val_aia
            bi_ar = bi_ar + val_bia
            i = i + 1.

    # asimptotski razvoj za velike |a|
    if (a < 0):
        p2 = 1. / (np.pi ** 0.5 * (-a) ** 0.25)
        ai_ar = p2 * (np.sin(ksi - np.pi / 4.) * Q + np.cos(ksi - np.pi / 4.) * P)
        bi_ar = p2 * (-np.sin(ksi - np.pi / 4.) * P + np.cos(ksi - np.pi / 4.) * Q)

        while np.abs(ai_ar - ai_oldar) >= epsilon or np.abs(bi_ar - bi_oldar) >= epsilon:
            ai_oldar = ai_ar
            bi_oldar = bi_ar
            # asimptotski razvoj za velike |a|
            P = P * (-1.) * (6. * (i - 1.) + 11. / 2.) * (6. * (i - 1.) + 9. / 2.) * \
                (6. * (i - 1.) + 7. / 2.) * (6. * (i - 1.) + 5. / 2.) * \
                (6. * (i - 1.) + 3. / 2.) * (6. * (i - 1.) + 1. / 2.) / \
                (54. ** 2. * 2. * i * (2. * i - 1.) * (2. * (i - 1.) + 3. / 2.) *
                 (2. * (i - 1.) + 1. / 2.) * ksi ** 2.)
            Q = Q * (-1.) * (6. * (i - 1.) + 17. / 2.) * (6. * (i - 1.) + 15. / 2.) * \
                (6. * (i - 1.) + 13. / 2.) * (6. * (i - 1.) + 11. / 2.) * \
                (6. * (i - 1.) + 9. / 2.) * (6. * (i - 1.) + 7. / 2.) / \
                (54. ** 2. * (2. * i + 1.) * 2. * i * (2. * (i - 1.) + 5. / 2.) *
                 (2. * (i - 1.) + 3. / 2.) * ksi ** 2.)
            val_aia = p2 * (np.sin(ksi - np.pi / 4.) * Q + np.cos(ksi - np.pi / 4.) * P)
            val_bia = p2 * (-np.sin(ksi - np.pi / 4.) * P + np.cos(ksi - np.pi / 4.) * Q)
            ai_ar = ai_ar + val_aia
            bi_ar = bi_ar + val_bia
            i = i + 1.
    return ai_ar, bi_ar



def Ai_funkcija(a):
    if -6.66666666667 <= a < 5.20202020202:
        return mauclarin_vrsti(a)[0]
    else:
        return asimptotski_razvoj(a)[0]



def Bi_funkcija(a):
    if -6.666666667 <= a < 5.20202020202:
        return mauclarin_vrsti(a)[1]
    else:
        return asimptotski_razvoj(a)[1]




x0 = np.linspace(-50., 30., 1000)
ai = np.zeros(1000)
bi = np.zeros(1000)
aiv, aivp, biv, bivp = special.airy(x0)

M= 1000
x1 = np.linspace(-15., 15., M)
aim, bim = np.zeros(M),np.zeros(M)
for t in range(M):
    aim[t] = mauclarin_vrsti(x1[t])[0]
    bim[t] = mauclarin_vrsti(x1[t])[1]

plt.plot(x1, aim, '-', label='$Ai(x)$')
plt.plot(x1, bim, '-', label='$Bi(x)$')
plt.ylim(-1,1.5)
plt.xlabel("x")
plt.ylabel("y")
plt.show()


for t in range(1000):
    ai[t] = Ai_funkcija(x0[t])
    bi[t] = Bi_funkcija(x0[t])
    # print (np.abs(bi[t] - biv[t]), x0[t])

# plt.plot(x0, np.abs(aim - aiv), label='$|Ai(x) - Ai_v(x)|$')
# plt.plot(x0, np.abs(bim - biv), label='$|Bi(x) - Bi_v(x)|$')
# plt.yscale("log")
plt.plot(x0, ai, '-', label='$Ai(x)$')
plt.plot(x0, bi, '-', label='$Bi(x)$')
plt.ylim(-1, 2)
plt.xlim(-25, 15)
plt.xlabel("x")
plt.ylabel("y")
# plt.axhline(y=0,color='0', linewidth=0.5, linestyle=':')
# plt.axvline(x=0, color='0', linewidth=0.5, linestyle=':')
plt.legend()

# plt.savefig('Ai_Bi.pdf')
plt.show()
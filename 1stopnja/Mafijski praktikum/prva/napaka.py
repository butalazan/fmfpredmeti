import numpy as np
from scipy import special
from decimal import *

alpha = 0.355028053887817239  # alpha = Ai(0) = Bi(0)/3^(1/2)
beta = 0.258819403792806798  # beta = Bi'(0)/3^(1/2) = -Ai'(0)
epsilon = 1e-10

M = 1000
x0 = np.linspace(-15., 15., M)
ai_maclaurin = np.zeros(M)
bi_maclaurin = np.zeros(M)
ai_asimptot = np.zeros(M)
bi_asimptot = np.zeros(M)
ai, aip, bi, bip = special.airy(x0)
j = 0

for x in x0:
    w, = np.where(x0 == x)[0]
    ksi = (2. / 3.) * (np.abs(x) ** (3. / 2.))
    # Maclaurinovi vrsti
    ai_m = alpha - beta * x
    bi_m = 3. ** 0.5 * (alpha + beta * x)
    i = 1.
    f = 1.
    g = x
    val_aim = 1.  # vrednosti, ki jih pristevamo
    val_bim = 1.  # vrednosti, ki jih pristevamo
    L = 1.
    P = 1.
    Q = (2. + 0.5) * (1. + 0.5) / (54. * ksi)
    val_aia = 1.  # vrednosti, ki jih pristevamo
    val_bia = 1.  # vrednosti, ki jih pristevamo
    ai_oldm = float("inf")
    bi_oldm = float("inf")
    ai_oldar = float("inf")
    bi_oldar = float("inf")

    if (x >= 0.):
        p1_ai = np.exp(-ksi) / (2. * np.pi ** 0.5 * x ** 0.25)
        p1_bi = np.exp(ksi) / (np.pi ** 0.5 * x ** 0.25)
        ai_ar = p1_ai
        bi_ar = p1_bi
        # while ((np.abs(ai_oldm - ai_m) >= epsilon or np.abs(bi_oldm - bi_m) >= epsilon) and
        #        (np.abs(ai_oldar - ai_ar) >= epsilon or np.abs(bi_oldar - bi_ar) >= epsilon)):
        # while ((np.abs(ai_m) > np.abs(ai_oldm) or np.abs(bi_m) > np.abs(bi_oldm)) or
        # (np.abs(ai_ar) > np.abs(ai_oldar) or np.abs(bi_ar) > np.abs(bi_oldar))):
        #     ai_oldm = ai_m
        #     bi_oldm = bi_m
        #     ai_oldar = ai_ar
        #     bi_oldar = bi_ar
        while ((np.abs(val_aim) >= epsilon or np.abs(val_bim) >= epsilon) and
               (np.abs(val_aia) >= epsilon or np.abs(val_bia) >= epsilon)):
        # while ((np.abs(ai_m - ai[w])/ai[w] >= epsilon or np.abs(bi_m - bi[w])/bi[w] >= epsilon) and
        #        (np.abs(ai_ar - ai[w])/ai[w] >= epsilon or np.abs(bi_ar - bi[w])/bi[w] >= epsilon)):
        #     if (i > 1000):
        #         break
            # Mauclarinovi vrsti
            f = f * (x ** (3.) * 3. * ((1. / 3.) + i - 1)) / \
                ((3. * (i - 1.) + 3.) * (3. * (i - 1.) + 2.) * (3. * (i - 1.) + 1.))
            g = g * (x ** (3.) * 3. * ((2. / 3.) + i - 1.)) / \
                ((3. * (i - 1.) + 4.) * (3. * (i - 1.) + 3.) * (3. * (i - 1.) + 2.))
            val_aim = alpha * f - beta * g
            val_bim = 3. ** 0.5 * (alpha * f + beta * g)
            ai_m = ai_m + val_aim
            bi_m = bi_m + val_bim
            # asimptotski razvoj za velike x>0
            L = L * (3. * (i - 1.) + 5. / 2.) * \
                (3. * (i - 1.) + 3. / 2.) * \
                (3. * (i - 1.) + 1. / 2.) / (54 * i * (i - 0.5) * ksi)
            val_aia = p1_ai * (-1) ** i * L
            val_bia = p1_bi * L
            ai_ar = ai_ar + val_aia
            bi_ar = bi_ar + val_bia
            i = i + 1.
            print(i)
    else:
        p2 = 1. / (np.pi ** 0.5 * (-x) ** 0.25)
        ai_ar = p2 * (np.sin(ksi - np.pi / 4.) * Q + np.cos(ksi - np.pi / 4.) * P)
        bi_ar = p2 * (-np.sin(ksi - np.pi / 4.) * P + np.cos(ksi - np.pi / 4.) * Q)
        while ((np.abs(ai_oldm - ai_m) >= epsilon or np.abs(bi_oldm - bi_m) >= epsilon) and
               (np.abs(ai_oldar - ai_ar) >= epsilon or np.abs(bi_oldar - bi_ar) >= epsilon)):
        # while ((np.abs(ai[w] - ai_m)/ai[w] >= epsilon or np.abs(bi[w] - bi_m)/bi[w] >= epsilon) and
        #        (np.abs(ai[w] - ai_ar)/ai[w] >= epsilon or np.abs(bi[w] - bi_ar) >= epsilon)/bi[w]):
        # while ((np.abs(ai_m) > np.abs(ai_oldm) or np.abs(bi_m) > np.abs(bi_oldm)) or
        #        (np.abs(ai_ar) > np.abs(ai_oldar) or np.abs(bi_ar) > np.abs(bi_oldar))):
            ai_oldm = ai_m
            bi_oldm = bi_m
            ai_oldar = ai_ar
            bi_oldar = bi_ar
        # while ((np.abs(val_aim) >= epsilon or np.abs(val_bim) >= epsilon) and
        #        (np.abs(val_aia) >= epsilon or np.abs(val_bia) >= epsilon)):
        #     if (i > 1000):
        #         break
            # Mauclarinovi vrsti
            f = f * (x ** (3.) * 3. * ((1. / 3.) + i - 1)) / \
                ((3. * (i - 1.) + 3.) * (3. * (i - 1.) + 2.) * (3. * (i - 1.) + 1.))
            g = g * (x ** (3.) * 3. * ((2. / 3.) + i - 1.)) / \
                ((3. * (i - 1.) + 4.) * (3. * (i - 1.) + 3.) * (3. * (i - 1.) + 2.))
            val_aim = alpha * f - beta * g
            val_bim = 3. ** 0.5 * (alpha * f + beta * g)
            ai_m = ai_m + val_aim
            bi_m = bi_m + val_bim
            # asimptotski razvoj za velike |x|
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
            i = i + 1
            print(i)

    # print bi_ar, bi[j], np.abs(bi_ar - bi[j])
    ai_maclaurin[j] = ai_m
    bi_maclaurin[j] = bi_m
    ai_asimptot[j] = ai_ar
    bi_asimptot[j] = bi_ar
    j = j + 1

# for i in range(9999):
#     if ((np.abs(ai_maclaurin[i] - ai[i]) > np.abs(ai_asimptot[i] - ai[i]) and
#          np.abs(ai_maclaurin[i + 1] - ai[i + 1]) < np.abs(ai_asimptot[i + 1] - ai[i + 1])) or
#         (np.abs(ai_maclaurin[i] - ai[i]) < np.abs(ai_asimptot[i] - ai[i]) and
#          np.abs(ai_maclaurin[i + 1] - ai[i + 1]) > np.abs(ai_asimptot[i + 1] - ai[i + 1]))):
#         #print ('ai'), x0[i], ai_maclaurin[i], ai_asimptot[i], ai[i]
#         pass
# for i in range(9999):
#     if ((np.abs(bi_maclaurin[i] - bi[i]) > np.abs(bi_asimptot[i] - bi[i]) and
#          np.abs(bi_maclaurin[i + 1] - bi[i + 1]) < np.abs(ai_asimptot[i + 1] - ai[i + 1])) or
#         (np.abs(bi_maclaurin[i] - bi[i]) < np.abs(bi_asimptot[i] - bi[i]) and
#          np.abs(bi_maclaurin[i + 1] - bi[i + 1]) > np.abs(bi_asimptot[i + 1] - bi[i + 1]))):
#         #print ('bi'), x0[i], bi_maclaurin[i], bi_asimptot[i], bi[i]
#         pass

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


M= 1000
x1 = np.linspace(-15., 15., M)
aim, bim = np.zeros(M),np.zeros(M)
for t in range(M):
    aim[t] = mauclarin_vrsti(x1[t])[0]
    bim[t] = mauclarin_vrsti(x1[t])[1]

import matplotlib.pyplot as plt

plt.plot(x0, ai_maclaurin,'-', label='$Ai (x)$')
plt.plot(x0, bi_maclaurin,'-', label='$Bi (x)$')
plt.ylim(-1,1.5)
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.figure()

plt.plot(x0, ai_asimptot,'-', label='$Ai (x)$')
plt.plot(x0, bi_asimptot,'-', label='$Bi (x)$')
plt.ylim(-1,1.5)
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

# ABSOLUTNE NAPAKE
plt.subplot(211)
plt.plot(x0, np.abs(aim - ai), label='Maclaurin')
plt.plot(x0, np.abs(ai_asimptot - ai), label='Asimpt.')
plt.yscale("log")
plt.xlabel("x")
plt.ylabel("$\Delta Ai$")
plt.legend()
# plt.figure()
plt.subplot(212)
plt.plot(x0, np.abs(bim - bi), label='Maclaurin')
plt.plot(x0, np.abs(bi_asimptot - bi), label='Asimpt.')
plt.yscale("log")
plt.xlabel("x")
plt.ylabel("$\Delta Bi$")
plt.legend()

# plt.figure()
# plt.plot(x0, np.log(np.abs(ai_maclaurin - ai)), label='$ln(|Ai_m(x) - Ai(x)|)$')
# plt.plot(x0, np.log(np.abs(ai_asimptot - ai)), label='$ln(|Ai_a(x) - Ai(x)|)$')
# plt.plot(x0, np.log(np.abs(bi_maclaurin - bi)), label='$ln(|Bi_m(x) - Bi(x)|)$')
# plt.plot(x0, np.log(np.abs(bi_asimptot - bi)), label='$ln(|Bi_a(x) - Bi(x)|)$')
# plt.legend()
plt.show()
# RELATIVNE NAPAKE
plt.subplot(211)
plt.plot(x0, (np.abs(ai_asimptot - ai) / np.abs(ai)), label='Asimpt.')
plt.plot(x0, (np.abs(aim - ai) / np.abs(ai)), label='Maclaurin')
# konst = [10**(-10) for h in range(10000)]
# plt.plot(x0, (konst), ':', linewidth=1.2, label='${10^{-10}}$')
plt.yscale("log")
plt.xlabel("x")
plt.ylabel("$\dfrac{\Delta Ai}{Ai}$")
plt.legend()
# plt.figure()
plt.subplot(212)
plt.plot(x0, (np.abs(bi_asimptot - bi) / np.abs(bi)), label='Asimpt.')
plt.plot(x0, (np.abs(bim - bi) / np.abs(bi)), label='Maclaurin')
# konst = [10**(-10) for h in range(M)]
# plt.plot(x0, (konst), ':', linewidth=1.2, label='${10^{-10}}$')
plt.yscale("log")
plt.xlabel("x")
plt.ylabel("$\dfrac{\Delta Bi}{Bi}$")
plt.legend()
plt.show()



# plt.plot(x0, np.log(np.abs(ai_maclaurin - ai) / np.abs(ai)),
#          label='$\ln{\dfrac{|Ai_m(x) - Ai(x)|}{|Ai(x)|}}$')
# plt.plot(x0, np.log(np.abs(ai_asimptot - ai) / np.abs(ai)),
#          label='$\ln{\dfrac{|Ai_a(x) - Ai(x)|}{|Ai(x)|}}$')
# konst = [10**(-10) for h in range(10000)]
# # plt.plot(x0, (konst), ':', linewidth=1.2, label='${10^{-10}}$')
# plt.legend()
# plt.figure()
#
# plt.plot(x0, np.log(np.abs(bi_maclaurin - bi) / np.abs(bi)),
#          label='$\ln{\dfrac{|Bi_m(x) - Bi(x)|}{|Bi(x)|}}$')
# plt.plot(x0, np.log(np.abs(bi_asimptot - bi) / np.abs(bi)),
#          label='$\ln{\dfrac{|Bi_a(x) - Bi(x)|}{|Bi(x)|}}$')
#
# plt.legend(loc='upper right')

# plt.ylim(-0.1,2)
# plt.yscale("log")
plt.show()
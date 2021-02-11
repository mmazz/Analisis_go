# -*- coding: utf-8 -*-
"""
   Trueskill Through Time
   ~~~~~~~~~
   :copyright: (c) 2019-2020 by Gustavo Landfried.
   :license: BSD, see LICENSE for more details.
"""
import math
#import ipdb
#from numba import jit

"""
TODO:
    - NUMBA
"""

MU = 25.0; SIGMA = (MU/3)
PI = SIGMA**-2; TAU = PI * MU
BETA = (SIGMA / 2); GAMMA = 0.5#(SIGMA / 100)
DRAW_PROBABILITY = 0.0
EPSILON = 1e-6
sqrt2 = math.sqrt(2)
sqrt2pi = math.sqrt(2 * math.pi)
inf = math.inf

def erfc(x):
    #"""(http://bit.ly/zOLqbc)"""
    z = abs(x)
    t = 1.0 / (1.0 + z / 2.0)
    a = -0.82215223 + t * 0.17087277; b =  1.48851587 + t * a
    c = -1.13520398 + t * b; d =  0.27886807 + t * c; e = -0.18628806 + t * d
    f =  0.09678418 + t * e; g =  0.37409196 + t * f; h =  1.00002368 + t * g
    r = t * math.exp(-z * z - 1.26551223 + t * h)
    return r if not(x<0) else 2.0 - r

def erfcinv(y):
    if y >= 2: return -inf
    if y < 0: raise ValueError('argument must be nonnegative')
    if y == 0: return inf
    if not (y < 1): y = 2 - y
    t = math.sqrt(-2 * math.log(y / 2.0))
    x = -0.70711 * ((2.30753 + t * 0.27061) / (1.0 + t * (0.99229 + t * 0.04481)) - t)
    for _ in [0,1,2]:
        err = erfc(x) - y
        x += err / (1.12837916709551257 * math.exp(-(x**2)) - x * err)
    return x if (y < 1) else -x

def compute_margin(draw_probability, size):
    _N = Gaussian(0.0, math.sqrt(size)*BETA)
    return abs(_N.ppf(0.5-draw_probability/2))



class Gaussian(object):
    def __init__(self,mu=0, sigma=inf, inverse=False):
        if not inverse:
            self.tau, self.pi = self.tau_pi(mu, sigma)
        else:
            self.tau, self.pi = mu, sigma

    def tau_pi(self,mu,sigma):
        if sigma < 0.: raise ValueError('sigma**2 should be greater than 0')
        if sigma > 0.:
            _pi = sigma**-2
            _tau = _pi * mu
        else:
            _pi = inf
            _tau = inf
        return _tau, _pi

    @property
    def mu(self):
        return 0. if (self.pi ==inf or self.pi==0.) else self.tau / self.pi
    @property
    def sigma(self):
        return math.sqrt(1 / self.pi) if self.pi else inf
    def cdf(self, x):
        z = -(x - self.mu) / (self.sigma * sqrt2)
        return (0.5 * erfc(z))
    def pdf(self, x):
        normalizer = (sqrt2pi * self.sigma)**-1
        functional = math.exp( -((x - self.mu)**2) / (2*self.sigma**2) )
        return normalizer * functional
    def ppf(self, p):
        return self.mu - self.sigma * sqrt2  * erfcinv(2 * p)
    def trunc(self, margin, tie):
        N01 = Gaussian(0,1)
        _alpha = (-margin-self.mu)/self.sigma
        _beta  = ( margin-self.mu)/self.sigma
        if not tie:
            #t= -_alpha
            v = N01.pdf(-_alpha) / N01.cdf(-_alpha)
            w = v * (v + (-_alpha))
        else:
            v = (N01.pdf(_alpha)-N01.pdf(_beta))/(N01.cdf(_beta)-N01.cdf(_alpha))
            u = (_alpha*N01.pdf(_alpha)-_beta*N01.pdf(_beta))/(N01.cdf(_beta)-N01.cdf(_alpha))
            w =  - ( u - v**2 )
        mu = self.mu + self.sigma * v
        sigma = self.sigma* math.sqrt(1-w)
        return Gaussian(mu, sigma)
    def __iter__(self):
        return iter((self.mu, self.sigma))
    def __repr__(self):
        return 'N(mu={:.3f}, sigma={:.3f})'.format(self.mu, self.sigma)
    def __add__(self, M):
        return Gaussian(self.mu + M.mu, math.sqrt(self.sigma**2 + M.sigma**2))
    def __sub__(self, M):
        return Gaussian(self.mu - M.mu, math.sqrt(self.sigma**2 + M.sigma**2))
    def __mul__(self, M):
        _tau, _pi = self.tau + M.tau, self.pi + M.pi
        return Gaussian(_tau, _pi, inverse=True)
    def __truediv__(self, M):
        _tau = self.tau - M.tau; _pi = self.pi - M.pi
        return Gaussian(_tau, _pi, inverse=True)
    def delta(self, M):
        return abs(self.mu - M.mu) , abs(self.sigma - self.sigma)
    def exclude(self, M):
        return Gaussian(self.mu - M.mu, math.sqrt(self.sigma**2 - M.sigma**2) )
    def isapprox(self, M, tol=1e-4):
        return (abs(self.mu - M.mu) < tol) and (abs(self.sigma - M.sigma) < tol)

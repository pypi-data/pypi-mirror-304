#!/usr/bin/env python3

"""
An open source package to generate synthetic IEC wind 
fields with extended turbulence characteristics 
url="https://github.com/fiddir/pyforwind"
license="MIT license"
"""

import matplotlib
import numpy as np
import math
import sys
import scipy.stats as stats
import scipy

import scipy.special as sc
from scipy.special import gamma, factorial
import scipy.special as sc
from matplotlib import pyplot as plt
from scipy.misc import derivative
import pandas as pd

class SWF:
    def __init__(self, H, L, L_c, tilde_L, mu, dy, dz, y_i, y_e, z_i, z_e, T, tilde_T, N_x, N_y, N_z, N_xi, V_hub, sigma=None):
        self.H = H
        self.L = L
        self.L_c = L_c
        self.tilde_L = tilde_L
        self.mu = mu
        self.dy = dy
        self.dz = dz
        self.y_i = y_i
        self.y_e = y_e
        self.z_i = z_i
        self.z_e = z_e
        self.T = T
        self.tilde_T = tilde_T
        self.df = 1./self.T
        self.N_x = N_x
        self.N_y = N_y
        self.N_z = N_z
        self.N_xi = N_xi
        self.V_hub = V_hub
        if sigma is None:
             self.sigma = 1.
        else:
            self.sigma = sigma
        self.dt = self.T/self.N_x
        self.t = np.linspace(self.dt, self.dt*(self.N_x/2), self.N_x//2+1)
        self.y = np.linspace(y_i, y_e, self.N_y)
        self.z = np.linspace(z_i, z_e, self.N_z)
        self.Fs = self.N_x/self.T
        self.f = np.linspace(self.df, 0.5*self.Fs, self.N_x//2+1)
        self.Y, self.Z = np.meshgrid(self.y, self.z)
        positions = np.vstack([self.Y.ravel(), self.Z.ravel()]).T
        self.R_ij = scipy.spatial.distance.cdist(positions, positions, 'euclidean')

    def kaimal_spec(self, F):
        return 4.*self.sigma**2*self.L/(1.+6.*F*self.L/self.V_hub)**(1.+2.*self.H)/self.V_hub

    def kaimal_coh(self, F, R):
        return np.exp(-12.*R*np.sqrt((F/self.V_hub)**2+(0.12/self.L_c)**2))
    
    def cov(self):
        kaimal_spec_vec = np.vectorize(self.kaimal_spec)
        return np.fft.irfft(kaimal_spec_vec(self.f))[:self.N_x//2]

    def rescaled_spec(self, xi):
        T_rescaled = np.array(xi**np.sqrt(self.mu*np.log(self.tilde_T/(self.t)))*(self.t/self.tilde_T)**(self.mu/2)*self.t)
        rescaled_int = np.array(T_rescaled/self.dt, dtype='int')
        if rescaled_int.max() < self.N_x//2-1:
            df = pd.DataFrame({'corr' : self.cov()[rescaled_int]})
            df[df.duplicated()]  = None
            cov_rescaled = df.interpolate(method='linear')
        else:
            cov = self.cov()
            rescaled_tilde = rescaled_int[rescaled_int<self.N_x//2]
            cov_rescaled = np.append(cov[rescaled_tilde], cov[rescaled_tilde][-1]*np.ones(self.N_x//2-rescaled_tilde.size+1))
        rescaled_spec = np.fft.rfft(np.append(cov_rescaled, cov_rescaled[::-1][1:]))
        return rescaled_spec

    def gauss_field(self, seed):
        np.random.seed(seed)
        random_phases = np.exp(1j*np.random.random_sample((self.N_y*self.N_y, self.N_x//2+1))*2*np.pi)
        u_hat = np.zeros((self.N_y*self.N_y, self.N_x//2+1), dtype='complex')
        for ff in range(1, self.N_x//2+1):
            coh_decomp = np.linalg.cholesky(self.kaimal_coh(self.f[ff], self.R_ij))
            u_hat[:,ff] = coh_decomp*np.sqrt(self.kaimal_spec(self.f[ff]))@random_phases[:, ff]
        u = np.fft.irfft(u_hat, axis=1)
        return u.reshape(self.N_y, self.N_y, self.N_x)
    
    def mask_field(self):
        random_phases = np.exp(1j*np.random.random_sample((self.N_y*self.N_y, self.N_x//2+1))*2*np.pi)
        u_hat = np.zeros((self.N_y*self.N_y, self.N_x//2+1), dtype='complex')
        for ff in range(1, self.N_x//2+1):
            coh_decomp = np.linalg.cholesky(self.kaimal_coh(self.f[ff], self.R_ij))
            u_hat[:,ff] = coh_decomp*np.sqrt(self.kaimal_spec(self.f[ff]))@random_phases[:, ff]
        u = np.fft.irfft(u_hat, axis=1)
        return u.reshape(self.N_y, self.N_y, self.N_x)

    def field(self, seed):
        np.random.seed(seed)
        random_phases = np.exp(1j*np.random.random_sample((self.N_y*self.N_y, self.N_x//2+1))*2*np.pi)
        u_field = np.zeros((self.N_xi, self.N_y, self.N_y, self.N_x))
        u = np.zeros((self.N_y, self.N_y, self.N_x))
        xi_array = np.sort(np.random.lognormal(0, 1, self.N_xi))
        u_gauss_hat = np.zeros((self.N_y*self.N_y, self.N_x//2+1), dtype='complex')
        for ff in range(1, self.N_x//2+1):
            coh_decomp = np.linalg.cholesky(self.kaimal_coh(self.f[ff], self.R_ij))
            u_gauss_hat[:,ff] = coh_decomp*np.sqrt(self.kaimal_spec(self.f[ff]))@random_phases[:, ff]
        u_gauss = np.fft.irfft(u_gauss_hat, axis=1).reshape(self.N_y, self.N_y, self.N_x)
        for xx in range(self.N_xi):
            xi = xi_array[xx]
            R_rescaled = np.where(self.R_ij==0, 0, np.array(xi**np.sqrt(self.mu*np.log(self.tilde_L/(self.R_ij)))*(self.R_ij/self.tilde_L)**(self.mu/2)*self.R_ij))
            print('xi_values', xi)
            u_hat = np.zeros((self.N_y*self.N_y, self.N_x//2+1), dtype='complex')
            spec = self.rescaled_spec(xi)
            for ff in range(1,self.N_x//2+1):
                coh_decomp = np.linalg.cholesky(self.kaimal_coh(self.f[ff], R_rescaled))
                u_hat[:, ff] = coh_decomp*np.sqrt(spec[ff])@random_phases[:, ff]
            u_field[xx] = np.fft.irfft(u_hat, axis=1).reshape(self.N_y, self.N_y, self.N_x)
        mask = self.mask_field()
        mask /= np.std(mask)
        mask = 1./2*(1.+sc.erf(mask/np.sqrt(2)))
        mask -= mask.min()
        mask /= mask.max()
        mask *= (self.N_xi-1)
        mask = mask.astype(int)
        for xx in range(self.N_y):
            for yy in range(self.N_y):
                for zz in range(self.N_x):
                    u[xx, yy, zz] = u_field[mask[xx, yy, zz], xx, yy, zz]
        u_raw = u
        u_int_hat = np.fft.fftshift(np.fft.rfftn(u),axes=(0,1))
        u_gauss_hat = np.fft.fftshift(np.fft.rfftn(u_gauss),axes=(0,1))
        u_int_hat *= np.sqrt(np.abs(u_gauss_hat)**2/np.abs(u_int_hat)**2)#*np.exp(1j*np.random.random_sample((self.N_y, self.N_y, self.N_x//2+1))*2*np.pi)
        u = np.fft.irfftn(np.fft.ifftshift(u_int_hat,axes=(0,1)))
        return u, u_raw, u_gauss, mask

N_x = 1024 # grid points in "temporal" direction                                                                                                                                                                    
N_y = N_z = 21 # rotor plane                                                                                                                                                                                        
N_xi = 50 # number of realization in Gaussian scale mixture                                                                                                                                                         
dy = dz = 10 # resolution in rotor plane                                                                                                                                                                            
y_i = z_i = -100. # lower left point of grid in rotor plane                                                                                                                                                         
y_e = z_e = 100. # u                                                                                                                                                                                                

H = 1./3. # Hurst exponent, determines power law of Kaimal spectrum                                                                                                                                                 
mu = 0.22 # intermittency coefficient                                                                                                                                                                               
eta = dy
L = 340.2 # integral length scale in Kaimal spectrum                                                                                                                                                                
L_c = 340.2 # correlation length in Kaimal coherences                                                                                                                                                               
T = 600. # length of time series                                                                                                                                                                                    
tilde_T = 600
V_hub = np.arange(int(sys.argv[1]), int(sys.argv[2]))
stem = ''
for uu in range(V_hub.size):
    tilde_L = tilde_T*(V_hub[uu]+0.5)
    seed = 301
    swf = SWF(H, L, L_c, tilde_L, mu, dy, dz, y_i, y_e, z_i, z_e, T, tilde_T, N_x, N_y, N_z, N_xi, V_hub[uu]+0.5)
    for nn in range(1):
        u, u_raw, u_gauss, mask = swf.field(seed)
        u /= np.std(u)
        u_raw /= np.std(u_raw)
        u_gauss /= np.std(u_gauss)
        #u_gauss = swf.gauss_field(seed)
        #u_gauss /= np.std(u_gauss)
        #f = open(stem+'V'+str(V_hub[uu])+'p5__SpatioTemp__Seed_'+str(nn+1)+'__U.log', "x")
        #f.write(str(list(swf.__dict__)[:19]))
        #f.write(str(list(swf.__dict__.values())[:19]))
        #f.write('seed'+str(nn))
        #f.close()
        np.save(stem+'V'+str(V_hub[uu])+'p5__SpatioTemp__Seed_'+str(nn+1)+'__U', u)
        np.save(stem+'V'+str(V_hub[uu])+'p5__SpatioTemp__Seed_Corrected'+str(nn+1)+'__U', u_raw)
        np.save(stem+'V'+str(V_hub[uu])+'p5__Gauss__Seed_'+str(nn+1)+'__U', u_gauss)

        seed +=1




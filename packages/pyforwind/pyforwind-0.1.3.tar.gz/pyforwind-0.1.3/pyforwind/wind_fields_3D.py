#!/usr/bin/env python3

"""
An open source package to generate synthetic wind fields
url="https://github.com/fiddir/winds"
license="MIT license"
"""

import matplotlib                                                                                                                                                                                                                                                                                                                                               
import numpy as np
import math                                                                                                                                                                                                                                                                                                                                                   
import scipy.stats as stats
import scipy                                                                                                                                                                                                                                                                                                                                        
import scipy.special as sc
from scipy.special import gamma, factorial
import scipy.special as sc
from matplotlib import pyplot as plt
from scipy.misc import derivative
import pandas as pd
from scipy import interpolate
from scipy.special import kv
from scipy.special import gamma, factorial

class SWF:
    def __init__(self, H, mu, L, tilde_L, eta, L_x, L_y, L_z, N_x, N_y, N_z, sigma=None): 
        self.H = H
        self.mu = mu
        self.A = 0.
        self.L = L
        self.tilde_L = tilde_L
        self.eta = eta
        self.L_x = L_x
        self.L_y = L_y
        self.L_z = L_z
        self.N_x = N_x
        self.N_y = N_y
        self.N_z = N_z
        if sigma is None:
            self.sigma = 1. 
        else:
            self.sigma = sigma
        kx = np.linspace(-self.N_x//2, self.N_x//2-1, self.N_x)*2.*np.pi/self.L_x
        ky = np.linspace(-self.N_y//2, self.N_y//2-1, self.N_y)*2.*np.pi/self.L_y
        kz = np.linspace(0, self.N_z//2, self.N_z//2+1)*2.*np.pi/self.L_z
        self.KX, self.KY, self.KZ = np.meshgrid(kx, ky, kz, indexing='ij')
        K2 =  np.square(self.KX)+np.square(self.KY)+np.square(self.KZ)
        self.K = np.sqrt(K2)
        x = np.linspace(0, L_x, N_x//2+1)
        y = np.linspace(0, L_y, N_y//2+1)
        z = np.linspace(0, L_z, N_z//2+1)
        X, Y, Z = np.meshgrid(x,y,z, indexing='ij')
        self.R = np.sqrt(np.square(X)+np.square(Y)+np.square(Z))

    def gauss_field(self):
        random_phases_x = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        random_phases_y = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        random_phases_z = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        S = (self.L**(-2)+self.KX**2+self.KY**2+self.KZ**2)**(-17./12.)
        cov = np.fft.irfftn(np.fft.ifftshift(S**2, axes=(0,1)))
        plt.imshow(np.fft.irfftn(np.fft.ifftshift(S**2, axes=(0,1)))[self.N_y//2])
        plt.savefig('cov_mann.pdf')
        hat_u = S*(self.KY*random_phases_z-self.KZ*random_phases_y)
        hat_v = S*(self.KZ*random_phases_x-self.KX*random_phases_z)
        hat_w = S*(self.KX*random_phases_y-self.KY*random_phases_x)
        u = np.fft.irfftn(np.fft.ifftshift(hat_u, axes=(0,1)))
        v = np.fft.irfftn(np.fft.ifftshift(hat_v, axes=(0,1)))
        w = np.fft.irfftn(np.fft.ifftshift(hat_w, axes=(0,1)))
        return u, v, w
    
    def karman_corr(self):
        corr= np.where(self.R==0, 1., 2.*(self.R/(2.*self.L))**(1./3.)*(kv(1./3., self.R/self.L)-(self.R/(3.*self.L))*kv(2./3., self.R/self.L))/gamma(1./3.))
    return corr

    def field(self):
        random_phases_x = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        random_phases_y = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        random_phases_z = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        cov = karman_corr(R.flatten(), L).reshape(N_x//2+1, N_y//2+1, N_z//2+1)
        cov = np.fft.irfftn(np.fft.ifftshift(S**2, axes=(0,1)))
        plt.imshow(np.fft.irfftn(np.fft.ifftshift(S**2, axes=(0,1)))[self.N_y//2])
        plt.savefig('cov_mann.pdf')
        hat_u = S*(self.KY*random_phases_z-self.KZ*random_phases_y)
        hat_v = S*(self.KZ*random_phases_x-self.KX*random_phases_z)
        hat_w = S*(self.KX*random_phases_y-self.KY*random_phases_x)
        u = np.fft.irfftn(np.fft.ifftshift(hat_u, axes=(0,1)))
        v = np.fft.irfftn(np.fft.ifftshift(hat_v, axes=(0,1)))
        w = np.fft.irfftn(np.fft.ifftshift(hat_w, axes=(0,1)))
        return u, v, w
            
    
    def cov_rescaled(self, xi):
        z = np.arange(self.N_z)
        y = np.piecewise(x, [x < self.N_y-1, x>=self.N_y-1], [np.arange(self.N_y-1), self.N_y-1]) 
        print(np.size(y))
        #z = np.piecewise(x, [x < self.N_z-1, x>=self.N_z-1], [np.arange(self.N_z-1), self.N_z-1])
        S = (self.L**(-2)+self.KX**2+self.KY**2+self.KZ**2)**(-17./6.)
        corr_radial_full = np.fft.irfftn(np.fft.ifftshift(S, axes=(0,1)))
        print(np.shape(corr_radial_full))
        N_corr = corr_radial_full.size
        corr_radial_left =  corr_radial_full[:N_corr//2]
        corr_radial_right =  corr_radial_full[N_corr//2:][::-1]
        R = np.arange(N_corr//2)/self.N_x
        R_rescaled = np.array(xi**np.sqrt(self.A+self.mu*self.log_plus(R))*((R+self.eta)/self.tilde_L)**(self.mu/2)*R)
        rescaled_int = np.array(R_rescaled/R[1], dtype='int')
        print(rescaled_int)
        if rescaled_int.max() < N_corr//2-1:
            df = pd.DataFrame({'corr' : np.append(corr_radial_left[rescaled_int], corr_radial_right[rescaled_int][::-1])})  
            df[df.duplicated()]  = None
            cov_rescaled = df.interpolate(method='slinear')['corr']
            #df = pd.DataFrame({'corr' : corr_radial_right[rescaled_int]})  
            #df[df.duplicated()]  = None
            #cov_rescaled_right = df.interpolate(method='slinear')['corr']
        else:
            rescaled_tilde = rescaled_int[rescaled_int<N_corr//2]
            cov_rescaled_left = np.append(corr_radial_left[rescaled_tilde], corr_radial_left[rescaled_tilde][-1]*np.ones(N_corr//2-rescaled_tilde.size))
            cov_rescaled_right = np.append(corr_radial_right[rescaled_tilde], corr_radial_right[rescaled_tilde][-1]*np.ones(N_corr//2-rescaled_tilde.size))
            cov_rescaled = np.append(cov_rescaled_left, cov_rescaled_right[::-1])
        plt.plot(np.arange(N_corr), cov_rescaled)
        plt.plot(np.arange(N_corr), corr_radial_full, color='black', ls='dashed')
        plt.savefig('cov_rescaled_mann.pdf')
        x, y, z = np.meshgrid(range(self.N_x),range(self.N_y),range(self.N_z), indexing='ij')
        d = np.sqrt((x-(self.N_x/2)+1)**2+(y-(self.N_y/2)+1)**2+(z-(self.N_z/2)+1)**2)
        f = interpolate.interp1d(np.arange(N_corr), cov_rescaled)
        cov_rescaled = np.fft.fftshift(f(d.flat).reshape(d.shape)[::-1,::-1,::-1])
        #plt.imshow(cov_rescaled[0])
        return cov_rescaled
    
    def karman(self, k):
        return (self.L**(-2)+k**2)**(-17./6.)
    

    def fou_spec(self):
        L_inst = 1*self.L
        K_rescale = self.K*L_inst
        H_eff = 1.
        with np.errstate(divide='ignore'):
            seg = np.where(self.K==0, 0, 1./(2*np.pi*self.K**2))
        return self.sigma**2/(1.+K_rescale**(1.+2.*H_eff))*seg
    
    def log_plus(self, R):
        log_plus = np.where(self.tilde_L/(R+self.eta)>1., np.log(self.tilde_L/(R+self.eta)), 0.)
        #log_plus = np.where(R>self.eta, np.log(self.tilde_L/(R+self.eta)), 0.)
        return log_plus
    
    def mask_field(self):
        random_phases = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        spec = self.fou_spec()
        amplitudes = np.sqrt(spec)
        hat_u = amplitudes*random_phases#*np.exp(-2*self.K**2/self.K.max())
        u = np.fft.irfftn(np.fft.ifftshift(hat_u, axes=(0,1)))
        return u
    
    def field(self):
        N_xi = 1
        random_phases_x = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        random_phases_y = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        random_phases_z = np.exp(1j*np.random.random_sample((self.N_x, self.N_y, self.N_z//2+1))*2*np.pi)
        u = np.zeros((self.N_x, self.N_y, self.N_z))
        u_field = np.zeros((N_xi, self.N_x, self.N_y, self.N_z))
        v = np.zeros((self.N_x, self.N_y, self.N_z))
        v_field = np.zeros((N_xi, self.N_x, self.N_y, self.N_z))
        w = np.zeros((self.N_x, self.N_y, self.N_z))
        w_field = np.zeros((N_xi, self.N_x, self.N_y, self.N_z))
        xi_array = np.sort(np.random.lognormal(0, 1, N_xi))
        idx = np.where(np.abs(xi_array-1.)==np.min(np.abs(xi_array-1.)))[0][0]
        for nn in range(N_xi):
            spec = np.fft.fftshift(np.fft.rfftn(self.cov_rescaled(xi_array[nn])), axes=(0,1))
            amplitudes = np.sqrt(spec)
            hat_u = amplitudes*(self.KY*random_phases_z-self.KZ*random_phases_y)
            hat_v = amplitudes*(self.KZ*random_phases_x-self.KX*random_phases_z)
            hat_w = amplitudes*(self.KX*random_phases_y-self.KY*random_phases_x)
            u_field[nn] = np.fft.irfftn(np.fft.ifftshift(hat_u, axes=(0,1)))
            v_field[nn] = np.fft.irfftn(np.fft.ifftshift(hat_v, axes=(0,1)))
            w_field[nn] = np.fft.irfftn(np.fft.ifftshift(hat_w, axes=(0,1)))
            #u_field[nn]/= np.std(u_field[nn])
        mask = self.mask_field()
        mask /= np.std(mask)
        mask = 1./2*(1+sc.erf(mask/np.sqrt(2)))                                                                                           
        mask -= mask.min()
        mask /= mask.max()
        mask *= (N_xi-1)
        mask = mask.astype(int)  
        for xx in range(self.N_x):
            for yy in range(self.N_y):
                for zz in range(self.N_z):
                    u[xx, yy, zz] = u_field[mask[xx, yy, zz], xx, yy, zz]
                    v[xx, yy, zz] = v_field[mask[xx, yy, zz], xx, yy, zz]
                    w[xx, yy, zz] = w_field[mask[xx, yy, zz], xx, yy, zz]
        #u_hat = np.fft.fftshift(np.fft.rfftn(u), axes=(0,1))
        #u_hat *= np.exp(-2.*self.K**2/self.K.max()**2)
        #u = np.fft.irfftn(np.fft.ifftshift(u_hat, axes=(0,1)))
        return u, u_field[idx], mask

H=1./3.; mu=0.; N_x=128; N_y=128; N_z=1024; L_x=1.; L_y=1.; L_z=10.*1.; eta=1./N_z; L=1.; tilde_L=L#L#dx*N_x+dx # for first try L=4
swf = SWF(H, mu, L, tilde_L, eta, L_x, L_y, L_z, N_x, N_y, N_z)
#u, u_field, mask = swf.field()
u_gauss, v_gauss, w_gauss = swf.gauss_field()
#u_gauss /= np.std(u_gauss)
for nn in range(1):
    u, u_field, mask = swf.field()
#    u_field /= np.std(u_field)
#    u /= np.std(u)
#    print(nn, u.mean(), u_field.mean())
    #np.save('u_karman_8096_21_21_mu_0_24_L_8_tildeL_8_realization_'+str(nn)+'.npy', u[:,:21,:21])
    #np.save('u_karman_8096_21_21_mu_0_L_8_tildeL_8_realization_'+str(nn)+'.npy', u_field[:,:21,:21])
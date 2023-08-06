# Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.io import loadmat
import statsmodels.api as sm
import seaborn as sns
import warnings
from numpy import linalg as LA
warnings.filterwarnings('ignore')

class PoissonGLM:

    def __init__(self):
        datadir = 'data_RGCs/'
        self.stim = np.squeeze(loadmat(f'{datadir}Stim.mat')['Stim']) # contains stimulus value at each frame
        self.stim_times = np.squeeze(loadmat(f'{datadir}stimtimes.mat')['stimtimes']) # contains time in seconds at each frame (120 Hz)
        self.all_spike_times = [np.squeeze(x) for x in np.squeeze(loadmat(f'{datadir}SpTimes.mat')['SpTimes'])] # time of spikes for 4 neurons (in units of stim frames)

        cell_id1 = 0
        self.spike_times1 = self.all_spike_times[cell_id1]
        cell_id2 = 1
        self.spike_times2 = self.all_spike_times[cell_id2]
        cell_id3 = 2
        self.spike_times3 = self.all_spike_times[cell_id3]
        cell_id4 = 3
        self.spike_times4 = self.all_spike_times[cell_id4]

        # Print  some basic info
        self.dt_stim = self.stim_times[1] - self.stim_times[0] # time bin size
        self.refresh_rate = 1/self.dt_stim # refresh rate of the monitor
        self.num_time_bins = self.stim.size # number of time bins in stimulus

        self.num_spikes1 = self.spike_times1.size # number of spikes cell 1
        self.num_spikes2 = self.spike_times2.size # number of spikes cell 2
        self.num_spikes3 = self.spike_times3.size # number of spikes cell 3
        self.num_spikes4 = self.spike_times4.size # number of spikes cell 4

        self.spikes_bin_centers = np.arange(self.num_time_bins+1) * self.dt_stim # centers of bins for applying to spike train
        self.spikes_binned_cell_1,_ = np.histogram(self.spike_times1, self.spikes_bin_centers)
        self.spikes_binned_cell_2,_ = np.histogram(self.spike_times2, self.spikes_bin_centers)
        self.spikes_binned_cell_3,_ = np.histogram(self.spike_times3, self.spikes_bin_centers)
        self.spikes_binned_cell_4,_ = np.histogram(self.spike_times4, self.spikes_bin_centers)

        self.iiplot = np.arange(360)
        self.jjplot = np.arange(360, 425)
        self.ttplot = self.iiplot*self.dt_stim

        self.X = self.stim[self.iiplot]
        self.y_cell_1 = self.spikes_binned_cell_1[self.iiplot]
        self.y_cell_2 = self.spikes_binned_cell_2[self.iiplot]
        self.y_cell_3 = self.spikes_binned_cell_3[self.iiplot]
        self.y_cell_4 = self.spikes_binned_cell_4[self.iiplot]

        self.X_tst = self.stim[self.jjplot]
        self.y_cell_1_tst = self.spikes_binned_cell_1[self.jjplot]
        self.y_cell_2_tst = self.spikes_binned_cell_2[self.jjplot]
        self.y_cell_3_tst = self.spikes_binned_cell_3[self.jjplot]
        self.y_cell_4_tst = self.spikes_binned_cell_4[self.jjplot]

    def print_dataset(self):
        print(f'Length of stimulus: {self.stim.shape}')
        print(f'Number of spikes for each of 4 neurons: {" ".join([str(x.size) for x in self.all_spike_times])}')

        print('--------------------------')
        print(f'Loaded RGC data: cell for all 4 cells')
        print(f'Number of stim frames: {self.num_time_bins} ({self.num_time_bins*self.dt_stim:.1f} seconds)')
        print(f'Time bin size: {self.dt_stim*1000:.1f} ms')
        print(f'Number of spikes cell 1: {self.num_spikes1} (mean rate={self.num_spikes1/self.num_time_bins*self.refresh_rate:.1f} Hz)')
        print(f'Number of spikes cell 2: {self.num_spikes2} (mean rate={self.num_spikes2/self.num_time_bins*self.refresh_rate:.1f} Hz)')
        print(f'Number of spikes cell 3: {self.num_spikes3} (mean rate={self.num_spikes3/self.num_time_bins*self.refresh_rate:.1f} Hz)')
        print(f'Number of spikes cell 4: {self.num_spikes4} (mean rate={self.num_spikes4/self.num_time_bins*self.refresh_rate:.1f} Hz)')

    def visualise_data(self):
        fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(5)
        fig.set_size_inches(12,10)
        ax1.plot(self.ttplot, self.stim[self.iiplot])
        ax1.set_title('Raw Stimulus (Full Field Flicker)')
        ax1.set_ylabel('Stimulus Intensity (Contrast)')
        ax1.set_xlabel('Time (s)')

        self.spike_times_1_plot = self.spike_times1[(self.spike_times1>=self.ttplot[0]) & (self.spike_times1<self.ttplot[-1])]
        ax2.plot(self.spike_times_1_plot, [1]*self.spike_times_1_plot.size, 'ko')
        ax2.set_xlim([self.ttplot[0], self.ttplot[-1]])
        ax2.set_xlabel('Time (s)')
        ax2.set_title('Spike Times')

        self.spike_times_2_plot = self.spike_times2[(self.spike_times2>=self.ttplot[0]) & (self.spike_times2<self.ttplot[-1])]
        ax3.plot(self.spike_times_2_plot, [1]*self.spike_times_2_plot.size, 'ko')
        ax3.set_xlim([self.ttplot[0], self.ttplot[-1]])
        ax3.set_xlabel('Time (s)')

        self.spike_times_3_plot = self.spike_times3[(self.spike_times3>=self.ttplot[0]) & (self.spike_times3<self.ttplot[-1])]
        ax4.plot(self.spike_times_3_plot, [1]*self.spike_times_3_plot.size, 'ko')
        ax4.set_xlim([self.ttplot[0], self.ttplot[-1]])
        ax4.set_xlabel('Time (s)')

        self.spike_times_4_plot = self.spike_times4[(self.spike_times4>=self.ttplot[0]) & (self.spike_times4<self.ttplot[-1])]
        ax5.plot(self.spike_times_4_plot, [1]*self.spike_times_4_plot.size, 'ko')
        ax5.set_xlim([self.ttplot[0], self.ttplot[-1]])
        ax5.set_xlabel('Time (s)')

        plt.tight_layout()
        plt.show()

    def make_cosine_basis(self, nB, firstPeak, lastPeak, coupling, visualise):
        nB1 = nB
        peakRange1 = [firstPeak, lastPeak]
        dt1 = 0.01
        if coupling:
            logOffset1 = 0.9
        else:
            logOffset1 = 0.005

        def nlin(x):
            return np.log(x+1e-20)
        def invnl(x):
            return np.exp(x-1e-20)

        logPeakFirst1 = nlin(peakRange1[0]+logOffset1)
        logPeakLast1 = nlin(peakRange1[-1]+logOffset1)
        logPeakRange1 = [logPeakFirst1, logPeakLast1]
        dCtr1 = np.diff(logPeakRange1)/(nB1-1)
        Bctrs1 = np.arange(logPeakRange1[0], logPeakRange1[1]+dCtr1, dCtr1)

        minT1 = 0
        maxT1 = invnl(logPeakRange1[1]+2*dCtr1)-logOffset1
        self.tgrid1 = np.arange(minT1, maxT1, dt1)
        nT = len(self.tgrid1)

        def raisedCosFun(x,ctr,dCtr):
            min1 = np.minimum(np.pi, (x-ctr)*np.pi/dCtr/2)
            max1 = np.maximum(-np.pi,min1)
            cos1 = np.cos(max1)+1
            return cos1/2
            
        mat = nlin(self.tgrid1+logOffset1)
        tile1 = np.tile(mat, (nB1, 1))
        tile1 = tile1.T
        tile2 = np.tile(Bctrs1.T, (nT, 1))

        cosBasis = raisedCosFun(tile1, tile2, dCtr1)
        cosBasis = cosBasis[:500]

        if visualise:
            plt.title('Post-Spike Filter')
            plt.xlabel('Spike history time bins')
            plt.ylabel('Cosine basis function value')
            plt.ylim((0,1))
            plt.xlim((0,5))
            plt.plot(self.tgrid1[:500], cosBasis)
            plt.show()

        return cosBasis

    def spike_rate_single(self,curr_index, post_spike_values, y_vals_curr):
        spike_window_curr_cell = y_vals_curr[curr_index-5:curr_index] # preceding 5 time bins
        dotted_history = np.dot(spike_window_curr_cell, post_spike_values[::-1])
        stim_value = self.X[curr_index]
        ans = stim_value + dotted_history + 0.88 #arbitrary constant
        exp_ans = np.exp(ans)
        return exp_ans

    def spike_rate_single_tst(self,curr_index, post_spike_values, y_vals_curr):
        spike_window_curr_cell = y_vals_curr[curr_index-5:curr_index] # preceding 5 time bins
        dotted_history = np.dot(spike_window_curr_cell, post_spike_values[::-1])
        stim_value = self.X_tst[curr_index]
        ans = stim_value + dotted_history + 0.88 #arbitrary constant
        exp_ans = np.exp(ans)
        return exp_ans

    def spike_rate_coupled(self,curr_index, post_spike_values, y_vals_curr, coupling_values, y_vals_coupled):
        spike_window_curr_cell = y_vals_curr[curr_index-5:curr_index] # preceding 5 time bins
        spike_window_coupled_cell = y_vals_coupled[curr_index-5:curr_index]
        dotted_history = np.dot(spike_window_curr_cell, post_spike_values[::-1])
        dotted_coupled = np.dot(spike_window_coupled_cell, coupling_values[::-1])
        stim_value = self.X[curr_index]
        ans = stim_value + dotted_history + dotted_coupled + 0 #arbitrary constant
        exp_ans = np.exp(ans)
        return exp_ans

    def spike_rate_coupled_tst(self,curr_index, post_spike_values, y_vals_curr, coupling_values, y_vals_coupled):
        spike_window_curr_cell = y_vals_curr[curr_index-5:curr_index] # preceding 5 time bins
        spike_window_coupled_cell = y_vals_coupled[curr_index-5:curr_index]
        dotted_history = np.dot(spike_window_curr_cell, post_spike_values[::-1])
        dotted_coupled = np.dot(spike_window_coupled_cell, coupling_values[::-1])
        stim_value = self.X_tst[curr_index]
        ans = stim_value + dotted_history + dotted_coupled + 0 #arbitrary constant
        exp_ans = np.exp(ans)
        return exp_ans

    def spike_rate_fully_coupled(self,curr_index, post_spike_values, y_vals_curr, coupling_values_1, y_vals_coupled_1,
        coupling_values_2, y_vals_coupled_2, coupling_values_4, y_vals_coupled_4):
        spike_window_curr_cell = y_vals_curr[curr_index-5:curr_index] # preceding 5 time bins
        spike_window_coupled_cell_1 = y_vals_coupled_1[curr_index-5:curr_index]
        spike_window_coupled_cell_2 = y_vals_coupled_2[curr_index-5:curr_index]
        spike_window_coupled_cell_4 = y_vals_coupled_4[curr_index-5:curr_index]
        dotted_history = np.dot(spike_window_curr_cell, post_spike_values[::-1])
        dotted_coupled_1 = np.dot(spike_window_coupled_cell_1, coupling_values_1[::-1])
        dotted_coupled_2 = np.dot(spike_window_coupled_cell_2, coupling_values_2[::-1])
        dotted_coupled_4 = np.dot(spike_window_coupled_cell_4, coupling_values_4[::-1])
        stim_value = self.X[curr_index]
        ans = stim_value + dotted_history + dotted_coupled_1 + dotted_coupled_2 + dotted_coupled_4 + 0 #arbitrary constant
        exp_ans = np.exp(ans)
        return exp_ans

    def spike_rate_fully_coupled_tst(self,curr_index, post_spike_values, y_vals_curr, coupling_values_1, y_vals_coupled_1,
        coupling_values_2, y_vals_coupled_2, coupling_values_4, y_vals_coupled_4):
        spike_window_curr_cell = y_vals_curr[curr_index-5:curr_index] # preceding 5 time bins
        spike_window_coupled_cell_1 = y_vals_coupled_1[curr_index-5:curr_index]
        spike_window_coupled_cell_2 = y_vals_coupled_2[curr_index-5:curr_index]
        spike_window_coupled_cell_4 = y_vals_coupled_4[curr_index-5:curr_index]
        dotted_history = np.dot(spike_window_curr_cell, post_spike_values[::-1])
        dotted_coupled_1 = np.dot(spike_window_coupled_cell_1, coupling_values_1[::-1])
        dotted_coupled_2 = np.dot(spike_window_coupled_cell_2, coupling_values_2[::-1])
        dotted_coupled_4 = np.dot(spike_window_coupled_cell_4, coupling_values_4[::-1])
        stim_value = self.X_tst[curr_index]
        ans = stim_value + dotted_history + dotted_coupled_1 + dotted_coupled_2 + dotted_coupled_4 + 0 #arbitrary constant
        exp_ans = np.exp(ans)
        return exp_ans

    # %%
    def generate_binned_spike_train_single(self,post_spike_values):
        post_spikes = post_spike_values
        spike_train = [0,0,0,0,0]
        rates = []
        for i in range(5, len(self.X_tst)):
            # use poisson distribution to generate spike train
            rate = self.spike_rate_single_tst(i, post_spikes, spike_train)
            if rate < 0.8:
                rate = 0
            rates.append(rate)
            probabilities = []
        
            for j in range(4):
                # f(y) = e^-(spike rate) * (spike rate)^y / y!
                prob = (np.exp(-rate) *  (rate ** j))/ np.math.factorial(j)
                probabilities.append((prob, j))
            probabilities.sort(reverse=True)
            spike_train.append(probabilities[0][1])
        
        spike_train = spike_train[5:] # taking into account the first 5 0's needed for filter initialisation
        fig, (ax1,ax2) = plt.subplots(2)
        fig.set_size_inches(14,10)
        ax1.plot(spike_train, 'r', alpha=0.4, label="Predicted")
        ax1.stem(self.y_cell_3_tst[:-5], label="Actual")
        ax1.set_title('Spike Count Single Cell')
        ax1.set_xlabel('Time Bins')
        ax1.set_ylabel('Count')
        ax1.legend()

        ax2.plot(rates)
        ax2.set_title('Spike Rate Single Cell')
        ax2.set_ylabel('Rate')
        ax2.set_xlabel('Time Bins')
        return spike_train


    def generate_binned_spike_train_coupled(self, post_spike_values, coupled_values, coupled_history):
        post_spikes = post_spike_values
        spike_train = [0,0,0,0,0]
        rates = []
        for i in range(5, len(self.X_tst)):
            # use poisson distribution to generate spike train
            rate = self.spike_rate_coupled_tst(i, post_spikes, spike_train, coupled_values, coupled_history)
            if rate < 1.85:
                rate = rate*0.7
            rates.append(rate)
            probabilities = []
        
            for j in range(4):
                # f(y) = e^-(spike rate) * (spike rate)^y / y!
                prob = (np.exp(-rate) *  (rate ** j))/ np.math.factorial(j)
                probabilities.append((prob, j))
            probabilities.sort(reverse=True)
            spike_train.append(probabilities[0][1])
        
        spike_train = spike_train[5:] # taking into account the first 5 0's needed for filter initialisation
        fig, (ax1,ax2) = plt.subplots(2)
        fig.set_size_inches(14,10)
        ax1.plot(spike_train, 'r', alpha=0.4, label="Predicted")
        ax1.stem(self.y_cell_3_tst[:-5], label="Actual")
        ax1.set_title('Spike Count Coupled Cell')
        ax1.set_xlabel('Time Bins')
        ax1.set_ylabel('Count')
        ax1.legend()

        ax2.plot(rates)
        ax2.set_title('Spike Rate Coupled Cell')
        ax2.set_ylabel('Rate')
        ax2.set_xlabel('Time Bins')
        return spike_train

    def generate_binned_spike_train_fully_coupled(self,post_spike_values, coupled_values_1, coupled_history_1, coupled_values_2, coupled_history_2, coupled_values_4, coupled_history_4):
        post_spikes = post_spike_values
        spike_train = [0,0,0,0,0]
        rates = []
        for i in range(5, len(self.X_tst)):
            # use poisson distribution to generate spike train
            rate = self.spike_rate_fully_coupled(i, post_spikes, spike_train, coupled_values_1, coupled_history_1, coupled_values_2, coupled_history_2, coupled_values_4, coupled_history_4)
            rate = np.log(rate)
            if rate < 3:
                rate = rate*0.5
            if rate > 5 and rate < 8:
                rate = rate*0.8
            rates.append(rate)
            probabilities = []
        
            for j in range(4):
                # f(y) = e^-(spike rate) * (spike rate)^y / y!
                prob = (np.exp(-rate) *  (rate ** j))/ np.math.factorial(j)
                if j == 3:
                    prob = prob*0.625
                probabilities.append((prob, j))
            probabilities.sort(reverse=True)
            spike_train.append(probabilities[0][1])
        
        spike_train = spike_train[5:] # taking into account the first 5 0's needed for filter initialisation
        fig, (ax1,ax2) = plt.subplots(2)
        fig.set_size_inches(14,10)
        ax1.plot(spike_train, 'r', alpha=0.4, label="Predicted")
        ax1.stem(self.y_cell_3_tst[2:-5], label="Actual")
        ax1.set_title('Spike Count Fully Coupled Cell')
        ax1.set_xlabel('Time Bins')
        ax1.set_ylabel('Count')
        ax1.legend()

        ax2.plot(rates)
        ax2.set_title('Spike Rate Fully Coupled Cell')
        ax2.set_ylabel('Rate')
        ax2.set_xlabel('Time Bins')
        return spike_train


    # %%
    def nll_single(self,coeffs, y_vals_curr1):
        y_vals_curr = y_vals_curr1
        weighted_ps = np.sum(coeffs * self.make_cosine_basis(5,0.1,2.5,False,False), axis=1)
        post_spike_values = [weighted_ps[50], weighted_ps[100], weighted_ps[150], weighted_ps[200], weighted_ps[250]]
        term1 = 0.0
        for i in range(5, len(self.X)):
            current_spike_rate = self.spike_rate_single(i, post_spike_values, y_vals_curr)
            if current_spike_rate == 0:
                current_spike_rate = 0.0000001
            log = np.log(current_spike_rate)
            if log == -np.inf:
                log = 0
            term1 += log
        term2 = 0.0
        for j in range(5, len(self.X)):
            current_spike_rate = self.spike_rate_single(j, post_spike_values, y_vals_curr)
            total = current_spike_rate
            term2 += total

        penalty = 2.05 * np.sum(coeffs**2)
        log_likelihood = term1 - (0.01*term2) + penalty
        return - log_likelihood


    # %%
    def nll_coupled(self, coeffs, y_vals_curr1, y_vals_coupled1):
        ps_coeffs = coeffs[:5]
        coupled_coeffs = coeffs[5:]
        y_vals_curr = y_vals_curr1
        y_vals_coupled = y_vals_coupled1
        weighted_ps = np.sum(ps_coeffs * self.make_cosine_basis(5,0.1,2.5,False,False), axis=1)
        post_spike_values = [weighted_ps[50], weighted_ps[100], weighted_ps[150], weighted_ps[200], weighted_ps[250]]
        weighted_coupled = np.sum(coupled_coeffs * self.make_cosine_basis(3,1.5,3.5,True,False), axis=1)
        coupled_values = [weighted_coupled[50], weighted_coupled[100], weighted_coupled[150], weighted_coupled[200], weighted_coupled[250]]
        term1 = 0.0
        for i in range(5, len(self.X)):
            current_spike_rate = self.spike_rate_coupled(i, post_spike_values, y_vals_curr, coupled_values, y_vals_coupled)
            if current_spike_rate == 0:
                current_spike_rate = 0.0000001
            log = np.log(current_spike_rate)
            if log == -np.inf:
                log = 0
            term1 += log
        term2 = 0.0
        for j in range(5, len(self.X)):
            current_spike_rate = self.spike_rate_coupled(j, post_spike_values, y_vals_curr, coupled_values, y_vals_coupled)
            total = current_spike_rate
            term2 += total

        penalty = 2.05 * np.sum(coeffs**2)
        log_likelihood = term1 - (0.01*term2) + penalty
        return - log_likelihood

    # %%
    def nll_fully_coupled(self, coeffs, y_vals_curr1, y_vals_coupled1, y_vals_coupled2, y_vals_coupled4):
        ps_coeffs = coeffs[:5]
        coupled_coeffs_1 = coeffs[5:8]
        coupled_coeffs_2 = coeffs[8:11]
        coupled_coeffs_4 = coeffs[11:]
        y_vals_curr = y_vals_curr1
        y_vals_coupled_1 = y_vals_coupled1
        y_vals_coupled_2 = y_vals_coupled2
        y_vals_coupled_4 = y_vals_coupled4
        weighted_ps = np.sum(ps_coeffs * self.make_cosine_basis(5,0.1,2.5,False, False), axis=1)
        post_spike_values = [weighted_ps[50], weighted_ps[100], weighted_ps[150], weighted_ps[200], weighted_ps[250]]
        weighted_coupled_1 = np.sum(coupled_coeffs_1 * self.make_cosine_basis(3,1.5,3.5,True, False), axis=1)
        coupled_values_1 = [weighted_coupled_1[50], weighted_coupled_1[100], weighted_coupled_1[150], weighted_coupled_1[200], weighted_coupled_1[250]]
        weighted_coupled_2 = np.sum(coupled_coeffs_2 * self.make_cosine_basis(3,1.5,3.5,True, False), axis=1)
        coupled_values_2 = [weighted_coupled_2[50], weighted_coupled_2[100], weighted_coupled_2[150], weighted_coupled_2[200], weighted_coupled_2[250]]
        weighted_coupled_4 = np.sum(coupled_coeffs_4 * self.make_cosine_basis(3,1.5,3.5,True, False), axis=1)
        coupled_values_4 = [weighted_coupled_4[50], weighted_coupled_4[100], weighted_coupled_4[150], weighted_coupled_4[200], weighted_coupled_4[250]]
        term1 = 0.0
        for i in range(5, len(self.X)):
            current_spike_rate = self.spike_rate_fully_coupled(i, post_spike_values, y_vals_curr, coupled_values_1, y_vals_coupled_1, coupled_values_2, y_vals_coupled_2, coupled_values_4, y_vals_coupled_4)
            if current_spike_rate == 0:
                current_spike_rate = 0.000001
            log = np.log(current_spike_rate)
            if log == -np.inf:
                log = 0
            term1 += log
        term2 = 0.0
        for j in range(5, len(self.X)):
            current_spike_rate = self.spike_rate_fully_coupled(j, post_spike_values, y_vals_curr, coupled_values_1, y_vals_coupled_1, coupled_values_2, y_vals_coupled_2, coupled_values_4, y_vals_coupled_4)
            total = current_spike_rate
            term2 += total

        penalty = 2.05 * np.sum(coeffs**2)
        log_likelihood = term1 - (0.01*term2) + penalty
        return - log_likelihood

    # %%

    def optimise_single(self):
        initial_thetas = [0,0,0,0,0]
        minimized = minimize(self.nll_single, args=(self.y_cell_3),x0=initial_thetas, method='Nelder-Mead')
        print('NLL: ', minimized.fun)
        optimal_thetas_unnormalised = minimized.x

        optimal_thetas_ps = optimal_thetas_unnormalised / LA.norm(optimal_thetas_unnormalised)

        optimal_post_spike = np.sum(optimal_thetas_ps * self.make_cosine_basis(5,0.1,2.5,False,False), axis=1)
        optimal_post_spike_vals = [optimal_post_spike[50], optimal_post_spike[100], optimal_post_spike[150], optimal_post_spike[200], optimal_post_spike[250]]

        plt.figure().set_figwidth(12)
        plt.title('Post-Spike Filter')
        plt.xlabel('Spike history time bins')
        plt.ylabel('Weighted value')
        plt.plot(self.tgrid1[:1000], optimal_post_spike)
        plt.xlim((0,5))
        plt.plot(self.tgrid1[:1000], self.tgrid1[:1000]*0, color='red', alpha=0.1)
        plt.tight_layout()
        plt.show()

        return optimal_post_spike_vals

    def optimise_coupled(self):
        initial_thetas = [0,0,0,0,0,0,0,0]
        minimized = minimize(self.nll_coupled, args=(self.y_cell_3, self.y_cell_4),x0=initial_thetas, method='Nelder-Mead')
        print('NLL: ', minimized.fun)
        optimal_thetas_unnormalised = minimized.x

        optimal_thetas_ps = optimal_thetas_unnormalised[:5] / LA.norm(optimal_thetas_unnormalised[:5])
        optimal_thetas_coupling = optimal_thetas_unnormalised[5:] / LA.norm(optimal_thetas_unnormalised[5:])

        optimal_post_spike = np.sum(optimal_thetas_ps * self.make_cosine_basis(5,0.1,2.5,False,False), axis=1)
        optimal_coupling = np.sum(optimal_thetas_coupling * self.make_cosine_basis(3,1,3.5,True,False), axis=1)
        optimal_post_spike_vals = [optimal_post_spike[50], optimal_post_spike[100], optimal_post_spike[150], optimal_post_spike[200], optimal_post_spike[250]]
        optimal_coupling_vals = [optimal_coupling[50], optimal_coupling[100], optimal_coupling[150], optimal_coupling[200], optimal_coupling[250]]

        fig, (ax1,ax2) = plt.subplots(2)
        fig.set_size_inches(12,8)
        ax1.set_title('Post-Spike Filter')
        ax1.set_xlabel('Spike history time bins')
        ax1.set_ylabel('Weighted value')
        ax1.set_xlim((0,5))
        ax1.plot(self.tgrid1[:500], self.tgrid1[:500]*0, color='red', alpha=0.1)
        ax1.plot(self.tgrid1[:500], optimal_post_spike)

        ax2.set_title('Coupling Filter')
        ax2.set_xlabel('Spike history time bins')
        ax2.set_ylabel('Cosine basis function value')
        ax2.plot(self.tgrid1[:500], optimal_coupling)
        ax2.plot(self.tgrid1[:500], self.tgrid1[:500]*0, color='red', alpha=0.1)
        ax2.set_xlim((0,5))
        plt.tight_layout()
        plt.show()

        return optimal_post_spike_vals, optimal_coupling_vals

    def optimise_fully_coupled(self):
        initial_thetas = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        minimized = minimize(self.nll_fully_coupled, args=(self.y_cell_3, self.y_cell_1, self.y_cell_2, self.y_cell_4),x0=initial_thetas, method='Nelder-Mead', options={'ftol':1e-2, 'xtol':1e-2})
        print('NLL: ', minimized.fun)
        optimal_thetas_unnormalised = minimized.x
        
        optimal_thetas_ps = optimal_thetas_unnormalised[:5] / LA.norm(optimal_thetas_unnormalised[:5])
        optimal_thetas_coupling_1 = optimal_thetas_unnormalised[5:8] / LA.norm(optimal_thetas_unnormalised[5:8])
        optimal_thetas_coupling_2 = optimal_thetas_unnormalised[8:11] / LA.norm(optimal_thetas_unnormalised[8:11])
        optimal_thetas_coupling_4 = optimal_thetas_unnormalised[11:] / LA.norm(optimal_thetas_unnormalised[11:])

        optimal_post_spike = np.sum(optimal_thetas_ps * self.make_cosine_basis(5,0.1,2.5, False, False), axis=1)
        optimal_coupling_1 = np.sum(optimal_thetas_coupling_1 * self.make_cosine_basis(3,1.5,3.5,True,False), axis=1)
        optimal_coupling_2 = np.sum(optimal_thetas_coupling_2 * self.make_cosine_basis(3,1.5,3.5,True,False), axis=1)
        optimal_coupling_4 = np.sum(optimal_thetas_coupling_4 * self.make_cosine_basis(3,1.5,3.5,True,False), axis=1)
        optimal_post_spike_vals = [optimal_post_spike[50], optimal_post_spike[100], optimal_post_spike[150], optimal_post_spike[200], optimal_post_spike[250]]
        optimal_coupling_vals_1 = [optimal_coupling_1[50], optimal_coupling_1[100], optimal_coupling_1[150], optimal_coupling_1[200], optimal_coupling_1[250]]
        optimal_coupling_vals_2 = [optimal_coupling_2[50], optimal_coupling_2[100], optimal_coupling_2[150], optimal_coupling_2[200], optimal_coupling_2[250]]
        optimal_coupling_vals_4 = [optimal_coupling_4[50], optimal_coupling_4[100], optimal_coupling_4[150], optimal_coupling_4[200], optimal_coupling_4[250]]    

        fig, (ax1,ax2,ax3,ax4) = plt.subplots(4)
        fig.set_size_inches(12,8)
        ax1.set_title('Post-Spike Filter')
        ax1.set_xlim((0,5))
        ax1.set_xlabel('Spike history time bins')
        ax1.set_ylabel('Weighted value')
        ax1.plot(self.tgrid1[:500], self.tgrid1[:500]*0, color='red', alpha=0.1)
        ax1.plot(self.tgrid1[:500], optimal_post_spike)

        ax2.set_title('Coupling Filter from Cell 1')
        ax2.set_xlabel('Spike history time bins')
        ax2.set_ylabel('Cosine basis function value')
        ax2.set_xlim((0,5))
        ax2.plot(self.tgrid1[:500], self.tgrid1[:500]*0, color='red', alpha=0.1)
        ax2.plot(self.tgrid1[:500], optimal_coupling_1)

        ax3.set_title('Coupling Filter from Cell 2')
        ax3.set_xlabel('Spike history time bins')
        ax3.set_ylabel('Cosine basis function value')
        ax3.set_xlim((0,5))
        ax3.plot(self.tgrid1[:500], self.tgrid1[:500]*0, color='red', alpha=0.1)
        ax3.plot(self.tgrid1[:500], optimal_coupling_2)

        ax4.set_title('Coupling Filter from Cell 4')
        ax4.set_xlabel('Spike history time bins')
        ax4.set_ylabel('Cosine basis function value')
        ax4.set_xlim((0,5))
        ax4.plot(self.tgrid1[:500], self.tgrid1[:500]*0, color='red', alpha=0.1)
        ax4.plot(self.tgrid1[:500], optimal_coupling_4)
        plt.tight_layout()
        plt.show()

        return optimal_post_spike_vals, optimal_coupling_vals_1, optimal_coupling_vals_2, optimal_coupling_vals_4

    def final_single_model(self):
        post_spike_single_final = self.optimise_single()
        estimated_spike_train_single = self.generate_binned_spike_train_single(post_spike_single_final)
        results = np.array(estimated_spike_train_single)
        actual = np.var(self.y_cell_3_tst) / np.mean(self.y_cell_3_tst)
        pred = np.var(results) / np.mean(results)
        print('Actual Fano Factor: ', actual)
        print('Single Cell Fano Factor: ', pred)

    def final_coupled_model(self):
        post_spike_final, coupling_final = self.optimise_coupled()
        estimated_spike_train_coupled = self.generate_binned_spike_train_coupled(post_spike_final, coupling_final,self.y_cell_4_tst)
        results = np.array(estimated_spike_train_coupled)
        actual = np.var(self.y_cell_3_tst) / np.mean(self.y_cell_3_tst)
        pred = np.var(results) / np.mean(results)
        print('Actual Fano Factor: ', actual)
        print('2-Coupled Fano Factor: ', pred)

    def final_fully_coupled_model(self):
        post_spike_final, coupling_final_1, coupling_final_2, coupling_final_4 = self.optimise_fully_coupled()
        estimated_spike_train_fully_coupled = self.generate_binned_spike_train_fully_coupled(post_spike_final, coupling_final_1, self.y_cell_1_tst, coupling_final_2, self.y_cell_2_tst, coupling_final_4, self.y_cell_4_tst)
        results = np.array(estimated_spike_train_fully_coupled)
        actual = np.var(self.y_cell_3_tst) / np.mean(self.y_cell_3_tst)
        pred = np.var(results) / np.mean(results)
        print('Actual Fano Factor: ', actual)
        print('Fully Coupled Fano Factor: ', pred)
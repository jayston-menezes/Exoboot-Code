import numpy as np
import exoboot
import time

class MusculoTendonJoint(object):
    n = 0  # counter

    # f_lce
    W = .56
    C = np.log(.05)

    # f_vce
    N = 1.5
    K = 5

    # f_pe
    E_REF_PE = W
    # f_be
    E_REF_BE = .5 * W
    E_REF_BE2 = 1 - W
    # f_se
    E_REF = 0.1 #

    # ECC
    TAU_ACT = .01  # [s]
    TAU_DACT = .04  # [s]

    # S range
    RNG_S = [.01, 1]

    def __init__(self, TIMESTEP, kw, FeedbackfromSensoryData, n_update=1):
        MusculoTendonJoint.n += 1
        self.s_data = FeedbackfromSensoryData
        # print(kw)

        # simulation timestep
        self.TIMESTEP = TIMESTEP
        self.TIMESTEP_inter = TIMESTEP / n_update
        self.n_update = n_update
        self.time_list = list()

        # muscle parameters
        self.F_max = kw['F_max']
        self.l_opt = kw['l_opt']
        self.v_max = kw['v_max']
        self.l_slack = kw['l_slack']

        # muscle attachment parameters
        self.r1 = kw['r1']  # > 0 if l_mtu ~ phi1
        self.phi1_ref = kw['phi1_ref']
        self.rho = kw['rho']
        self.r2 = 0 if 'r2' not in kw else kw['r2']  # > 0 if l_mtu ~ phi2
        self.phi2_ref = 0 if 'phi2_ref' not in kw else kw['phi2_ref']

        self.A_init = .01 if 'A' not in kw else kw['A']

        self.phi1 = kw['phi1_0']
        self.phi2 = None if 'phi2_0' not in kw else kw['phi2_0']

        # -----------------------------------------------
        # angles from degrees to radians
        self.phi1_ref *= np.pi / 180
        self.phi1 *= np.pi / 180

        self.phi2_ref *= np.pi / 180
        self.phi2 = self.phi2 * np.pi / 180 if self.phi2 is not None else None
        # -----------------------------------------------

        self.flag_afferent = 0 if 'flag_afferent' not in kw else kw['flag_afferent']
        # print(self.flag_afferent)
        if self.flag_afferent:
            self.del_t = kw['del_t']  # sensory delay

        self.name = 'muscle' + str(MusculoTendonJoint.n) if 'name' not in kw else kw['name']

        self.reset(self.phi1, self.phi2)

    def __del__(self):
        nn = "empty"

    def reset(self, phi1, phi2=None):
        self.phi1 = phi1
        self.phi2 = phi2

        self.v_ce = 0
        self.F_mtu = 0
        self.A = self.A_init
        self.S = self.A

        l_mtu = self.l_slack + self.l_opt
        l_mtu -= self.rho * self.r1 * (self.phi1 - self.phi1_ref)
        if self.phi2 is not None:
            l_mtu -= self.rho * self.r2 * (self.phi2 - self.phi2_ref)
        self.l_ce = l_mtu - self.l_slack

        if self.flag_afferent:
            l_que = round(self.del_t / self.TIMESTEP)
            self.aff_l_ce0 = [self.l_ce / self.l_opt] * l_que
            self.aff_v_ce0 = [0] * l_que
            self.aff_F_mtu0 = [0] * l_que

    def update_inter(self, S, phi1, phi2=None, n_update=1):
        MTU = MusculoTendonJoint

        # ECC: update self.A
        self.fn_ECC(S)  # Excitation Contraction Coupling

        # calculate l_mtu
        l_mtu = self.l_slack + self.l_opt
        l_mtu -= self.rho * self.r1 * (phi1 - self.phi1_ref)
        if phi2 is not None:
            l_mtu -= self.rho * self.r2 * (phi2 - self.phi2_ref)

        # update muscle state
        self.l_se = l_mtu - self.l_ce
        f_se0 = fn_f_p0(self.l_se / self.l_slack, MTU.E_REF)
        f_be0 = fn_f_p0_ext(self.l_ce / self.l_opt, MTU.E_REF_BE, MTU.E_REF_BE2)
        f_pe0 = fn_f_p0(self.l_ce / self.l_opt, MTU.E_REF_PE)
        f_lce0 = fn_f_lce0(self.l_ce / self.l_opt, MTU.W, MTU.C)
        f_vce0 = (f_se0 + f_be0) / (f_pe0 + self.A * f_lce0)
        # f_vce0 = (f_se0 + f_be0 - f_pe0)/(self.A*f_lce0)
        v_ce0 = fn_inv_f_vce0(f_vce0, MTU.K, MTU.N)

        # self.v_ce = 0.5*self.l_opt*self.v_max*v_ce0
        self.v_ce = self.l_opt * self.v_max * v_ce0
        self.l_ce = self.l_ce + self.v_ce * self.TIMESTEP_inter
        self.F_mtu = self.F_max * f_se0

    def update(self, S, phi1, phi2=None):

        # self.reset(self.phi1_initial, self.phi2_initial)

        n_update = self.n_update
        if n_update == 1:  # Number o
            self.update_inter(S, phi1, phi2)
        else:
            begin_time = time.time()
            v_S = np.linspace(S, self.S, n_update, endpoint=False)
            v_phi1 = np.linspace(phi1, self.phi1, n_update, endpoint=False)
            if phi2 is not None:
                v_phi2 = np.linspace(phi2, self.phi2, n_update, endpoint=False)
            for i in range(n_update):
                S_inter = v_S[-i - 1]
                phi1_inter = v_phi1[-i - 1]
                phi2_inter = None if phi2 is None else v_phi2[-i - 1]
                self.update_inter(S_inter, phi1_inter, phi2_inter, n_update=n_update)

        if self.flag_afferent:
            self.updateSensor()

        self.S = S
        self.phi1 = phi1
        self.phi2 = phi2

    def getTorque(self):
        return self.F_mtu * self.r1

    def getTorque2(self):
        return self.F_mtu * self.r2

    def getSensoryData(self):
        if self.s_data is 'F_mtu':
            return self.aff_F_mtu0[0]
        elif self.s_data is 'l_ce':
            return self.aff_l_ce0[0]
        elif self.s_data is 'v_ce':
            return self.aff_v_ce0[0]
        else:
            import sys
            sys.exit("wrong data query!!")

    def updateSensor(self):
        self.aff_v_ce0.append(self.v_ce / (self.l_opt * self.v_max))
        self.aff_v_ce0.pop(0)
        self.aff_l_ce0.append(self.l_ce / self.l_opt)
        self.aff_l_ce0.pop(0)
        self.aff_F_mtu0.append(self.F_mtu / self.F_max)
        self.aff_F_mtu0.pop(0)

    def fn_ECC(self, S):
        MTU = MusculoTendonJoint

        S = np.clip(S, MTU.RNG_S[0], MTU.RNG_S[1])
        A = self.A
        if S > A:
            tau = MTU.TAU_ACT
        else:
            tau = MTU.TAU_DACT

        dA = (S - A) / tau
        self.A = A + dA * self.TIMESTEP_inter

        return self.A

    def getStates(self):
        F_mtu0 = self.F_mtu / self.F_max
        l_ce0 = self.l_ce / self.l_opt
        v_ce0 = self.v_ce / (self.l_opt * self.v_max)
        return (self.name, F_mtu0, l_ce0, v_ce0)


# MTU based on Geyer2010
def fn_inv_f_vce0(f_vce0, K, N):
    if f_vce0 <= 1:
        v_ce0 = (f_vce0 - 1) / (K * f_vce0 + 1)
    elif f_vce0 > 1 and f_vce0 <= N:
        temp = (f_vce0 - N) / (f_vce0 - N + 1)
        v_ce0 = (temp + 1) / (1 - 7.56 * K * temp)
    else:  # elif f_vce0 > N:
        v_ce0 = .01 * (f_vce0 - N) + 1

    return v_ce0

def fn_f_lce0(l_ce0, w, c):
    f_lce0 = np.exp(c * np.abs((l_ce0 - 1) / (w)) ** 3)
    return f_lce0


# f_p0 is for both f_se0 and f_pe0
def fn_f_p0(l0, e_ref):
    if l0 > 1:
        f_p0 = ((l0 - 1) / (e_ref)) ** 2
    else:
        f_p0 = 0

    return f_p0


# for both f_be0
def fn_f_p0_ext(l0, e_ref, e_ref2):
    if l0 < e_ref2:
        f_p0 = ((l0 - e_ref2) / (e_ref)) ** 2
    else:
        f_p0 = 0

    return f_p0

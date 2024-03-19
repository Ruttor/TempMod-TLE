import matplotlib.pyplot as plt
import numpy as np

def create_tempmap(rate, pulse_durations, temp):
    # Creates a meshgrid for the colormap
    p, T_p = np.meshgrid(rate, pulse_durations)
    # Converts the temperatures into an array and reshapes it into the right shape (2D)
    temp_min, temp_max = np.nanmin(temp), np.nanmax(temp)
    Temps = np.array(temp).reshape(len(rate), len(pulse_durations))
    # Creates the colormap
    plt.figure(figsize=(5, 4))
    plt.imshow(Temps, origin='lower', aspect='auto', cmap='inferno')
    # plt.tick_params(axis='both', which='major', labelsize=12)
    # plt.yticks([p.min(), p.max()], ['kurz', 'lang'], fontsize=12)
    # plt.xticks([p.min(), p.max()], ['niedrig', 'hoch'], fontsize=12)
    # currently german labels because I need them for my thesis (will be changed in the future)
    print(temp_min, temp_max)
    cbar = plt.colorbar(label='$T_\mathrm{Sub}$', ticks=[temp_min, temp_max])
    cbar.set_label('$T_\mathrm{Sub}$', fontsize=12, labelpad=-30)
    cbar.ax.set_yticklabels(['niedrig', 'hoch'], fontsize=12)
    # plt.loglog()
    plt.xlabel('$R$', fontsize=12)
    plt.ylabel('$t_\mathrm{P}$', fontsize=12, labelpad=-20)
    plt.savefig('tempmap.pdf', bbox_inches = "tight")
    plt.show()
    
def create_thickmap(rate, pulse_durations, thick):
    # Creates a meshgrid for the colormap
    p, T_p = np.meshgrid(rate, pulse_durations)
    # Converts the temperatures into an array and reshapes it into the right shape (2D)
    Thicks = np.array(thick).reshape(len(rate), len(pulse_durations))
    # Creates the colormap
    plt.figure(figsize=(8, 6))
    plt.imshow(Thicks, extent=(p.min(), p.max(), T_p.min(), T_p.max()), origin='lower', aspect='auto', cmap='inferno')
    # plt.tick_params(axis='both', which='major', labelsize=12)
    # plt.xticks([p.min(), p.max()], ['niedrig', 'hoch'])
    # plt.yticks([p.min(), p.max()], ['kurz', 'lang'])
    # currently german labels because I need them for my thesis (will be changed in the future)
    plt.colorbar(label='Schichtdicke')
    plt.xlabel('Rate', fontsize=12)
    plt.ylabel('Pulsdauer', fontsize=12)
    plt.savefig('thickmap.pdf', bbox_inches = "tight")
    plt.show()

def create_powmap(rate, pulse_durations, pow):
    # Creates a meshgrid for the colormap
    p, T_p = np.meshgrid(rate, pulse_durations)
    # Converts the temperatures into an array and reshapes it into the right shape (2D)
    pow_min, pow_max = np.nanmin(pow), np.nanmax(pow)
    Pows = np.array(pow).reshape(len(rate), len(pulse_durations))
    # Creates the colormap
    plt.figure(figsize=(5, 4))
    plt.imshow(Pows, extent=(p.min(), p.max(), T_p.min(), T_p.max()), origin='lower', aspect='auto', cmap='inferno')
    # plt.tick_params(axis='both', which='major', labelsize=12)
    # plt.yticks([p.min(), p.max()], ['kurz', 'lang'], fontsize=12)
    # plt.xticks([p.min(), p.max()], ['niedrig', 'hoch'], fontsize=12)
    # currently german labels because I need them for my thesis (will be changed in the future)
    print(pow_min, pow_max)
    cbar = plt.colorbar(label='$P$', ticks=[pow_min, pow_max])
    cbar.set_label('$P$', fontsize=12, labelpad=-30)
    cbar.ax.set_yticklabels(['niedrig', 'hoch'], fontsize=12)
    # plt.loglog()
    plt.xlabel('$R$', fontsize=12)
    plt.ylabel('$t_\mathrm{P}$', fontsize=12, labelpad=-20)
    plt.savefig('powmap.pdf', bbox_inches = "tight")
    plt.show()
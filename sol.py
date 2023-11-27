import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import newton
from scipy.optimize import bisect
import mod
import dgl
from tqdm import tqdm

params = {
    'P': 2e5,
    'T0_so': 1e-14,
    'T0_sub': 0e0,
    't_range': [0,100],
    'pulsed': True,
    'f': 0.1,
    't_p': 1e0,
    'n': 10,
    'thick0': 0.0,
    }

def schichtdicke(P, t_end=100, t_p=None, n=10, pulsed=False):

    # erhebt Valuerror 
    # wenn t_p nicht angegeben ist, aber gepulster Betrieb gewünscht ist
    if pulsed and not t_p:
        raise ValueError("t_p is required for pulsed laser heating.")
    
    tm = mod.TempMod(dgl.T_punkt)  # Initialisiert die Temperaturmodell-Klasse
    if pulsed:
        result = tm.mod(P=P, T0_so=params['T0_so'], T0_sub=params['T0_sub'], pulsed=pulsed, f=params['f'], t_p=t_p, n=n, gr_factor=dgl.c['gr_factor'], gr_exp=dgl.c['gr_exp'])
    else:
        result = tm.mod(P=P, T0_so=params['T0_so'], T0_sub=params['T0_sub'], t_range=[0, t_end], gr_factor=dgl.c['gr_factor'], gr_exp=dgl.c['gr_exp'])
    # Returnt die letzte Schichtdicke und die maximale Substrattemperatur
    return result['Thickness'][-1], result['Temp_substrate'].max()

def fehlerfunktion(P_pulse, t_p, rate, t_end, n, cache={}):

    # Schlüssel für den Cache
    key = (t_p, rate, P_pulse, t_end, n)
    if key in cache:
        return cache[key]  # Gibt gecachtes Ergebnis zurück, falls vorhanden
    # Berechnet nur die Differenz der Schichtdicken, die Temperatur wird hier ignoriert
    thickness_const = rate * t_end
    thickness_pulse, _ = schichtdicke(P_pulse, t_end, t_p, n, pulsed=True)
    #print(thickness_pulse)
    diff = thickness_const - thickness_pulse
    cache[key] = diff
    return diff


def nullstellen(fehlerfunktion, a, b, args=()):
    bisektion = bisect(fehlerfunktion, a, b, args=args, xtol=1)
    print(bisektion)
    nullstelle = newton(fehlerfunktion, bisektion, args=args, tol=0.1)
    return nullstelle

# Beispiel für die Anwendung der geänderten Funktion
n = 10
t_p = [i*0.1 for i in range(1, n+1)]
rate_vals = [i*0.1 for i in range(1, n+1)]
p_opt = []
colormap_data = []
colormap_data_thick = []
print(t_p[0], rate_vals[0])



# Schleife für die Berechnung der optimalen Pulsbreite

print('p_opt Berechnung läuft:')
for i in range(len(rate_vals)):
    print(f'Berechnung für t_p={t_p[i]}s:')
    for r in rate_vals:
        p_opt.append(nullstellen(fehlerfunktion, 0, 1e10, args=(t_p[i], r, 10, 10)))
print('p_opt Berechnung ist fertig.')
#print(p_opt)
# Schleife über die Leistung und Pulsbreiten
print('Berechnung der Temperaturen läuft:')
for tp in t_p:
    for p in range(len(rate_vals)):
        #print(p, tp)
        thickness_solved, temperature = schichtdicke(P=p_opt[p], t_p=tp, pulsed=True)  # Gepulster Betrieb
        print(f'Thickness: {thickness_solved}nm, Temperature: {temperature}K')
        colormap_data.append(temperature)
        colormap_data_thick.append(thickness_solved)
print('Berechnung der Temperaturen ist fertig.')

# Erstellen der Farbkarte
def create_colormap(rate, pulse_durations, temp):
    # Erstellen des Meshgrids für die Leistung und die Pulsbreiten
    p, T_p = np.meshgrid(rate, pulse_durations)
    # Konvertiert die Temperaturen in ein Array und formt es in die richtige Form (2D)
    Temps = np.array(temp).reshape(len(rate), len(pulse_durations))
    # Erstellen der Farbkarte mit imshow
    plt.figure(figsize=(8, 6))
    plt.imshow(Temps, extent=(p.min(), p.max(), T_p.min(), T_p.max()), origin='lower', aspect='auto', cmap='inferno')
    #for i in range(len(p_opt)):
        #plt.plot(power, p_opt[i], ':', label=f'$t_P$ same thickness as const P={(i+10)*100 }W')
    plt.colorbar(label='Substrattemperatur')
    #plt.loglog()
    plt.xlabel('Rate')
    plt.ylabel('Pulsdauer')
    plt.title('Temperatur Colormap')
    #plt.legend()
    plt.show()

create_colormap(rate_vals, t_p, colormap_data)

    
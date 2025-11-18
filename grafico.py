import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as pe 

# Style 
COLOR_ANDREW = 'royalblue'     
COLOR_BARNEY = 'firebrick'    
COLOR_LIGHT_CONE = 'orange'    
COLOR_SIGNAL_A = 'blue'       
COLOR_SIGNAL_B = 'red'        
BG_COLOR = '#F9F9F9'          

shadow = [pe.withStroke(linewidth=3, foreground='black', alpha=0.2)]

# Math
v = 0.6 
c = 1.0
gamma = 1 / np.sqrt(1 - v**2) 

ct_turnaround = 5
x_turnaround = v * ct_turnaround
ct_end = 10

tau_turnaround = ct_turnaround / gamma  
tau_end = ct_end / gamma                

# Graphic
fig, ax = plt.subplots(figsize=(8, 10))
fig.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_title("Spacetime Diagram: The Twin Paradox (v = 0.6c)", pad=20, fontsize=16)

ax.plot([0, 0], [0, ct_end], color=COLOR_ANDREW, linewidth=2.5, 
        label="Andrew's world line", path_effects=shadow)

ax.plot([0, x_turnaround], [0, ct_turnaround], color=COLOR_BARNEY, linewidth=2.5, 
        label="Barney's outgoing world line", path_effects=shadow)
ax.plot([x_turnaround, 0], [ct_turnaround, ct_end], color=COLOR_BARNEY, linewidth=2.5, 
        label="Barney's returning world line", path_effects=shadow)

ax.plot(x_turnaround, ct_turnaround, 'o', color='yellow', markersize=10, 
        markeredgecolor='black', markeredgewidth=1.5)

andrew_ticks_ct = np.arange(0, ct_end + 1, 1)
ax.plot(np.zeros_like(andrew_ticks_ct), andrew_ticks_ct, 'o', color=COLOR_ANDREW, 
        markersize=6, markeredgecolor='white', markeredgewidth=1)
for t in andrew_ticks_ct:
    ax.text(-0.1, t, f'{int(t)}', ha='right', va='center', 
            color=COLOR_ANDREW, fontsize=9, fontweight='bold')

#Barney
barney_tau = np.arange(0, tau_end + 1, 1)
barney_ticks_x = []
barney_ticks_ct = []

for tau in barney_tau:
    if tau <= tau_turnaround:
        t = tau * gamma
        x = v * t
        ha, offset = 'left', 0.1 
    else:
        tau_prime = tau - tau_turnaround
        t = ct_turnaround + (tau_prime * gamma)
        x = x_turnaround - (v * tau_prime * gamma)
        ha, offset = 'left', 0.1 
    
    barney_ticks_x.append(x)
    barney_ticks_ct.append(t)
    ax.plot(x, t, 'o', color=COLOR_BARNEY, markersize=6, 
            markeredgecolor='white', markeredgewidth=1)
    ax.text(x + offset, t, f'{int(tau)}', ha=ha, va='center', 
            color=COLOR_BARNEY, fontsize=9, fontweight='bold')

# Signals
for i in range(1, len(barney_ticks_x)): 
    x_barney, ct_barney = barney_ticks_x[i], barney_ticks_ct[i]
    ct_andrew = ct_barney + x_barney 
    ax.arrow(x_barney, ct_barney, -x_barney, ct_andrew - ct_barney, 
             color=COLOR_SIGNAL_B, ls='-', lw=1, alpha=0.6, 
             head_width=0.1, head_length=0.2, length_includes_head=True)
    
# Signals from Andrew to Barney 
for t_andrew in andrew_ticks_ct[1:-1]: 
    x_barney_out = v * t_andrew / (1 - v)
    ct_barney_out = t_andrew / (1 - v)
    
    if ct_barney_out <= ct_turnaround + 1e-6:
        ax.arrow(0, t_andrew, x_barney_out, ct_barney_out - t_andrew, 
                 color=COLOR_SIGNAL_A, ls='-', lw=1, alpha=0.6, 
                 head_width=0.1, head_length=0.2, length_includes_head=True)
    else:
        x_barney_ret = v * (ct_end - t_andrew) / (1 + v)
        ct_barney_ret = ct_end - (x_barney_ret / v)
        ax.arrow(0, t_andrew, x_barney_ret, ct_barney_ret - t_andrew, 
                 color=COLOR_SIGNAL_A, ls='-', lw=1, alpha=0.6, 
                 head_width=0.1, head_length=0.2, length_includes_head=True)

# Light cones
ax.plot([0, 6], [0, 6], ':', color=COLOR_LIGHT_CONE, linewidth=2, alpha=0.8)
ax.plot([0, -6], [0, 6], ':', color=COLOR_LIGHT_CONE, linewidth=2, alpha=0.8)

#decorations
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_color('#AAAAAA')
ax.spines['left'].set_color('#AAAAAA')
ax.grid(True, linestyle=':', alpha=0.5)

ax.set_xlim(-3.5, 3.5) 
ax.set_ylim(-1, 11)

ax.set_xlabel('x', fontsize=12, loc='right', labelpad=5)
ax.set_ylabel('ct', fontsize=12, loc='top', rotation=0, labelpad=-10)

ax.set_xticks([])
ax.set_yticks([])

ax.text(-0.2, 7.5, "Andrew's\nworld line", rotation=0, ha='right', va='center', 
        color=COLOR_ANDREW, fontweight='bold')
ax.text(2.4, 3.5, "Barney's outgoing", rotation=53, ha='center', va='center', 
        color=COLOR_BARNEY, fontweight='bold')
ax.text(2.3, 7.0, "Barney's returning", rotation=-53, ha='center', va='center', 
        color=COLOR_BARNEY, fontweight='bold')
ax.text(x_turnaround + 0.3, ct_turnaround, "Turnaround\nPoint", 
        ha='left', va='center', fontweight='bold')
ax.text(3, 2.5, "Light line", rotation=41, ha='center', va='center', 
        color=COLOR_LIGHT_CONE, alpha=0.9)
ax.text(-3, 2.5, "Light line", rotation=-41, ha='center', va='center', 
        color=COLOR_LIGHT_CONE, alpha=0.9)

#Save
plt.tight_layout()
plt.savefig('graphic.png', dpi=200) 

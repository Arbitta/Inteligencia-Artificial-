import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import deque

# PARTE A: VALUE ITERATION

def value_iteration(env, gamma=0.99, theta=1e-8):
    
    n_estados  = env.observation_space.n
    n_aciones = env.action_space.n
    P         = env.unwrapped.P
    V = np.zeros(n_estados)
    interaccion = 0

    while True:
        delta = 0
        for s in range(n_estados):
            v_old = V[s]
            q_values = np.zeros(n_aciones)
            for a in range(n_aciones):
                for prob, next_s, reward, done in P[s][a]:
                    q_values[a] += prob * (reward + gamma * V[next_s] * (not done))
            V[s] = np.max(q_values)
            delta = max(delta, abs(v_old - V[s]))
        interaccion += 1
        if delta < theta:
            break

    policy = np.zeros(n_estados, dtype=int)
    for s in range(n_estados):
        q_values = np.zeros(n_aciones)
        for a in range(n_aciones):
            for prob, next_s, reward, done in P[s][a]:
                q_values[a] += prob * (reward + gamma * V[next_s] * (not done))
        policy[s] = np.argmax(q_values)

    print(f"  Value Iteration convergió en {interaccion} iteraciones.")
    return V, policy

# PARTE B: Q-LEARNING

def q_learning(env, episodes=5000, alpha=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.999, epsilon_min=0.01):
    n_estados  = env.observation_space.n
    n_aciones = env.action_space.n

    Q = np.zeros((n_estados, n_aciones))
    recompensa_episodio  = []
    pasos_por_episodio    = []
    exitos_por_episodio = []

    for ep in range(episodes):
        state, _ = env.reset()
        total_reward = 0
        steps = 0
        done = False

        while not done:
            # Epsilon-greedy
            if np.random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(Q[state])

            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            # Actualización Q-Learning (off-policy)
            best_next = np.max(Q[next_state])
            Q[state, action] += alpha * (
                reward + gamma * best_next * (not done) - Q[state, action]
            )

            state = next_state
            total_reward += reward
            steps += 1

        recompensa_episodio.append(total_reward)
        pasos_por_episodio.append(steps)
        # Éxito: recompensa final es +20 (dejó al pasajero correctamente)
        exitos_por_episodio.append(1 if total_reward > 0 else 0)

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

    policy = np.argmax(Q, axis=1)
    return Q, policy, recompensa_episodio, pasos_por_episodio


# EVALUACIÓN

def evaluar_politica(env, policy, n_episodes=1000):
    exitos = 0
    recompensa_episodio  = []
    pasos_episodio    = []

    for _ in range(n_episodes):
        state, _ = env.reset()
        done = False
        ep_reward = 0
        steps = 0
        while not done:
            action = policy[state]
            state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            ep_reward += reward
            steps += 1
        recompensa_episodio.append(ep_reward)
        pasos_episodio.append(steps)
        if ep_reward > 0:
            exitos += 1

    return {
        "success_rate": exitos / n_episodes,
        "avg_reward":   np.mean(recompensa_episodio),
        "avg_steps":    np.mean(pasos_episodio),
    }


# ──────────────────────────────────────────────
# VISUALIZACIONES
# ──────────────────────────────────────────────

def plot_training(rewards, steps, title="Q-Learning – Taxi-v4", window=200):
    """Gráficas de recompensa y pasos durante el entrenamiento."""
    def moving_avg(data, w):
        return np.convolve(data, np.ones(w)/w, mode='valid')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # Recompensas
    ax = axes[0]
    ax.plot(rewards, alpha=0.2, color='steelblue', label='Recompensa por episodio')
    if len(rewards) >= window:
        avg = moving_avg(rewards, window)
        ax.plot(range(window-1, len(rewards)), avg,
                color='darkorange', linewidth=2, label=f'Media móvil ({window} ep)')
    ax.set_title("Recompensa por episodio")
    ax.set_xlabel("Episodio")
    ax.set_ylabel("Recompensa total")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Pasos
    ax = axes[1]
    ax.plot(steps, alpha=0.2, color='seagreen', label='Pasos por episodio')
    if len(steps) >= window:
        avg_s = moving_avg(steps, window)
        ax.plot(range(window-1, len(steps)), avg_s,
                color='crimson', linewidth=2, label=f'Media móvil ({window} ep)')
    ax.set_title("Pasos por episodio (eficiencia)")
    ax.set_xlabel("Episodio")
    ax.set_ylabel("Cantidad de pasos")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("./taxi_training.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Gráfica guardada: taxi_training.png")


def plot_value_comparison(V_vi, policy_vi, Q_ql, policy_ql):
    """
    Visualiza los valores de los estados (promedio sobre pasajero/destino)
    y muestra la acción preferida en la grilla 5x5 para ambos métodos.
    """
    ACTION_SYMBOLS = {0: "↓", 1: "↑", 2: "→", 3: "←", 4: "P", 5: "D"}
    # Walls del mapa de Taxi (columnas bloqueadas a la derecha de cada celda)
    # No las graficamos para no complicar, pero sí coloreamos la grilla

    grid = 5

    # Colapsamos los 500 estados a 25 (posición del taxi) promediando sobre
    # pasajero y destino para obtener V media por posición
    V_grid_vi = np.zeros(grid * grid)
    V_grid_ql = np.zeros(grid * grid)
    count = np.zeros(grid * grid)
    Q_max_grid = np.zeros(grid * grid)
    pol_vi_grid  = np.zeros(grid * grid, dtype=int)
    pol_ql_grid  = np.zeros(grid * grid, dtype=int)

    for s in range(500):
        # Decodificar estado de Taxi: (taxi_row, taxi_col, pass_loc, dest_idx)
        taxi_row = s // 100
        taxi_col = (s % 100) // 20
        pos = taxi_row * grid + taxi_col

        V_grid_vi[pos] += V_vi[s]
        V_grid_ql[pos] += np.max(Q_ql[s])
        count[pos] += 1

        # Política más frecuente (moda) – usamos suma de votos
        pol_vi_grid[pos] = policy_vi[s]  # última asignación, suficiente para viz
        pol_ql_grid[pos] = policy_ql[s]

    V_grid_vi /= np.maximum(count, 1)
    V_grid_ql /= np.maximum(count, 1)

    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle("Taxi-v4: Función de valor promedio y política (grilla 5×5)",
                 fontsize=13, fontweight='bold')

    # Ubicaciones especiales (R, G, Y, B)
    specials = {(0,0): "R", (0,4): "G", (4,0): "Y", (4,3): "B"}

    for ax, V_g, pol_g, method in zip(
            axes,
            [V_grid_vi, V_grid_ql],
            [pol_vi_grid, pol_ql_grid],
            ["Value Iteration", "Q-Learning"]):

        ax.set_title(method, fontsize=12)
        ax.set_xlim(0, grid); ax.set_ylim(0, grid)
        ax.set_xticks(range(grid+1)); ax.set_yticks(range(grid+1))
        ax.grid(True, color='gray', linewidth=0.5)

        vmin, vmax = V_g.min(), V_g.max()

        for row in range(grid):
            for col in range(grid):
                pos = row * grid + col
                x, y = col + 0.5, (grid - 1 - row) + 0.5

                # Color según valor
                norm_v = (V_g[pos] - vmin) / (vmax - vmin + 1e-9)
                color = plt.cm.YlGn(0.2 + 0.7 * norm_v)
                ax.add_patch(plt.Rectangle((col, grid-1-row), 1, 1,
                                           color=color, zorder=1))

                # Valor numérico
                ax.text(x, y + 0.2, f"{V_g[pos]:.1f}",
                        ha='center', va='center', fontsize=7, color='black', zorder=3)

                # Acción preferida
                label = specials.get((row, col), ACTION_SYMBOLS[pol_g[pos]])
                fc = 'navy' if (row, col) in specials else 'black'
                ax.text(x, y - 0.15, label,
                        ha='center', va='center', fontsize=12,
                        fontweight='bold', color=fc, zorder=3)

        ax.set_xticklabels([])
        ax.set_yticklabels([])

    # Leyenda acciones
    legend_items = [mpatches.Patch(color='white', label=f'{sym} = {name}')
                    for sym, name in [("↓","Sur"),("↑","Norte"),("→","Este"),("←","Oeste"),("P","Recoger"),("D","Dejar")]]
    fig.legend(handles=legend_items, loc='lower center', ncol=6, fontsize=9, frameon=True, bbox_to_anchor=(0.5, -0.04))

    plt.tight_layout()
    plt.savefig("./taxi_policy.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Gráfica guardada: taxi_policy.png")


def plot_comparison_bar(results):
    """Tabla visual de comparación entre métodos."""
    methods = list(results.keys())
    metrics = ["success_rate", "avg_reward", "avg_steps"]
    labels  = ["Tasa de éxito", "Recompensa promedio", "Pasos promedio"]
    colors  = ["#4C72B0", "#DD8452"]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle("Comparación Value Iteration vs Q-Learning – Taxi-v4", fontsize=13, fontweight='bold')

    for ax, metric, label in zip(axes, metrics, labels):
        vals = [results[m][metric] for m in methods]
        bars = ax.bar(methods, vals, color=colors[:len(methods)], width=0.4, edgecolor='white', linewidth=1.2)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + abs(max(vals)) * 0.02,
                    f"{val:.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax.set_title(label)
        ax.set_ylabel(label)
        ax.grid(True, axis='y', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig("./taxi_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Gráfica guardada: taxi_comparison.png")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def run_point2():
    print("  PUNTO 2 – RESOLUCIÓN DE TAXI-v4")
    env = gym.make("Taxi-v4")

    # ── PARTE A: VALUE ITERATION ──────────────────────────────
    print("─" * 60)
    print("  PARTE A: VALUE ITERATION")
    print("─" * 60)

    V_vi, policy_vi = value_iteration(env, gamma=0.99, theta=1e-8)

    res_vi = evaluar_politica(env, policy_vi, n_episodes=1000)
    print(f"  Tasa de éxito    : {res_vi['success_rate']*100:.1f}%")
    print(f"  Recompensa media : {res_vi['avg_reward']:.2f}")
    print(f"  Pasos promedio   : {res_vi['avg_steps']:.1f}")

    # Estadísticas de la función de valor
    print(f"\n  Función de valor V*:")
    print(f"    Min  : {V_vi.min():.4f}")
    print(f"    Max  : {V_vi.max():.4f}")
    print(f"    Media: {V_vi.mean():.4f}")

    # ── PARTE B: Q-LEARNING ───────────────────────────────────
    print("\n" + "─" * 60)
    print("  PARTE B: Q-LEARNING")
    print("─" * 60)
    print("  Entrenando 5000 episodios (α=0.1, γ=0.99, ε decay=0.999)...")

    Q_ql, policy_ql, rewards_ql, steps_ql = q_learning(
        env,
        episodes=5000,
        alpha=0.1,
        gamma=0.99,
        epsilon=1.0,
        epsilon_decay=0.999,
        epsilon_min=0.01
    )

    res_ql = evaluar_politica(env, policy_ql, n_episodes=1000)
    print(f"  Tasa de éxito    : {res_ql['success_rate']*100:.1f}%")
    print(f"  Recompensa media : {res_ql['avg_reward']:.2f}")
    print(f"  Pasos promedio   : {res_ql['avg_steps']:.1f}")
    print(f"\n  Recompensa promedio últimos 500 episodios: "
          f"{np.mean(rewards_ql[-500:]):.2f}")
    print(f"  Pasos promedio últimos 500 episodios    : "
          f"{np.mean(steps_ql[-500:]):.1f}")

    # ── COMPARACIÓN FINAL ─────────────────────────────────────
    print("\n" + "─" * 60)
    print("  COMPARACIÓN: VALUE ITERATION vs Q-LEARNING")
    print("─" * 60)
    print(f"\n  {'Métrica':<25} | {'Value Iteration':>16} | {'Q-Learning':>12}")
    print("  " + "-" * 58)
    print(f"  {'Tasa de éxito':<25} | {res_vi['success_rate']*100:>14.1f}% | {res_ql['success_rate']*100:>10.1f}%")
    print(f"  {'Recompensa promedio':<25} | {res_vi['avg_reward']:>16.2f} | {res_ql['avg_reward']:>12.2f}")
    print(f"  {'Pasos promedio':<25} | {res_vi['avg_steps']:>16.1f} | {res_ql['avg_steps']:>12.1f}")

    # ── GRÁFICAS ──────────────────────────────────────────────
    print("  GENERANDO GRÁFICAS")
    plot_training(rewards_ql, steps_ql)
    plot_value_comparison(V_vi, policy_vi, Q_ql, policy_ql)
    plot_comparison_bar({"Value Iteration": res_vi, "Q-Learning": res_ql})

    env.close()


if __name__ == "__main__":
    run_point2()
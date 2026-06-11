import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ──────────────────────────────────────────────
# PARTE A: VALUE ITERATION
# ──────────────────────────────────────────────

def value_iteration(env, gamma=0.99, theta=1e-8):
    n_states  = env.observation_space.n
    n_actions = env.action_space.n

    # 1. Inicializar la función de valor en cero
    V = np.zeros(n_states)

    iterations = 0
    while True:
        delta = 0
        # 2. Recorrer todos los estados
        for s in range(n_states):
            v_old = V[s]
            # 3. Evaluar todas las acciones posibles usando la dinámica env.P
            q_values = np.zeros(n_actions)
            for a in range(n_actions):
                # env.unwrapped.P[s][a] = lista de (prob, next_state, reward, done)
                for prob, next_state, reward, done in env.unwrapped.P[s][a]:
                    q_values[a] += prob * (reward + gamma * V[next_state] * (not done))
            # 4. Actualizar V con el máximo Q
            V[s] = np.max(q_values)
            delta = max(delta, abs(v_old - V[s]))

        iterations += 1
        # 5. Convergencia cuando el cambio máximo es menor que theta
        if delta < theta:
            break

    # 6. Extraer la política óptima
    policy = np.zeros(n_states, dtype=int)
    for s in range(n_states):
        q_values = np.zeros(n_actions)
        for a in range(n_actions):
            for prob, next_state, reward, done in env.unwrapped.P[s][a]:
                q_values[a] += prob * (reward + gamma * V[next_state] * (not done))
        policy[s] = np.argmax(q_values)

    print(f"  Value Iteration convergió en {iterations} iteraciones.")
    return V, policy


def evaluate_policy(env, policy, n_episodes=1000):
    """
    Ejecuta n_episodes con la política dada y retorna la tasa de éxito.
    """
    successes = 0
    for _ in range(n_episodes):
        state, _ = env.reset()
        done = False
        while not done:
            action = policy[state]
            state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
        if reward == 1.0:
            successes += 1
    return successes / n_episodes


def print_value_table(V, grid_size=4):
    """Imprime la tabla de valores como cuadrícula."""
    print("\n  Tabla de Valores V*(s):")
    print("  " + "-" * (9 * grid_size + 1))
    for row in range(grid_size):
        line = "  |"
        for col in range(grid_size):
            s = row * grid_size + col
            line += f" {V[s]:6.4f} |"
        print(line)
    print("  " + "-" * (9 * grid_size + 1))


def print_policy(policy, grid_size=4):
    """Imprime la política como flechas."""
    arrows = {0: "←", 1: "↓", 2: "→", 3: "↑"}
    holes  = {5, 7, 11, 12}   # posiciones de agujeros en FrozenLake 4x4
    goal   = {15}

    print("\n  Política óptima (flechas):")
    print("  " + "-" * (4 * grid_size + 1))
    for row in range(grid_size):
        line = "  |"
        for col in range(grid_size):
            s = row * grid_size + col
            if s in holes:
                line += " H |"
            elif s in goal:
                line += " G |"
            else:
                line += f" {arrows[policy[s]]} |"
        print(line)
    print("  " + "-" * (4 * grid_size + 1))


# ──────────────────────────────────────────────
# PARTE B: Q-LEARNING
# ──────────────────────────────────────────────

def q_learning(env, episodes=10000, alpha=0.1, gamma=0.99,
               epsilon=1.0, epsilon_decay=0.999, epsilon_min=0.01):
    n_states  = env.observation_space.n
    n_actions = env.action_space.n

    # 1. Inicializar la tabla Q en cero
    Q = np.zeros((n_states, n_actions))
    rewards_per_episode = []

    for ep in range(episodes):
        state, _ = env.reset()
        total_reward = 0
        done = False

        while not done:
            # 2. Estrategia epsilon-greedy
            if np.random.random() < epsilon:
                action = env.action_space.sample()          # exploración
            else:
                action = np.argmax(Q[state])                # explotación

            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            # 3. Actualizar Q con la ecuación de Q-Learning (off-policy)
            best_next = np.max(Q[next_state])
            Q[state, action] += alpha * (
                reward + gamma * best_next * (not done) - Q[state, action]
            )

            state = next_state
            total_reward += reward

        rewards_per_episode.append(total_reward)

        # Decay de epsilon
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

    # Política derivada de Q
    policy = np.argmax(Q, axis=1)
    return Q, policy, rewards_per_episode


# ──────────────────────────────────────────────
# VISUALIZACIÓN
# ──────────────────────────────────────────────

def plot_training(rewards_det, rewards_sto, window=200):
    """Gráfica de recompensas promedio durante el entrenamiento."""
    def moving_avg(data, w):
        return np.convolve(data, np.ones(w)/w, mode='valid')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Q-Learning: Recompensas durante el entrenamiento", fontsize=14, fontweight='bold')

    for ax, rewards, title in zip(
            axes,
            [rewards_det, rewards_sto],
            ["Determinístico (is_slippery=False)", "Estocástico (is_slippery=True)"]):
        ax.plot(rewards, alpha=0.3, color='steelblue', label='Recompensa por episodio')
        if len(rewards) >= window:
            avg = moving_avg(rewards, window)
            ax.plot(range(window-1, len(rewards)), avg,
                    color='darkorange', linewidth=2, label=f'Media móvil ({window} ep)')
        ax.set_title(title)
        ax.set_xlabel("Episodio")
        ax.set_ylabel("Recompensa")
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("./training_rewards.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("\n  Gráfica guardada: training_rewards.png")


def plot_value_comparison(V_det, V_sto, policy_vi_det, policy_vi_sto,
                          policy_ql_det, policy_ql_sto):
    """Visualiza tablas de valor y políticas de ambos métodos."""
    arrows = {0: "←", 1: "↓", 2: "→", 3: "↑"}
    holes  = [5, 7, 11, 12]
    goal   = [15]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("FrozenLake 4×4: Comparación de métodos", fontsize=14, fontweight='bold')

    configs = [
        (axes[0,0], V_det, policy_vi_det, "Value Iteration – Determinístico"),
        (axes[0,1], V_sto, policy_vi_sto, "Value Iteration – Estocástico"),
        (axes[1,0], None,  policy_ql_det, "Q-Learning – Determinístico"),
        (axes[1,1], None,  policy_ql_sto, "Q-Learning – Estocástico"),
    ]

    for ax, V, pol, title in configs:
        ax.set_title(title, fontsize=11)
        ax.set_xlim(0, 4); ax.set_ylim(0, 4)
        ax.set_xticks([]); ax.set_yticks([])

        for row in range(4):
            for col in range(4):
                s = row * 4 + col
                x, y = col + 0.5, 3 - row + 0.5

                if s in holes:
                    color = '#d9534f'
                    ax.add_patch(mpatches.FancyBboxPatch(
                        (col+0.05, 3-row+0.05), 0.9, 0.9,
                        boxstyle="round,pad=0.05", color=color, alpha=0.7))
                    ax.text(x, y, "H", ha='center', va='center',
                            fontsize=14, fontweight='bold', color='white')
                elif s in goal:
                    color = '#5cb85c'
                    ax.add_patch(mpatches.FancyBboxPatch(
                        (col+0.05, 3-row+0.05), 0.9, 0.9,
                        boxstyle="round,pad=0.05", color=color, alpha=0.7))
                    ax.text(x, y, "G", ha='center', va='center',
                            fontsize=14, fontweight='bold', color='white')
                else:
                    ax.add_patch(mpatches.FancyBboxPatch(
                        (col+0.05, 3-row+0.05), 0.9, 0.9,
                        boxstyle="round,pad=0.05", color='#d9edf7', alpha=0.9))
                    ax.text(x, y + 0.2, arrows[pol[s]],
                            ha='center', va='center', fontsize=18)
                    if V is not None:
                        ax.text(x, y - 0.2, f"{V[s]:.3f}",
                                ha='center', va='center', fontsize=8, color='gray')

        ax.set_aspect('equal')
        for spine in ax.spines.values():
            spine.set_visible(False)

    plt.tight_layout()
    plt.savefig("./policy_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Gráfica guardada: policy_comparison.png")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def run_point1():
    print("=" * 60)
    print("  PUNTO 1 – RESOLUCIÓN DE FROZEN LAKE")
    print("=" * 60)

    # ── PARTE A: VALUE ITERATION ──────────────────────────────

    print("\n" + "─" * 60)
    print("  PARTE A: VALUE ITERATION")
    print("─" * 60)

    for label, slippery in [("DETERMINÍSTICO", False), ("ESTOCÁSTICO", True)]:
        print(f"\n  [{label}]")
        env = gym.make("FrozenLake-v1", is_slippery=slippery)

        V, policy = value_iteration(env, gamma=0.99, theta=1e-8)
        print_value_table(V)
        print_policy(policy)

        success = evaluate_policy(env, policy, n_episodes=1000)
        print(f"  Tasa de éxito (1000 episodios): {success*100:.1f}%")

        if label == "DETERMINÍSTICO":
            V_det, policy_vi_det = V, policy
        else:
            V_sto, policy_vi_sto = V, policy

        env.close()

    # ── PARTE B: Q-LEARNING ───────────────────────────────────

    print("\n" + "─" * 60)
    print("  PARTE B: Q-LEARNING")
    print("─" * 60)

    for label, slippery in [("DETERMINÍSTICO", False), ("ESTOCÁSTICO", True)]:
        print(f"\n  [{label}]")
        env = gym.make("FrozenLake-v1", is_slippery=slippery)

        episodes = 10000
        Q, policy, rewards = q_learning(
            env,
            episodes=episodes,
            alpha=0.1,
            gamma=0.99,
            epsilon=1.0,
            epsilon_decay=0.999,
            epsilon_min=0.01
        )

        # Mostrar política
        print_policy(policy)

        # Tabla Q (últimas filas como muestra)
        print("\n  Tabla Q (estados 12-15):")
        print(f"  {'Estado':>6} | {'←':>8} {'↓':>8} {'→':>8} {'↑':>8}")
        print("  " + "-" * 45)
        for s in [12, 13, 14, 15]:
            row = " | ".join(f"{Q[s,a]:8.4f}" for a in range(4))
            print(f"  {s:>6} | {row}")

        success = evaluate_policy(env, policy, n_episodes=1000)
        print(f"\n  Tasa de éxito (1000 episodios): {success*100:.1f}%")
        print(f"  Recompensa promedio últimos 500 episodios: "
              f"{np.mean(rewards[-500:]):.4f}")

        if label == "DETERMINÍSTICO":
            rewards_det, policy_ql_det = rewards, policy
        else:
            rewards_sto, policy_ql_sto = rewards, policy

        env.close()

    # ── GRÁFICAS ──────────────────────────────────────────────

    print("\n" + "─" * 60)
    print("  GENERANDO GRÁFICAS")
    print("─" * 60)
    plot_training(rewards_det, rewards_sto)
    plot_value_comparison(V_det, V_sto,
                          policy_vi_det, policy_vi_sto,
                          policy_ql_det, policy_ql_sto)

    # ── COMPARACIÓN FINAL ─────────────────────────────────────

    print("\n" + "─" * 60)
    print("  COMPARACIÓN: VALUE ITERATION vs Q-LEARNING")
    print("─" * 60)

    envs = {
        "Determinístico": gym.make("FrozenLake-v1", is_slippery=False),
        "Estocástico":    gym.make("FrozenLake-v1", is_slippery=True),
    }
    policies = {
        "Determinístico": (policy_vi_det, policy_ql_det),
        "Estocástico":    (policy_vi_sto, policy_ql_sto),
    }

    print(f"\n  {'Entorno':<16} | {'Value Iteration':>16} | {'Q-Learning':>12}")
    print("  " + "-" * 50)
    for name, env in envs.items():
        vi_pol, ql_pol = policies[name]
        vi_rate = evaluate_policy(env, vi_pol, 1000)
        ql_rate = evaluate_policy(env, ql_pol, 1000)
        print(f"  {name:<16} | {vi_rate*100:>14.1f} % | {ql_rate*100:>10.1f} %")
        env.close()

if __name__ == "__main__":
    run_point1()
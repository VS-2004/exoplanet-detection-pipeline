import matplotlib.pyplot as plt
def plot_raw(time, flux, title="", save_path=None):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(time, flux, s=2)
    ax.set_xlabel("Time (BJD)")
    ax.set_ylabel("Normalized Flux")
    ax.set_title(title)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig
def plot_phase_folded(time, flux, period, t0, model_phase=None, model_flux=None, title="", save_path=None):
    phase = ((time - t0 + 0.5 * period) % period) / period - 0.5
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(phase, flux, s=2, alpha=0.5)
    if model_phase is not None:
        ax.plot(model_phase, model_flux, color="red")
    ax.set_xlabel("Phase")
    ax.set_ylabel("Normalized Flux")
    ax.set_title(title)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig

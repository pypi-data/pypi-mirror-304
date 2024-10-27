def add_titles(axes, colors=None):
    return [
        ax.text(
            0.02, 0.98, 
            f'({chr(ord("a")+i)})', 
            ha='left', 
            va='top',
            transform=ax.transAxes,
            color = 'k' if colors is None else colors[i],
        ) for  i, ax in enumerate(axes)
    ]
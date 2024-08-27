import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_monthly_report(ts_df, income_data, expense_data, configs_json, date_str,currency):
    background_color = configs_json["background_colors"]
    palette = configs_json["palette"]
    dims = configs_json["subplot"]["dims"]
    fig_size = configs_json["subplot"]["fig_size"]
    grid_width = configs_json["subplot"]["gridspec"]["linewidth"]
    height_ratios = configs_json["subplot"]["gridspec"]["height_ratios"]
    metric_colors = configs_json["metric_color_codes"]
    text_style = configs_json["text_style"]
    grid_style = configs_json["graph_grid_style"]
    bar_style = configs_json["bar_graph_style"]
    main_title_config = configs_json["main_title"]

    # Create the figure with a specified subplot configuration
    fig, axes = plt.subplots(dims[0], dims[1], figsize=fig_size, gridspec_kw={'height_ratios': height_ratios})
    fig.patch.set_facecolor(background_color)  # Background color for the entire figure

    fig.suptitle(
        main_title_config["text"] + date_str,
        fontsize=main_title_config["font_size"],
        fontweight=main_title_config["font_weight"],
        color=main_title_config["color"],
        ha='center',  # Horizontal alignment
        va='top',     # Vertical alignment
    )

    fig.text(
        0.5, 0.94,  
        "All values are in currency: " + currency,  
        ha='center', 
        va='top',  
        fontsize=20,  
        color=main_title_config["color"], 
        fontweight='normal'  
    )

    # Adjust spacing between subplots to make room for the outer border
    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    for ax in axes.flat:
        # Set subplot borders
        for spine in ax.spines.values():
            spine.set_edgecolor('#ffffff')
            spine.set_linewidth(2)

    # Graph 1: Total Financial Metrics for the month
    ax1 = axes[0, 0]
    ax1.set_facecolor(background_color)
    data = ts_df.iloc[-1].to_dict()

    bars = ax1.bar(data.keys(), data.values(),
                   color=[metric_colors['income'], metric_colors['expense'], metric_colors['balance']],
                   alpha=bar_style['alpha'], edgecolor=bar_style['edge_color'],
                   linewidth=bar_style['line_width'], width=bar_style['bar_width'],
                   hatch=bar_style['hatch'], zorder=bar_style['zorder'])

    ax1.set_title(str(configs_json["graph_1"]["title"]),
                  fontsize=text_style["title"]["font"], color=text_style["color"], pad=text_style["title"]["pad"])
    ax1.set_ylabel(configs_json["graph_1"]["y_label"], fontsize=text_style["label"]["font"],
                   color=text_style["label"]["color"], labelpad=text_style["label"]["labelpad"])
    ax1.grid(True, which='major', color=text_style["color"], linestyle=grid_style["style"], linewidth=grid_style["major_width"])
    ax1.grid(True, which='minor', color=text_style["color"], linestyle=grid_style["style"], linewidth=grid_style["minor_width"])
    ax1.tick_params(axis='x', colors=text_style["color"], rotation=configs_json["graph_1"]["x_rotation"])
    ax1.tick_params(axis='y', colors=text_style["color"])

    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval + 20, round(yval, 2), ha='center', fontsize=12, color=text_style["color"])

    ax2 = axes[1, 0]
    ax2.set_facecolor(background_color)
    sns.barplot(y=income_data.index, x=income_data.values, palette=palette, hue=income_data.index, ax=ax2, legend=False,hatch=bar_style['hatch'])
    ax2.set_xlabel(configs_json["graph_2"]["x_label"], fontsize=text_style["label"]["font"], color=text_style["label"]["color"],)
    ax2.set_ylabel(configs_json["graph_2"]["y_label"], fontsize=text_style["label"]["font"], color=text_style["label"]["color"])
    ax2.set_title(configs_json["graph_2"]["title"], fontsize=text_style["title"]["font"], color=text_style["color"], pad=text_style["title"]["pad"])
    ax2.tick_params(axis='x', colors=text_style["color"])
    ax2.tick_params(axis='y', colors=text_style["color"])
    ax2.grid(True, which='major', color=text_style["color"], linestyle=grid_style["style"], linewidth=grid_style["major_width"])
    ax2.grid(True, which='minor', color=text_style["color"], linestyle=grid_style["style"], linewidth=grid_style["minor_width"])

    ax3 = axes[1, 1]
    ax3.set_facecolor(background_color)
    sns.barplot(y=expense_data.index, x=expense_data.values, palette=palette, hue=expense_data.index, ax=ax3, legend=False,hatch=bar_style['hatch'])
    ax3.set_xlabel(configs_json["graph_3"]["x_label"], fontsize=text_style["label"]["font"], color=text_style["label"]["color"])
    ax3.set_ylabel(configs_json["graph_3"]["y_label"], fontsize=text_style["label"]["font"], color=text_style["label"]["color"])
    ax3.set_title(configs_json["graph_3"]["title"], fontsize=text_style["title"]["font"], color=text_style["color"], pad=text_style["title"]["pad"])
    ax3.tick_params(axis='x', colors=text_style["color"])
    ax3.tick_params(axis='y', colors=text_style["color"])
    ax3.grid(True, which='major', color=text_style["color"], linestyle=grid_style["style"], linewidth=grid_style["major_width"])
    ax3.grid(True, which='minor', color=text_style["color"], linestyle=grid_style["style"], linewidth=grid_style["minor_width"])

    ax4 = axes[0, 1]
    ax4.set_facecolor(background_color)

    sns.lineplot(data=ts_df, x=ts_df.index, y="credit", label="Income", linewidth=1.5,
                 color=metric_colors['income'], linestyle='--', ax=ax4)
    sns.lineplot(data=ts_df, x=ts_df.index, y="debit", label="Expenses", linewidth=1.5,
                 color=metric_colors['expense'], linestyle='--', ax=ax4)
    sns.lineplot(data=ts_df, x=ts_df.index, y="balance", label="Balance", linewidth=1.5,
                 color=metric_colors['balance'], linestyle='--', ax=ax4)

    ax4.axhline(y=0, color=text_style["color"], linewidth=0.5, linestyle='dashdot')
    ax4.grid(True, which='major', color=text_style["color"], linestyle=grid_style["style"], linewidth=grid_style["major_width"])
    ax4.grid(True, which='minor', color=text_style["color"], linestyle=grid_style["style"], linewidth=grid_style["minor_width"])
    ax4.tick_params(axis='x', colors=text_style["color"], rotation=45)
    ax4.tick_params(axis='y', colors=text_style["color"])
    ax4.set_xlabel(configs_json["graph_4"]["x_label"], fontsize=text_style["label"]["font"], color=text_style["label"]["color"], labelpad=text_style["label"]["labelpad"])
    ax4.set_ylabel(configs_json["graph_4"]["y_label"], fontsize=text_style["label"]["font"], color=text_style["label"]["color"], labelpad=text_style["label"]["labelpad"])
    ax4.set_title(configs_json["graph_4"]["title"], fontsize=text_style["title"]["font"], color=text_style["color"], pad=text_style["title"]["pad"])

    legend = ax4.legend(loc="upper left", fontsize=12, facecolor=background_color, edgecolor='white')
    for text in legend.get_texts():
        text.set_color(text_style["color"])

    fig.patch.set_linewidth(grid_width)  
    fig.patch.set_edgecolor('white')  

    buffer = io.BytesIO()
    plt.savefig(buffer, format='pdf', facecolor=fig.get_facecolor(), bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    return buffer

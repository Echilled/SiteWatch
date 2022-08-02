import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import pandas as pd

Stats = {}


def json_indexer(filename):
    property_list = []
    with open(filename, "r") as file:
        try:
            data = json.load(file)
            for url, property in data['URLs'].items():
                Stats[url] = property['properties']
            return Stats
        except Exception as e:
            print(e)
            print("First time archiving")


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def create_scatterplot():
    try:
        json_indexer('archive/WebHash.Json')
        date_list = []
        changed_count_list = []
        url_list = []
        x_axis = date_list
        for key, property in Stats.items():
            url_list.append(key)
            date_list.append(property['archival_date'].split(" ", 1)[0])
            changed_count_list.append(property['number of times URL content change'])
        date_list = [pd.to_datetime(d) for d in date_list]
        y_axis = changed_count_list
        plt.yticks(list(range(1, max(y_axis) + 1)), [str(i) for i in range(1, max(y_axis) + 1)])
        plt.xticks(fontsize=6)
        plt.xlabel("Date last checked")
        plt.ylabel("No. of times it's content changed")
        plt.scatter(x_axis, y_axis)
        for i, txt in enumerate(url_list):
            plt.annotate(txt, (x_axis[i], y_axis[i]), fontsize=6)
        return plt.gcf()
    except FileNotFoundError:
        print("this")
        pass


def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')


def main():

    json_indexer("archive/WebHash.Json")
    create_scatterplot()
    # creating the bar plot


if __name__ == '__main__':
    main()

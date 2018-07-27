import matplotlib.pyplot as plt
import pandas as pd
from threading import Thread


class EmployeePerformanceAnalyser(object):
    def __init__(self, employee_data="EmployeeData.msg"):
        self.data_file = employee_data
        self.data_frame = pd.read_msgpack("EmployeeDataComplete.msg")
        self.multi_index_creation()
        for dates, new_df in self.data_frame.groupby(level=0):
            self.data_graph_creation(dates,new_df)
        print("WAIT")


    def multi_index_creation(self):
        self.data_frame.set_index(['DATE', 'TIME'], inplace=True)

    def data_graph_creation(self, dates,data_frame):
        plot_graph = data_frame['FINAL COUNT'].plot(kind='line', title=dates, legend=True,fontsize=12)
        plot_graph.set_xlabel("Minutes", fontsize=12)
        plot_graph.set_ylabel("Activity Count", fontsize=12)
        plt.show()

    def panel_creation(self, start_date, end_date):
        """
        For Converting the dataframes into panel for better vision of data
        :rtype: object
        :param start_date:
        :param end_date:
        """
        panel_dictionary = {}
        for date in range(start_date, end_date):
            merged_dataframe = pd.DataFrame()
            for index in self.data_frame.iterrows():
                self.empty_index = "18/07/{0}".format(str(date).zfill(2))
                if self.empty_index in index[0]:
                    merged_dataframe = merged_dataframe.append(
                        self.data_frame.rename({index[0]: index[0].split("_")[1]}).loc[index[0].split("_")[1]])
            panel_dictionary[self.empty_index] = merged_dataframe
            print(merged_dataframe)
        self.panel_frame = pd.Panel(panel_dictionary)
        self.panel_frame.to_msgpack(self.data_file)

    def data_synchronize(self, start_date, end_date):
        """
        For synchronize the missing data with empty string and sorting it accoridng to index.
        :rtype: object
        :param start_date:
        :param end_date:
        """
        new_data_frame = pd.DataFrame()
        for date in range(start_date, end_date):
            column = ["DATE", "TIME", "PRESSED CHAR", "PRESSED COUNT", "RELEASED CHAR", "RELEASED COUNT",
                      "MOUSE MOVE COUNT", "MOUSE CLICKED COUNT", "MOUSE SCROLLED COUNT", "FINAL COUNT"]
            for hour in range(0, 24):
                for minute in range(0, 60):
                    empty_index = "18/07/{0}_{1}:{2}".format(str(date).zfill(2), str(hour).zfill(2),
                                                             str(minute).zfill(2))
                    if not empty_index in self.data_frame.index:
                        empty_data = [
                            ["18/07/{0}".format(str(date).zfill(2)), str(hour).zfill(2) + ":" + str(minute).zfill(2),
                             "N/A", 0, "N/A", 0, 0, 0, 0, 0]]
                        new_data_frame = new_data_frame.append(
                            pd.DataFrame(data=empty_data, columns=column))
                    else:
                        extra_data = list(self.data_frame.loc[empty_index].values)
                        extra_data.insert(0, "18/07/{0}".format(str(date).zfill(2)))
                        extra_data.insert(1, str(hour).zfill(2) + ":" + str(minute).zfill(2))
                        new_data_frame = new_data_frame.append(
                            pd.DataFrame(data=[extra_data], columns=column))
        new_data_frame.sort_index(inplace=True)
        new_data_frame.to_msgpack("EmployeeDataComplete.msg")


if __name__ == '__main__':
    ROOT = EmployeePerformanceAnalyser()
